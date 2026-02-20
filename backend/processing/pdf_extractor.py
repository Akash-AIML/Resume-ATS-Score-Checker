import pdfplumber
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
from typing import Dict, List

class PDFExtractor:
    """Extract text from PDF resumes with fallback mechanisms"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract text from PDF using pdfplumber, fallback to PyPDF2, then OCR"""
        try:
            # Primary: pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                
                if text.strip():
                    return PDFExtractor.normalize_text(text)
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        try:
            # Fallback 1: PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                
                if text.strip():
                    return PDFExtractor.normalize_text(text)
        except Exception as e:
            print(f"PyPDF2 failed: {e}, trying OCR...")
        
        try:
            # Fallback 2: OCR with Tesseract
            print("Attempting OCR extraction (this may take a moment)...")
            images = convert_from_path(pdf_path, dpi=300)
            text = ""
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='eng')
                text += page_text + "\n"
                print(f"OCR page {i+1}: extracted {len(page_text)} chars")
            
            if text.strip():
                return PDFExtractor.normalize_text(text)
            else:
                raise Exception("OCR extraction returned empty text")
        except Exception as e:
            raise Exception(f"All extraction methods failed. Last error (OCR): {e}")
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,;:()\-@]', '', text)
        return text.strip()
    
    @staticmethod
    def detect_sections(text: str) -> Dict[str, str]:
        """Detect common resume sections"""
        sections = {
            'experience': '',
            'education': '',
            'skills': '',
            'projects': '',
            'summary': '',
            'other': ''
        }
        
        # Section headers patterns
        patterns = {
            'experience': r'(experience|work history|employment|professional experience)',
            'education': r'(education|academic|qualifications|degrees)',
            'skills': r'(skills|technical skills|competencies|expertise)',
            'projects': r'(projects|portfolio|work samples)',
            'summary': r'(summary|objective|profile|about)'
        }
        
        text_lower = text.lower()
        
        # Find section boundaries
        section_positions = []
        for section_name, pattern in patterns.items():
            matches = list(re.finditer(pattern, text_lower))
            for match in matches:
                section_positions.append((match.start(), section_name))
        
        # Sort by position
        section_positions.sort()
        
        # Extract section content
        for i, (start_pos, section_name) in enumerate(section_positions):
            end_pos = section_positions[i + 1][0] if i + 1 < len(section_positions) else len(text)
            sections[section_name] = text[start_pos:end_pos].strip()
        
        # If no sections detected, put everything in 'other'
        if not any(sections.values()):
            sections['other'] = text
        
        return sections
