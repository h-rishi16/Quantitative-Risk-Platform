# Requirements

This directory contains all Python package requirements for the Quantitative Risk Modeling Platform.

## Files

- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development and testing dependencies

## Installation

### Production Environment
```bash
pip install -r requirements/requirements.txt
```

### Development Environment
```bash
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt
```

### Using pip-tools (Recommended)
```bash
# Install pip-tools
pip install pip-tools

# Generate requirements from pyproject.toml
pip-compile pyproject.toml

# Install requirements
pip-sync requirements.txt
```

## Package Categories

### Core Dependencies (requirements.txt)
- FastAPI - Web framework
- Streamlit - Frontend framework
- NumPy, SciPy - Mathematical computing
- Pandas - Data manipulation
- Plotly - Visualization
- SQLAlchemy - Database ORM
- Redis - Caching
- Uvicorn - ASGI server

### Development Dependencies (requirements-dev.txt)
- pytest - Testing framework
- mypy - Type checking
- black - Code formatting
- isort - Import sorting
- pre-commit - Git hooks