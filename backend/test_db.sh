#!/bin/bash

echo "Testing PostgreSQL connection..."
echo ""

# Test 1: Check if PostgreSQL is running
echo "1. Checking if PostgreSQL is running..."
sudo systemctl status postgresql | grep "Active:"

echo ""

# Test 2: Try to connect as postgres user
echo "2. Testing connection as postgres user..."
sudo -u postgres psql -c "SELECT version();" | head -n 3

echo ""

# Test 3: List existing databases
echo "3. Listing existing databases..."
sudo -u postgres psql -c "\l" | grep ats_db

echo ""

# Test 4: List existing users
echo "4. Listing existing users..."
sudo -u postgres psql -c "\du" | grep ats_user

echo ""
echo "Now let's create the database properly..."
echo ""

# Create database and user
sudo -u postgres psql << 'EOSQL'
-- Drop if exists
DROP DATABASE IF EXISTS ats_db;
DROP ROLE IF EXISTS ats_user;

-- Create role with login
CREATE ROLE ats_user WITH LOGIN PASSWORD 'ats_password_123';

-- Create database
CREATE DATABASE ats_db WITH OWNER ats_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ats_db TO ats_user;

-- Connect and grant schema privileges
\c ats_db
GRANT ALL ON SCHEMA public TO ats_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ats_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ats_user;

-- Show result
\du ats_user
\l ats_db
EOSQL

echo ""
echo "Testing connection with new user..."
PGPASSWORD='ats_password_123' psql -h localhost -U ats_user -d ats_db -c "SELECT 'Connection successful!' as status;"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Database is ready!"
    echo ""
    echo "Now you can run:"
    echo "  conda activate ml"
    echo "  python init_db.py"
    echo "  python create_admin.py"
else
    echo ""
    echo "❌ Connection test failed"
fi
