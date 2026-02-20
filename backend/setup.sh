#!/bin/bash

echo "🚀 Setting up ATS Resume Analyzer Backend (using conda ml environment)..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Create PostgreSQL database
echo -e "${YELLOW}Step 1: Creating PostgreSQL database...${NC}"
sudo -u postgres psql << EOF
CREATE DATABASE ats_db;
CREATE USER ats_user WITH PASSWORD 'ats_password_123';
GRANT ALL PRIVILEGES ON DATABASE ats_db TO ats_user;
ALTER DATABASE ats_db OWNER TO ats_user;
\q
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database created successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Database might already exist (this is OK)${NC}"
fi

echo ""

# Step 2: Activate conda environment and install missing dependencies
echo -e "${YELLOW}Step 2: Installing missing dependencies in conda ml environment...${NC}"
cd /home/akash/Resume_Score/backend

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate ml

# Install only the backend-specific dependencies that might be missing
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 python-multipart==0.0.6
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
pip install pydantic==2.5.3 pydantic-settings==2.1.0
pip install pdfplumber==0.10.3 PyPDF2==3.0.1
pip install langchain==0.0.354 langchain-community==0.0.20 langchain-openai==0.0.6
pip install chromadb==0.4.22 tiktoken==0.5.2
pip install psycopg2-binary==2.9.9 sqlalchemy==2.0.25
pip install google-auth==2.27.0 google-auth-oauthlib==1.2.0
pip install python-dotenv==1.0.0

echo -e "${GREEN}✅ Dependencies installed!${NC}"

echo ""

# Step 3: Initialize database
echo -e "${YELLOW}Step 3: Initializing database tables...${NC}"
python init_db.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database initialized!${NC}"
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi

echo ""

# Step 4: Create admin user
echo -e "${YELLOW}Step 4: Creating admin user...${NC}"
python create_admin.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Admin user created!${NC}"
else
    echo -e "${YELLOW}⚠️  Admin user might already exist (this is OK)${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Backend setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Admin Credentials:${NC}"
echo "  Email: admin@ats.com"
echo "  Password: admin123"
echo ""
echo -e "${YELLOW}To start the backend:${NC}"
echo "  1. Make sure your OpenAI API key is in .env file"
echo "  2. Run: conda activate ml"
echo "  3. Run: uvicorn main:app --reload"
echo ""
echo -e "${GREEN}Backend will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}API Docs: http://localhost:8000/docs${NC}"
