#!/bin/bash
# Simple deployment script for Quantitative Risk Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}STEP: $1${NC}"
}

print_success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Check if Python is available
print_step "Checking Python installation..."
if ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if virtual environment exists
print_step "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    print_step "Creating virtual environment..."
    python -m venv .venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment exists"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_step "Installing dependencies..."
pip install -r requirements/requirements.txt
print_success "Dependencies installed"

# Run tests
print_step "Running tests..."
python -m pytest tests/ -v
print_success "Tests passed"

print_success "Deployment preparation complete!"
echo ""
echo "To start the application:"
echo "  1. Backend:  python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002"
echo "  2. Frontend: streamlit run frontend/app.py --server.port 8501"
echo ""
echo "Access URLs:"
echo "  • Frontend Dashboard: http://localhost:8501"
echo "  • Backend API Docs:   http://localhost:8002/docs"
echo "  • API Health Check:   http://localhost:8002/health"