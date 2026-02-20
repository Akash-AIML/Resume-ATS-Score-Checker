---
title: Resume ATS Score Checker API
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Resume ATS Score Checker - Backend API

FastAPI backend for AI-powered resume analysis with semantic similarity scoring.

## Features

- **PDF Processing** - Extract text from resume and job description PDFs
- **Semantic Scoring** - Uses sentence-transformers for embedding similarity
- **AI Suggestions** - OpenAI-powered improvement recommendations
- **RAG Explainability** - Detailed breakdown of score components

## API Endpoints

- `POST /analyze/resume` - Analyze resume against job description
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Environment Variables

Set `OPENAI_API_KEY` in your HF Space secrets for AI-powered suggestions.

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

API available at http://localhost:7860/docs
