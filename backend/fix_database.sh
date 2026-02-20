#!/bin/bash

echo "🔧 Fixing PostgreSQL Database Setup..."
echo ""

# Drop and recreate the database and user properly
sudo -u postgres psql << 'EOF'
-- Drop existing database and user if they exist
DROP DATABASE IF EXISTS ats_db;
DROP USER IF EXISTS ats_user;

-- Create user with password
CREATE USER ats_user WITH PASSWORD 'ats_password_123';

-- Create database
CREATE DATABASE ats_db OWNER ats_user;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE ats_db TO ats_user;

-- Connect to the database and grant schema privileges
\c ats_db
GRANT ALL ON SCHEMA public TO ats_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ats_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ats_user;

\q
EOF

echo ""
echo "✅ Database setup complete!"
echo ""
echo "Testing connection..."
PGPASSWORD='ats_password_123' psql -h localhost -U ats_user -d ats_db -c "SELECT version();"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Connection successful!"
    echo ""
    echo "Now run:"
    echo "  conda activate ml"
    echo "  python init_db.py"
    echo "  python create_admin.py"
else
    echo ""
    echo "❌ Connection failed. Please check the error above."
fi
