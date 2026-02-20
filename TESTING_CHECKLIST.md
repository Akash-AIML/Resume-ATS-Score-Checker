# 🧪 Testing Checklist - ATS Resume Analyzer

## ✅ Step 1: Initialize Backend (Do this first!)

```bash
# Exit venv if active
deactivate

# Activate conda ml environment
conda activate ml
cd /home/akash/Resume_Score/backend

# Initialize database
python init_db.py
python create_admin.py

# Add your OpenAI API key to .env (line 18)
nano .env  # or use your editor
# OPENAI_API_KEY=sk-your-key-here

# Start backend
uvicorn main:app --reload
```

---

## 🌐 Step 2: Check Backend is Running

### Test 1: Health Check
Open browser: **http://localhost:8000/health**

Expected response:
```json
{"status": "healthy"}
```

### Test 2: API Documentation
Open browser: **http://localhost:8000/docs**

You should see:
- Interactive Swagger UI
- All API endpoints listed
- Authentication, Jobs, Resumes, Ranking sections

### Test 3: Root Endpoint
Open browser: **http://localhost:8000**

Expected response:
```json
{
  "message": "ATS Resume Analyzer API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 🎨 Step 3: Check Frontend (Already Running!)

### Test 1: Homepage
Open browser: **http://localhost:3000**

You should see:
- ✅ Landing page with hero section
- ✅ "Get Started" and "Learn More" buttons
- ✅ Beautiful gradient design

### Test 2: Login Page
Click "Login" or go to: **http://localhost:3000/login**

Try logging in with:
- **Email**: `admin@ats.com`
- **Password**: `admin123`

Expected: Redirect to admin dashboard

---

## 🔐 Step 4: Test Admin Features

### Test 1: Admin Dashboard
After login, you should see:
- ✅ "Manage Jobs" button
- ✅ "Rank Resumes" button
- ✅ Admin navigation

### Test 2: View Job Sections
Go to: **http://localhost:3000/admin/jobs**

You should see 5 job sections:
1. 💻 Software Engineering
2. 📊 Data Science
3. 📱 Product Management
4. ☁️ DevOps & Cloud
5. 🎨 Design & UX

### Test 3: Create a Job
1. Click on "Software Engineering"
2. Click "Create New Job"
3. Fill in:
   - **Title**: "Senior Full Stack Developer"
   - **Description**: "We're looking for an experienced developer..."
   - **Requirements**: "5+ years experience, React, Node.js, Python..."
4. Click "Create Job"

Expected: Job created successfully

---

## 👤 Step 5: Test User Features

### Test 1: Register New User
1. Logout from admin
2. Click "Register"
3. Create a test user account

### Test 2: Browse Jobs
Go to: **http://localhost:3000/jobs**

You should see:
- ✅ All 5 job sections
- ✅ Jobs you created as admin

### Test 3: Upload Resume
1. Click on a job
2. Click "Apply Now"
3. Upload a PDF resume (max 5MB)

Expected: Resume uploaded and processed

---

## 🎯 Step 6: Test Ranking System (Admin)

### Test 1: Run Ranking
1. Login as admin
2. Go to: **http://localhost:3000/admin/rank-resumes**
3. Select job section and job
4. Click "Run Ranking"

Expected:
- ✅ Processing message
- ✅ Ranked results table with scores
- ✅ Scores from 0-100

### Test 2: View Explanation
1. Click "View Explanation" on a ranked resume

Expected:
- ✅ Overall assessment
- ✅ Matched skills list
- ✅ Missing skills list
- ✅ Strengths
- ✅ Improvement suggestions

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
lsof -i :8000

# Check database connection
PGPASSWORD='ats_password_123' psql -h localhost -U ats_user -d ats_db -c "SELECT 1;"
```

### Frontend can't connect to backend?
- Check `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Check browser console for CORS errors
- Verify backend is running on port 8000

### OpenAI API errors?
- Verify API key in `.env` is correct
- Check you have credits: https://platform.openai.com/usage
- Test with: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"`

---

## 📊 Expected Flow

1. **Admin creates jobs** → Jobs stored in database
2. **Users upload resumes** → PDFs processed, text extracted, chunked, embedded
3. **Admin runs ranking** → Embeddings compared, scores calculated
4. **Users view results** → RAG generates explanations using GPT-3.5-turbo

---

## 🎉 Success Criteria

✅ Backend running on http://localhost:8000  
✅ Frontend running on http://localhost:3000  
✅ Can login as admin  
✅ Can create jobs  
✅ Can upload resumes  
✅ Can run ranking  
✅ Can view RAG explanations  

**If all checks pass, your ATS Resume Analyzer is fully functional!** 🚀
