# 🔧 Quick Fixes for Current Issues

## Issue 1: Backend Authentication (bcrypt error)

**Problem**: Uvicorn reloader has cached old bcrypt 5.0.0 module  
**Solution**: Completely stop and restart the backend

```bash
# In the backend terminal:
# 1. Press Ctrl+C to stop uvicorn
# 2. Wait for it to fully stop
# 3. Restart:
uvicorn main:app --reload
```

## Issue 2: Resume Upload 422 Error

**Problem**: Frontend sending incorrect format for resume upload  
**Likely cause**: Missing `job_id` query parameter

The backend expects:
```
POST /resumes/upload?job_id=1
Content-Type: multipart/form-data
file: <PDF file>
```

Check frontend code to ensure it's sending `job_id` as a query parameter, not in the form data.

## Issue 3: React Error (Objects not valid as React child)

**Problem**: Frontend trying to render an error object directly  
**Error object structure**: `{type, loc, msg, input}`

This is a FastAPI validation error. The frontend needs to:
1. Check if response is an error
2. Extract the error message properly
3. Display it as a string, not render the object

**Frontend fix needed**: Handle 422 validation errors properly in the resume upload component.

---

## Quick Test

After restarting backend, test login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ats.com","password":"admin123"}'
```

Should return a JWT token, not a 500 error.
