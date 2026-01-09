#!/usr/bin/env bash
# AgenticOmni Database Setup Script
# Runs Alembic migrations to set up or update the database schema

set -e

echo "======================================================================="
echo "AgenticOmni Database Setup"
echo "======================================================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using .env.example as template."
    echo "   Please create .env from .env.example and configure your settings."
    echo ""
fi

# Check if alembic is installed
if ! command -v alembic &> /dev/null; then
    echo "❌ Error: alembic not found. Install dependencies first:"
    echo "   pip install -e ."
    exit 1
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database migrations completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Start the API server: uvicorn src.api.main:app --reload"
    echo "  2. Access API docs: http://localhost:8000/api/v1/docs"
else
    echo ""
    echo "❌ Migration failed. Check error messages above."
    exit 1
fi
