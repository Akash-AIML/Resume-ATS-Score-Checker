#!/bin/bash

echo "🔧 Fixing Python environment issue..."
echo ""

# Deactivate any active venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivating venv: $VIRTUAL_ENV"
    deactivate 2>/dev/null || true
fi

# Activate conda ml environment
echo "Activating conda ml environment..."
eval "$(conda shell.bash hook)"
conda activate ml

# Verify which python is being used
echo ""
echo "Python location: $(which python)"
echo "Python version: $(python --version)"
echo ""

# Test database connection with Python
echo "Testing database connection with Python..."
python << 'EOPY'
import psycopg2
try:
    conn = psycopg2.connect(
        host="localhost",
        database="ats_db",
        user="ats_user",
        password="ats_password_123"
    )
    print("✅ Python can connect to database!")
    conn.close()
except Exception as e:
    print(f"❌ Python connection failed: {e}")
EOPY

echo ""
echo "Now running init_db.py..."
python init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database initialized!"
    echo ""
    echo "Creating admin user..."
    python create_admin.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "To start the backend:"
        echo "  conda activate ml"
        echo "  uvicorn main:app --reload"
    fi
else
    echo "❌ Database initialization failed"
fi
