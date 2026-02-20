import re
from typing import List, Dict

class ResumeChunker:
    """Custom chunking strategy for resumes"""
    
    @staticmethod
    def chunk_by_sections(sections: Dict[str, str]) -> List[Dict[str, str]]:
        """Chunk resume by detected sections"""
        chunks = []
        
        for section_name, content in sections.items():
            if not content.strip():
                continue
            
            # Further split large sections
            if len(content) > 500:
                sub_chunks = ResumeChunker.semantic_sentence_chunking(content, max_length=500)
                for i, sub_chunk in enumerate(sub_chunks):
                    chunks.append({
                        'text': sub_chunk,
                        'section': section_name,
                        'chunk_type': 'sentence',
                        'position': i
                    })
            else:
                chunks.append({
                    'text': content,
                    'section': section_name,
                    'chunk_type': 'section',
                    'position': 0
                })
        
        return chunks
    
    @staticmethod
    def semantic_sentence_chunking(text: str, max_length: int = 500) -> List[str]:
        """Split text into semantic chunks at sentence boundaries"""
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    @staticmethod
    def extract_skills_with_context(text: str, window_size: int = 100) -> List[Dict[str, str]]:
        """Extract skills with surrounding context"""
        # Common skill patterns
        skill_patterns = [
            r'\b(Python|Java|JavaScript|C\+\+|SQL|React|Node\.js|Docker|Kubernetes)\b',
            r'\b(Machine Learning|Deep Learning|NLP|Computer Vision|Data Science)\b',
            r'\b(AWS|Azure|GCP|Cloud|DevOps|CI/CD)\b'
        ]
        
        skills_with_context = []
        
        for pattern in skill_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - window_size)
                end = min(len(text), match.end() + window_size)
                context = text[start:end]
                
                skills_with_context.append({
                    'skill': match.group(),
                    'context': context,
                    'position': match.start()
                })
        
        return skills_with_context
