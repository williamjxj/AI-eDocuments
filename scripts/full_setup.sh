#!/usr/bin/env bash
# AgenticOmni Full Setup Script
# Complete environment setup from scratch

set -e

echo "======================================================================="
echo "AgenticOmni Full Setup"
echo "======================================================================="
echo ""

# Step 1: Check prerequisites
echo "[1/6] Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found. Please install Python 3.12+."
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Step 2: Create .env file if it doesn't exist
echo "[2/6] Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please review and update .env with your configuration!"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Step 3: Start Docker services
echo "[3/6] Starting Docker services (PostgreSQL + Redis)..."
docker-compose up -d

# Wait for services to be healthy
echo "   Waiting for services to be ready..."
sleep 10

echo "✅ Docker services started"
echo ""

# Step 4: Set up Python virtual environment (if not exists)
echo "[4/6] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Step 5: Install Python dependencies
echo "[5/6] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -e .
echo "✅ Dependencies installed"
echo ""

# Step 6: Run database migrations
echo "[6/6] Running database migrations..."
alembic upgrade head || echo "⚠️  No migrations to run yet (expected for new setup)"
echo ""

echo "======================================================================="
echo "✅ AgenticOmni setup complete!"
echo "======================================================================="
echo ""
echo "Next steps:"
echo "  1. Review and update .env file with your configuration"
echo "  2. Start the API server: ./scripts/run_dev.sh"
echo "  3. Access API docs: http://localhost:8000/api/v1/docs"
echo ""
echo "Useful commands:"
echo "  - Check Docker services: docker-compose ps"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Run migrations: ./scripts/setup_db.sh"
echo ""
