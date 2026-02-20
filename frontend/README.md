# ATS Resume Analyzer - Frontend

Production-grade Next.js 14 frontend for the ATS Resume Analyzer with semantic ranking and explainable AI.

## 🚀 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: JWT-based (localStorage)
- **HTTP Client**: Axios
- **Charts**: Recharts
- **File Upload**: react-dropzone
- **Icons**: Lucide React

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing page
│   ├── globals.css             # Global styles
│   ├── login/
│   │   └── page.tsx            # Login/Register
│   ├── jobs/
│   │   ├── page.tsx            # Browse jobs (5 sections)
│   │   └── [jobId]/
│   │       └── apply/
│   │           └── page.tsx    # Apply with resume
│   ├── results/
│   │   └── page.tsx            # View ranking results
│   ├── explanation/
│   │   └── [resultId]/
│   │       └── page.tsx        # RAG explanation
│   └── admin/
│       ├── jobs/
│       │   └── page.tsx        # Manage jobs (CRUD)
│       └── rank-resumes/
│           └── page.tsx        # Run ranking
├── lib/
│   └── api.ts                  # Axios client
├── types/
│   └── index.ts                # TypeScript interfaces
└── package.json
```

## 🎨 Features

### User Features
- **Browse Jobs**: 5 predefined sections (Software Engineering, Data Science, Product Management, DevOps, UI/UX)
- **Apply to Jobs**: Upload resume for specific job roles
- **View Results**: See ranking scores with visual breakdowns
- **Detailed Explanations**: RAG-powered insights on matched/missing skills

### Admin Features
- **Job Management**: Create, edit, delete job roles
- **Document Upload**: Attach job descriptions and requirements
- **Resume Ranking**: Run AI-powered ranking for applicants
- **View Rankings**: See all candidates sorted by score

## 🛠️ Setup Instructions

### Prerequisites

**IMPORTANT**: This project requires **Node.js 18+**. Your current version is v12.22.9.

#### Update Node.js

```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Or using NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local .env.local.example
# Edit .env.local with your backend URL

# Run development server
npm run dev
```

The app will be available at `http://localhost:3000`

## 🔧 Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here
```

## 🎯 API Integration

The frontend expects the following backend endpoints:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Jobs
- `GET /jobs/sections` - Get all job sections
- `GET /jobs/section/{name}` - Get jobs in section
- `GET /jobs/{id}` - Get job details
- `POST /jobs/` - Create job (admin)
- `PUT /jobs/{id}` - Update job (admin)
- `DELETE /jobs/{id}` - Delete job (admin)
- `GET /jobs/{id}/documents` - Get job documents
- `POST /jobs/{id}/documents` - Upload document (admin)

### Resumes
- `POST /resumes/upload` - Upload resume
- `GET /resumes/` - Get user's resumes
- `DELETE /resumes/{id}` - Delete resume

### Ranking
- `POST /ranking/rank` - Run ranking (admin)
- `GET /ranking/results/{job_id}` - Get ranking results
- `GET /ranking/user/{user_id}` - Get user's results
- `GET /ranking/explanation/{result_id}` - Get RAG explanation

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (`#0ea5e9` to `#0369a1`)
- **Secondary**: Purple gradient (`#a855f7` to `#7e22ce`)
- **Success**: Green (`#10b981`)
- **Warning**: Yellow (`#f59e0b`)
- **Error**: Red (`#ef4444`)

### Components
- **Glass Cards**: `glass-card` class for glassmorphism effect
- **Buttons**: `btn-primary`, `btn-secondary` for gradient buttons
- **Inputs**: `input-field` for consistent form styling

## 📦 Build & Deploy

### Build for Production

```bash
npm run build
npm run start
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your GitHub repo to Vercel for automatic deployments.

## 🔐 Authentication Flow

1. User logs in/registers at `/login`
2. Backend returns JWT token and user object
3. Token stored in `localStorage`
4. Axios interceptor adds token to all requests
5. Role-based redirect (admin → `/admin/jobs`, user → `/jobs`)

## 🎯 User Roles

- **Admin**: Can create/edit/delete jobs, upload documents, run rankings
- **User**: Can browse jobs, upload resumes, view results

## 📝 Notes

- All pages use client-side rendering (`'use client'`)
- Authentication is handled via localStorage (simple but works)
- For production, consider using NextAuth.js with proper session management
- File uploads use FormData with multipart/form-data
- Charts use Recharts for score visualization

## 🚀 Next Steps

1. Update Node.js to version 18+
2. Run `npm install` in the frontend directory
3. Configure `.env.local` with your backend URL
4. Start the dev server with `npm run dev`
5. Build your backend API to match the expected endpoints

## 📞 Support

For issues or questions, refer to the implementation plan or check the backend API documentation.
