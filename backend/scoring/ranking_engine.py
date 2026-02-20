from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RankingEngine:
    """Deterministic, weighted, rule-based scoring engine"""
    
    # Scoring weights
    WEIGHTS = {
        'skills': 0.40,      # 40% - Most important
        'experience': 0.30,  # 30%
        'education': 0.15,   # 15%
        'projects': 0.15     # 15%
    }
    
    @staticmethod
    def calculate_semantic_similarity(resume_embedding: np.ndarray, job_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between embeddings"""
        if resume_embedding.ndim == 1:
            resume_embedding = resume_embedding.reshape(1, -1)
        if job_embedding.ndim == 1:
            job_embedding = job_embedding.reshape(1, -1)
        
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return float(similarity)
    
    @staticmethod
    def score_skills(resume_chunks: List[Dict], job_chunks: List[Dict], 
                     resume_embeddings: np.ndarray, job_embeddings: np.ndarray) -> float:
        """Score skills match between resume and job"""
        # Filter skill-related chunks
        resume_skill_chunks = [c for c in resume_chunks if c['section'] == 'skills']
        job_skill_chunks = [c for c in job_chunks if 'skill' in c.get('section', '').lower() or 
                           'requirement' in c.get('section', '').lower()]
        
        if not resume_skill_chunks or not job_skill_chunks:
            return 0.0
        
        # Get corresponding embeddings
        resume_skill_indices = [i for i, c in enumerate(resume_chunks) if c['section'] == 'skills']
        job_skill_indices = [i for i, c in enumerate(job_chunks) if 'skill' in c.get('section', '').lower() or 
                            'requirement' in c.get('section', '').lower()]
        
        resume_skill_emb = resume_embeddings[resume_skill_indices]
        job_skill_emb = job_embeddings[job_skill_indices]
        
        # Calculate average similarity
        similarities = []
        for r_emb in resume_skill_emb:
            for j_emb in job_skill_emb:
                sim = RankingEngine.calculate_semantic_similarity(r_emb, j_emb)
                similarities.append(sim)
        
        avg_similarity = np.mean(similarities) if similarities else 0.0
        
        # Convert to 0-100 scale
        return float(avg_similarity * 100)
    
    @staticmethod
    def score_experience(resume_chunks: List[Dict], job_chunks: List[Dict],
                        resume_embeddings: np.ndarray, job_embeddings: np.ndarray) -> float:
        """Score experience match"""
        resume_exp_chunks = [c for c in resume_chunks if c['section'] == 'experience']
        job_exp_chunks = [c for c in job_chunks if 'experience' in c.get('section', '').lower() or
                         'responsibility' in c.get('section', '').lower()]
        
        if not resume_exp_chunks:
            return 0.0
        
        resume_exp_indices = [i for i, c in enumerate(resume_chunks) if c['section'] == 'experience']
        resume_exp_emb = resume_embeddings[resume_exp_indices]
        
        if not job_exp_chunks:
            # If no specific experience section in job, compare with all job chunks
            job_exp_emb = job_embeddings
        else:
            job_exp_indices = [i for i, c in enumerate(job_chunks) if 'experience' in c.get('section', '').lower() or
                              'responsibility' in c.get('section', '').lower()]
            job_exp_emb = job_embeddings[job_exp_indices]
        
        similarities = []
        for r_emb in resume_exp_emb:
            for j_emb in job_exp_emb:
                sim = RankingEngine.calculate_semantic_similarity(r_emb, j_emb)
                similarities.append(sim)
        
        avg_similarity = np.mean(similarities) if similarities else 0.0
        return float(avg_similarity * 100)
    
    @staticmethod
    def score_education(resume_chunks: List[Dict], job_chunks: List[Dict],
                       resume_embeddings: np.ndarray, job_embeddings: np.ndarray) -> float:
        """Score education match"""
        resume_edu_chunks = [c for c in resume_chunks if c['section'] == 'education']
        
        if not resume_edu_chunks:
            return 50.0  # Neutral score if no education section
        
        resume_edu_indices = [i for i, c in enumerate(resume_chunks) if c['section'] == 'education']
        resume_edu_emb = resume_embeddings[resume_edu_indices]
        
        # Compare with all job chunks
        similarities = []
        for r_emb in resume_edu_emb:
            for j_emb in job_embeddings:
                sim = RankingEngine.calculate_semantic_similarity(r_emb, j_emb)
                similarities.append(sim)
        
        avg_similarity = np.mean(similarities) if similarities else 0.5
        return float(avg_similarity * 100)
    
    @staticmethod
    def score_projects(resume_chunks: List[Dict], job_chunks: List[Dict],
                      resume_embeddings: np.ndarray, job_embeddings: np.ndarray) -> float:
        """Score projects match"""
        resume_proj_chunks = [c for c in resume_chunks if c['section'] == 'projects']
        
        if not resume_proj_chunks:
            return 50.0  # Neutral score if no projects section
        
        resume_proj_indices = [i for i, c in enumerate(resume_chunks) if c['section'] == 'projects']
        resume_proj_emb = resume_embeddings[resume_proj_indices]
        
        similarities = []
        for r_emb in resume_proj_emb:
            for j_emb in job_embeddings:
                sim = RankingEngine.calculate_semantic_similarity(r_emb, j_emb)
                similarities.append(sim)
        
        avg_similarity = np.mean(similarities) if similarities else 0.5
        return float(avg_similarity * 100)
    
    @staticmethod
    def calculate_overall_score(breakdown: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        overall = sum(breakdown[key] * RankingEngine.WEIGHTS[key] for key in RankingEngine.WEIGHTS)
        return round(overall, 2)
    
    @staticmethod
    def rank_resume(resume_chunks: List[Dict], job_chunks: List[Dict],
                   resume_embeddings: np.ndarray, job_embeddings: np.ndarray) -> Dict:
        """Main ranking function"""
        breakdown = {
            'skills': RankingEngine.score_skills(resume_chunks, job_chunks, resume_embeddings, job_embeddings),
            'experience': RankingEngine.score_experience(resume_chunks, job_chunks, resume_embeddings, job_embeddings),
            'education': RankingEngine.score_education(resume_chunks, job_chunks, resume_embeddings, job_embeddings),
            'projects': RankingEngine.score_projects(resume_chunks, job_chunks, resume_embeddings, job_embeddings)
        }
        
        overall_score = RankingEngine.calculate_overall_score(breakdown)
        
        return {
            'score': overall_score,
            'breakdown': breakdown
        }
