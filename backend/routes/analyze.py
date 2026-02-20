from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import uuid
import tempfile
from pydantic import BaseModel
from typing import List, Dict

from embeddings.model_manager import EmbeddingModel
from scoring.ranking_engine import RankingEngine
from rag.explainer import RAGExplainer
from processing.pdf_extractor import PDFExtractor
from processing.chunker import ResumeChunker
from config import settings

router = APIRouter(prefix="/analyze", tags=["Resume Analysis"])

# Initialize services
embedding_model = EmbeddingModel(settings.EMBEDDING_MODEL)
ranking_engine = RankingEngine()
rag_explainer = RAGExplainer()


class AnalysisResponse(BaseModel):
    score: float
    breakdown: Dict[str, float]
    overall_assessment: str
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    improvement_suggestions: List[str]


@router.post("/resume", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description_text: Optional[str] = Form(None, description="Job description as text"),
    job_description_file: Optional[UploadFile] = File(None, description="Job description as PDF")
):
    """
    Analyze a resume against a job description.
    
    Provide either job_description_text OR job_description_file (PDF).
    Returns score, breakdown, and AI-powered improvement suggestions.
    """
    
    # Validate inputs
    if not job_description_text and not job_description_file:
        raise HTTPException(
            status_code=400, 
            detail="Please provide either job description text or a job description PDF"
        )
    
    if not resume.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Resume must be a PDF file")
    
    try:
        # Save resume temporarily
        resume_temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.pdf")
        with open(resume_temp_path, "wb") as f:
            content = await resume.read()
            f.write(content)
        
        # Extract resume text
        resume_text = PDFExtractor.extract_text(resume_temp_path)
        resume_sections = PDFExtractor.detect_sections(resume_text)
        resume_chunks = ResumeChunker.chunk_by_sections(resume_sections)
        
        # If no chunks, create a single chunk from full text
        if not resume_chunks:
            resume_chunks = [{
                'text': resume_text,
                'section': 'other',
                'chunk_type': 'full',
                'position': 0
            }]
        
        # Get job description
        if job_description_file and job_description_file.filename:
            # Extract from PDF
            job_temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.pdf")
            with open(job_temp_path, "wb") as f:
                job_content = await job_description_file.read()
                f.write(job_content)
            job_text = PDFExtractor.extract_text(job_temp_path)
            os.remove(job_temp_path)
        else:
            job_text = job_description_text
        
        # Create job chunks
        job_chunks = [
            {'text': job_text, 'section': 'description', 'position': 0},
            {'text': job_text, 'section': 'requirements', 'position': 1}
        ]
        
        # Generate embeddings
        resume_texts = [chunk['text'] for chunk in resume_chunks]
        job_texts = [chunk['text'] for chunk in job_chunks]
        
        resume_embeddings = embedding_model.encode(resume_texts)
        job_embeddings = embedding_model.encode(job_texts)
        
        # Calculate ranking
        ranking_result = ranking_engine.rank_resume(
            resume_chunks, job_chunks,
            resume_embeddings, job_embeddings
        )
        
        # Generate AI explanation and suggestions
        explanation = rag_explainer.generate_explanation(
            resume_text=resume_text,
            job_description=job_text,
            ranking_result=ranking_result,
            resume_chunks=resume_chunks,
            job_chunks=job_chunks
        )
        
        # Clean up temp file
        os.remove(resume_temp_path)
        
        return AnalysisResponse(
            score=ranking_result['score'],
            breakdown=ranking_result['breakdown'],
            overall_assessment=explanation.get('overall_assessment', ''),
            matched_skills=explanation.get('matched_skills', []),
            missing_skills=explanation.get('missing_skills', []),
            strengths=explanation.get('strengths', []),
            improvement_suggestions=explanation.get('improvement_suggestions', [])
        )
        
    except Exception as e:
        # Clean up temp files on error
        if 'resume_temp_path' in locals() and os.path.exists(resume_temp_path):
            os.remove(resume_temp_path)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/text", response_model=AnalysisResponse)
async def analyze_resume_text(
    resume_text: str = Form(..., description="Resume text content"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze resume text against job description text.
    Use this endpoint if you already have extracted text.
    """
    
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    try:
        # Detect sections from resume text
        resume_sections = PDFExtractor.detect_sections(resume_text)
        resume_chunks = ResumeChunker.chunk_by_sections(resume_sections)
        
        if not resume_chunks:
            resume_chunks = [{
                'text': resume_text,
                'section': 'other',
                'chunk_type': 'full',
                'position': 0
            }]
        
        # Create job chunks
        job_chunks = [
            {'text': job_description, 'section': 'description', 'position': 0},
            {'text': job_description, 'section': 'requirements', 'position': 1}
        ]
        
        # Generate embeddings
        resume_texts = [chunk['text'] for chunk in resume_chunks]
        job_texts = [chunk['text'] for chunk in job_chunks]
        
        resume_embeddings = embedding_model.encode(resume_texts)
        job_embeddings = embedding_model.encode(job_texts)
        
        # Calculate ranking
        ranking_result = ranking_engine.rank_resume(
            resume_chunks, job_chunks,
            resume_embeddings, job_embeddings
        )
        
        # Generate AI explanation
        explanation = rag_explainer.generate_explanation(
            resume_text=resume_text,
            job_description=job_description,
            ranking_result=ranking_result,
            resume_chunks=resume_chunks,
            job_chunks=job_chunks
        )
        
        return AnalysisResponse(
            score=ranking_result['score'],
            breakdown=ranking_result['breakdown'],
            overall_assessment=explanation.get('overall_assessment', ''),
            matched_skills=explanation.get('matched_skills', []),
            missing_skills=explanation.get('missing_skills', []),
            strengths=explanation.get('strengths', []),
            improvement_suggestions=explanation.get('improvement_suggestions', [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
