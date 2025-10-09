#!/bin/bash
# Build Environment Setup Script for Quantitative Risk Platform
# This script sets up the complete development and production environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Main build function  
main() {
    log_header "🚀 Quantitative Risk Platform - Build Environment Setup"
    log_header "============================================================"
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        log_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Environment detection
    if [ "$1" = "production" ] || [ "$1" = "prod" ]; then
        ENVIRONMENT="production"
        log_info "Setting up PRODUCTION environment"
    else
        ENVIRONMENT="development"
        log_info "Setting up DEVELOPMENT environment"
    fi
    
    # Step 1: System Check
    log_header "\n📋 Step 1: System Requirements Check"
    check_system_requirements
    
    # Step 2: Python Environment
    log_header "\n🐍 Step 2: Python Environment Setup"
    setup_python_environment
    
    # Step 3: Dependencies
    log_header "\n📦 Step 3: Installing Dependencies"
    install_dependencies
    
    # Step 4: Environment Variables
    log_header "\n⚙️ Step 4: Environment Configuration"
    setup_environment_variables
    
    # Step 5: Database/Storage Setup
    log_header "\n🗄️ Step 5: Storage Setup"
    setup_storage
    
    # Step 6: Validation
    log_header "\n✅ Step 6: Environment Validation"
    validate_environment
    
    log_header "\n🎉 Build Complete!"
    print_next_steps
}

check_system_requirements() {
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python version: $PYTHON_VERSION"
        
        # Check if Python 3.9+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
            log_success "Python version is compatible (3.9+)"
        else
            log_warning "Python 3.9+ recommended. Current: $PYTHON_VERSION"
        fi
    else
        log_error "Python 3 not found. Please install Python 3.9+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3 available"
    else
        log_error "pip3 not found. Please install pip"
        exit 1
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        log_success "Git available"
    else
        log_warning "Git not found. Version control features may be limited"
    fi
}

setup_python_environment() {
    # Check for virtual environment
    if [ -d ".venv" ]; then
        log_info "Virtual environment found at .venv"
        log_info "Activating virtual environment..."
        source .venv/bin/activate
        log_success "Virtual environment activated"
    else
        log_info "Creating virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate
        log_success "Virtual environment created and activated"
    fi
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel
    log_success "Pip upgraded"
}

install_dependencies() {
    if [ "$ENVIRONMENT" = "production" ]; then
        log_info "Installing production dependencies..."
        pip install -r requirements/requirements-render.txt
    else
        log_info "Installing development dependencies..."
        pip install -r requirements.txt
        
        # Install dev dependencies if available
        if [ -f "requirements/requirements-dev.txt" ]; then
            log_info "Installing development tools..."
            pip install -r requirements/requirements-dev.txt
        fi
    fi
    
    log_success "Dependencies installed"
    
    # List installed packages
    log_info "Installed packages:"
    pip list | head -20
    echo "... (showing first 20 packages)"
}

setup_environment_variables() {
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        log_info "Creating .env file..."
        cat > .env << EOF
# Quantitative Risk Platform Environment Variables

# Application Configuration
ENV=$ENVIRONMENT
DEBUG=true
LOG_LEVEL=INFO

# Backend Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8002
BACKEND_URL=http://localhost:8002

# Frontend Configuration
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501

# Database Configuration (if needed in future)
# DATABASE_URL=sqlite:///./risk_platform.db

# API Keys (add your keys here)
# ALPHA_VANTAGE_API_KEY=your_key_here
# QUANDL_API_KEY=your_key_here

# Security
SECRET_KEY=dev_secret_key_change_in_production

# Python Path
PYTHONPATH=.
EOF
        log_success ".env file created"
    else
        log_info ".env file already exists"
    fi
    
    # Create production .env if in production mode
    if [ "$ENVIRONMENT" = "production" ]; then
        if [ ! -f ".env.production" ]; then
            log_info "Creating production environment template..."
            cat > .env.production << EOF
# Production Environment Variables
ENV=production
DEBUG=false
LOG_LEVEL=WARNING

# Update these for production deployment
BACKEND_URL=https://your-api.onrender.com
SECRET_KEY=change_this_in_production

# Add production API keys
# ALPHA_VANTAGE_API_KEY=prod_key
# QUANDL_API_KEY=prod_key
EOF
            log_success "Production environment template created"
        fi
    fi
}

setup_storage() {
    # Create necessary directories
    log_info "Creating storage directories..."
    
    mkdir -p logs
    mkdir -p temp
    mkdir -p data/uploads
    mkdir -p data/cache
    
    # Create .gitkeep files
    touch logs/.gitkeep
    touch temp/.gitkeep
    touch data/uploads/.gitkeep
    touch data/cache/.gitkeep
    
    log_success "Storage directories created"
}

validate_environment() {
    log_info "Running environment validation..."
    
    # Run the validation script
    if [ -f "validate.py" ]; then
        python validate.py
        if [ $? -eq 0 ]; then
            log_success "Environment validation passed"
        else
            log_error "Environment validation failed"
            exit 1
        fi
    else
        log_warning "validate.py not found, skipping validation"
    fi
    
    # Test basic imports
    log_info "Testing critical imports..."
    python -c "
import streamlit
import fastapi
import numpy
import pandas
import plotly
print('✅ All critical imports successful')
"
    
    if [ $? -eq 0 ]; then
        log_success "Import tests passed"
    else
        log_error "Import tests failed"
        exit 1
    fi
}

print_next_steps() {
    echo ""
    log_header "🎯 Next Steps:"
    echo ""
    
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "📋 Production Deployment:"
        echo "   1. Review and update .env.production with your actual values"
        echo "   2. Choose your deployment configuration:"
        echo "      - Single service: configs/render.yaml"
        echo "      - Two services: configs/render-fullstack.yaml"
        echo "   3. Deploy to Render using your chosen config"
        echo ""
        echo "🔐 Security Checklist:"
        echo "   - Update SECRET_KEY in production"
        echo "   - Add real API keys"
        echo "   - Set DEBUG=false"
    else
        echo "🚀 Local Development:"
        echo "   1. Start the development environment:"
        echo "      ./start.sh"
        echo ""
        echo "   Or start services manually:"
        echo "      # Terminal 1 - Backend:"
        echo "      python -m uvicorn backend.app.main:app --reload --port 8002"
        echo ""
        echo "      # Terminal 2 - Frontend:"
        echo "      streamlit run frontend/app.py"
        echo ""
        echo "🔧 Development Tools:"
        echo "   - Format code: ./format-code.sh"
        echo "   - Run tests: pytest"
        echo "   - Validate: python validate.py"
    fi
    
    echo ""
    log_success "Environment setup complete! 🎉"
}

# Run main function with all arguments
main "$@"