#!/bin/bash

# Quick test script to verify backend starts correctly

echo "🧪 Testing Backend Startup..."
echo ""

# Activate conda ml environment
eval "$(conda shell.bash hook)"
conda activate ml

# Test Python imports
echo "1. Testing Python imports..."
python -c "
import psycopg2
import jose
import passlib
import fastapi
import langchain
import chromadb
import openai
print('✅ All imports successful!')
"

if [ $? -ne 0 ]; then
    echo "❌ Import test failed"
    exit 1
fi

echo ""
echo "2. Testing database connection..."
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        database='ats_db',
        user='ats_user',
        password='ats_password_123'
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"

echo ""
echo "3. Starting backend server..."
echo "   Backend will run on: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
