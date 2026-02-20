# 🚀 ATS Resume Analyzer - Complete Setup Guide

## 📋 Prerequisites

- ✅ Node.js 18+ (already installed)
- ✅ Python 3.9+
- ⬜ PostgreSQL database
- ⬜ OpenAI API key

---

## 🗄️ Step 1: Set Up PostgreSQL Database

### Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Start PostgreSQL
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create Database and User
```bash
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE ats_db;
CREATE USER ats_user WITH PASSWORD 'ats_password_123';
GRANT ALL PRIVILEGES ON DATABASE ats_db TO ats_user;
\q
```

---

## 🐍 Step 2: Set Up Backend

### Navigate to Backend
```bash
cd /home/akash/Resume_Score/backend
```

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Edit `/home/akash/Resume_Score/backend/.env`:

**REQUIRED - Update these:**
```bash
# Database - Update with your PostgreSQL password
DATABASE_URL=postgresql://ats_user:ats_password_123@localhost:5432/ats_db

# OpenAI - Add your API key
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**OPTIONAL - Google OAuth (can skip for now):**
```bash
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Initialize Database
```bash
python init_db.py
```

This will:
- Create all database tables
- Seed 5 job sections (Software Engineering, Data Science, etc.)

### Create Admin User
```bash
python create_admin.py
```

**Default Admin Credentials:**
- **Email**: `admin@ats.com`
- **Password**: `admin123`

### Start Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend running at**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

---

## ⚛️ Step 3: Configure Frontend

### Update Frontend Environment

Edit `/home/akash/Resume_Score/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Frontend is Already Running!
Your frontend is already running at: http://localhost:3000

---

## 🎯 Step 4: Test the Application

### 1. **Open Frontend**
Visit: http://localhost:3000

### 2. **Login as Admin**
- Click "Login" button
- Email: `admin@ats.com`
- Password: `admin123`

### 3. **Create a Job (Admin)**
- Navigate to "Admin Dashboard" → "Manage Jobs"
- Select a job section (e.g., "Software Engineering")
- Click "Create New Job"
- Fill in:
  - Title: "Senior Full Stack Developer"
  - Description: "We're looking for an experienced full-stack developer..."
  - Requirements: "5+ years experience, React, Node.js, Python, AWS..."
- Click "Create Job"

### 4. **Upload Job Documents (Optional)**
- In the job card, click "Upload Document"
- Upload any relevant PDFs (job descriptions, requirements docs)

### 5. **Test as User**
- Logout from admin account
- Register a new user account
- Browse jobs
- Upload a resume (PDF only, max 5MB)

### 6. **Run Ranking (Admin)**
- Login as admin
- Go to "Rank Resumes"
- Select the job section and job role
- Click "Run Ranking"
- View ranked results with scores

### 7. **View Explanation (User)**
- Login as the user who uploaded the resume
- Go to "My Results"
- Click "View Explanation"
- See RAG-generated feedback

---

## 🔑 Default Credentials

### Admin Account
```
Email: admin@ats.com
Password: admin123
```

### Test User Account
Create your own by clicking "Register" on the frontend!

---

## 🛠️ Troubleshooting

### Backend won't start?
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check if port 8000 is available
lsof -i :8000

# View backend logs
tail -f backend.log
```

### Frontend can't connect to backend?
- Make sure backend is running on port 8000
- Check `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Check browser console for CORS errors

### Database connection error?
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Test connection: `psql postgresql://ats_user:ats_password_123@localhost:5432/ats_db`

### OpenAI API errors?
- Verify your API key is correct in `.env`
- Check you have credits: https://platform.openai.com/usage
- Ensure `OPENAI_API_KEY` starts with `sk-`

---

## 📁 Project Structure

```
Resume_Score/
├── frontend/          # Next.js frontend (running on :3000)
│   ├── app/          # Pages and routes
│   ├── lib/          # API client
│   └── types/        # TypeScript types
├── backend/          # FastAPI backend (running on :8000)
│   ├── routes/       # API endpoints
│   ├── auth/         # Authentication
│   ├── processing/   # PDF processing
│   ├── embeddings/   # Vector store
│   ├── scoring/      # Ranking engine
│   └── rag/          # RAG explainer
└── SETUP_GUIDE.md   # This file
```

---

## 🎉 You're All Set!

Your ATS Resume Analyzer is now running with:
- ✅ Frontend on http://localhost:3000
- ✅ Backend on http://localhost:8000
- ✅ Admin account ready
- ✅ Database initialized
- ✅ RAG explainability enabled

**Happy analyzing! 🚀**
