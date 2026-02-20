# Quick Start Guide

## ⚡ Current Status
- ✅ Frontend running on http://localhost:3000
- ⏳ Backend setup in progress

## 🔧 Fix Database Issue

Your terminal is waiting for your **sudo password**. After entering it:

### 1. Initialize Database
```bash
conda activate ml
cd /home/akash/Resume_Score/backend
python init_db.py
python create_admin.py
```

### 2. Add OpenAI API Key
Edit `/home/akash/Resume_Score/backend/.env` line 18:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start Backend
```bash
uvicorn main:app --reload
```

## 🔑 Admin Login
```
Email: admin@ats.com
Password: admin123
```

## 🌐 URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
