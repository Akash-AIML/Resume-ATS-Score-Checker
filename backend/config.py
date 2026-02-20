from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Resume Score Analyzer"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 7860  # Hugging Face Spaces default port
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""  # Optional: for custom OpenAI-compatible APIs
    
    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Local model, no API needed
    
    # ChromaDB - use /tmp for Hugging Face Spaces
    CHROMA_PERSIST_DIRECTORY: str = os.environ.get("CHROMA_DIR", "/tmp/chroma_db")
    
    # File Storage - use /tmp for Hugging Face Spaces
    UPLOAD_DIR: str = os.environ.get("UPLOAD_DIR", "/tmp/uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
