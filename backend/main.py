from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analyze
from config import settings
import os

# Create upload directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Resume Score Analyzer - AI-powered resume analysis with improvement suggestions",
    version="1.0.0"
)

# CORS middleware - allow all for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router)

@app.get("/")
def root():
    return {
        "message": "Resume Score Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
