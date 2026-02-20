# ATS Resume Analyzer - Backend

Production-grade FastAPI backend for ATS Resume Analyzer with semantic ranking and RAG explainability.

## 🚀 Features

- **FastAPI** REST API with automatic OpenAPI docs
- **JWT Authentication** + **Google OAuth 2.0**
- **PDF Processing** with pdfplumber and PyPDF2 fallback
- **OpenAI Embeddings** using text-embedding-3-small
- **ChromaDB** vector database for semantic search
- **Deterministic Ranking Engine** with weighted scoring
- **RAG Explainability** using LangChain + GPT-3.5-turbo
- **PostgreSQL** database with SQLAlchemy ORM

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL database
- OpenAI API key
- Google OAuth credentials (optional)

## 🛠️ Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)
- `GOOGLE_CLIENT_ID`: Google OAuth client ID (optional)
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret (optional)

### 4. Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Seed 5 default job sections

### 5. Run the Server

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py              # Settings and configuration
├── database.py            # Database connection
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── init_db.py             # Database initialization
├── auth/
│   ├── jwt_handler.py     # JWT token management
│   ├── google_oauth.py    # Google OAuth verification
│   └── dependencies.py    # Auth dependencies
├── processing/
│   ├── pdf_extractor.py   # PDF text extraction
│   └── chunker.py         # Custom chunking logic
├── embeddings/
│   ├── model_manager.py   # OpenAI embedding model
│   └── vector_store.py    # ChromaDB vector store
├── scoring/
│   └── ranking_engine.py  # Deterministic ranking
├── rag/
│   └── explainer.py       # RAG-based explanations
└── routes/
    ├── auth.py            # Authentication endpoints
    ├── jobs.py            # Job management endpoints
    ├── resumes.py         # Resume upload endpoints
    └── ranking.py         # Ranking & explanation endpoints
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register with email/password
- `POST /auth/login` - Login with email/password
- `POST /auth/google` - Login with Google OAuth

### Jobs
- `GET /jobs/sections` - Get all job sections
- `GET /jobs/section/{name}` - Get jobs in a section
- `GET /jobs/{id}` - Get job details
- `POST /jobs/` - Create job (admin)
- `PUT /jobs/{id}` - Update job (admin)
- `DELETE /jobs/{id}` - Delete job (admin)
- `GET /jobs/{id}/documents` - Get job documents
- `POST /jobs/{id}/documents` - Upload job document (admin)

### Resumes
- `POST /resumes/upload` - Upload resume
- `GET /resumes/my-resumes` - Get user's resumes
- `GET /resumes/job/{id}` - Get resumes for job (admin)

### Ranking
- `POST /ranking/rank` - Run ranking for a job (admin)
- `GET /ranking/results/{job_id}` - Get ranking results (admin)
- `GET /ranking/my-results` - Get user's results
- `GET /ranking/explanation/{result_id}` - Get RAG explanation

## 🎯 Ranking Algorithm

**Weighted Scoring:**
- Skills: 40%
- Experience: 30%
- Education: 15%
- Projects: 15%

**Process:**
1. Extract text from PDF resume
2. Detect sections (skills, experience, education, projects)
3. Chunk text semantically
4. Generate embeddings using OpenAI text-embedding-3-small
5. Store in ChromaDB vector database
6. Calculate cosine similarity with job requirements
7. Apply weighted scoring formula
8. Generate RAG explanation using LangChain + GPT-3.5-turbo

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google`
6. Copy Client ID and Client Secret to `.env`

## 🗄️ Database Schema

- **users**: User accounts (email, password, Google ID, role)
- **job_sections**: 5 predefined job categories
- **job_roles**: Job postings within sections
- **job_documents**: Documents attached to jobs
- **resumes**: Uploaded resumes
- **ranking_results**: Scoring results with explanations

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=. --cov-report=html
```

## 🚀 Deployment

### Using Docker

```bash
docker build -t ats-backend .
docker run -p 8000:8000 --env-file .env ats-backend
```

### Using Railway/Render

1. Connect your GitHub repository
2. Set environment variables
3. Deploy with auto-scaling

## 📝 License

MIT License
# Resume-ATS-Score-Checker
