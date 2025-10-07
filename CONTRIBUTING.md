# Contributing to Quantitative Risk Modeling Platform

We love your input! We want to make contributing to the Quantitative Risk Modeling Platform as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Update documentation as needed.
6. Issue that pull request!

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Git
- Docker (optional but recommended)

### Local Development

1. **Clone your fork**
```bash
git clone https://github.com/yourusername/quantitative-risk-platform.git
cd quantitative-risk-platform
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install development dependencies**
```bash
pip install -r requirements-dev.txt
```

4. **Install pre-commit hooks**
```bash
pre-commit install
```

5. **Run tests**
```bash
pytest
```

6. **Start development servers**
```bash
# Backend (Terminal 1)
python -m uvicorn simple_main:app --reload --port 8002

# Frontend (Terminal 2)
streamlit run frontend/app.py --server.port 8501
```

## Code Style

We use several tools to maintain code quality:

### Formatting
- **Black**: Code formatting
- **isort**: Import sorting

```bash
# Format code
black .
isort .
```

### Linting
- **flake8**: Style guide enforcement
- **pylint**: Code analysis
- **mypy**: Type checking

```bash
# Lint code
flake8 .
pylint backend/ frontend/
mypy backend/ --ignore-missing-imports
```

### Running All Checks
```bash
# Run all quality checks
black --check .
isort --check-only .
flake8 .
pylint backend/ frontend/
mypy backend/ --ignore-missing-imports
pytest --cov=backend --cov=frontend
```

## Testing

### Test Structure
```
tests/
├── unit/              # Unit tests
│   ├── test_monte_carlo.py
│   └── test_data_processor.py
├── integration/       # Integration tests
│   ├── test_api.py
│   └── test_workflow.py
└── fixtures/          # Test data and fixtures
    ├── sample_portfolio.csv
    └── sample_returns.csv
```

### Writing Tests

#### Unit Tests
```python
import pytest
from backend.risk_engines.monte_carlo import MonteCarloVaR

def test_monte_carlo_calculation():
    # Test Monte Carlo VaR calculation
    assets = ["AAPL", "GOOGL"]
    weights = [0.6, 0.4]
    returns = [[0.01, -0.005], [-0.02, 0.015]]
    
    var_engine = MonteCarloVaR(assets, weights, returns)
    results = var_engine.calculate_var([0.95], 1000, 1)
    
    assert len(results) == 1
    assert 0 < results[0]['confidence_level'] < 1
```

#### Integration Tests
```python
import pytest
from fastapi.testclient import TestClient
from simple_main import app

client = TestClient(app)

def test_monte_carlo_api():
    data = {
        "assets": ["AAPL", "GOOGL"],
        "weights": [0.6, 0.4],
        "historical_returns": [[0.01, -0.005], [-0.02, 0.015]],
        "confidence_levels": [0.95]
    }
    
    response = client.post("/monte_carlo_var", json=data)
    assert response.status_code == 200
    assert "var_results" in response.json()
```

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_monte_carlo.py

# With coverage
pytest --cov=backend --cov=frontend --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Architecture Guidelines

### Backend Structure
```
backend/
├── api/
│   ├── routes/        # API endpoints
│   └── schemas/       # Pydantic models
├── risk_engines/      # Risk calculation engines
├── data_processing/   # Data handling utilities
├── models/           # Data models
└── utils/            # Helper functions
```

### Adding New Features

#### 1. Risk Models
Create new risk calculation engines in `backend/risk_engines/`:
```python
# backend/risk_engines/new_model.py
class NewRiskModel:
    def __init__(self, params):
        self.params = params
    
    def calculate_risk(self):
        # Implementation
        pass
```

#### 2. API Endpoints
Add new endpoints in `backend/api/routes/`:
```python
# backend/api/routes/new_endpoint.py
from fastapi import APIRouter
from ..schemas.requests import NewRequest
from ..schemas.responses import NewResponse

router = APIRouter()

@router.post("/new_endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    # Implementation
    pass
```

#### 3. Frontend Features
Add new Streamlit components in `frontend/`:
```python
# frontend/new_feature.py
import streamlit as st

def new_feature_page():
    st.header("New Feature")
    # Implementation
    pass
```

## Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google docstring format
- Include type hints for all functions

```python
def calculate_var(
    returns: np.ndarray, 
    confidence_level: float,
    method: str = "monte_carlo"
) -> Dict[str, float]:
    """Calculate Value at Risk using specified method.
    
    Args:
        returns: Historical return data
        confidence_level: VaR confidence level (0-1)
        method: Calculation method
        
    Returns:
        Dictionary containing VaR results
        
    Raises:
        ValueError: If confidence_level is not between 0 and 1
    """
    pass
```

### API Documentation
- Use Pydantic models for request/response schemas
- Add descriptions to all fields
- Include examples in docstrings

## Git Workflow

### Branch Naming
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes  
- `hotfix/critical-fix` - Critical fixes
- `docs/documentation-update` - Documentation changes

### Commit Messages
Follow conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(api): add new VaR calculation endpoint
fix(frontend): resolve file upload validation issue
docs(readme): update installation instructions
test(monte_carlo): add unit tests for correlation matrix
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for changes
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Issue Reporting

### Bug Reports
Use the bug report template with:
- Environment details (OS, Python version, etc.)
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Error messages/logs

### Feature Requests
Use the feature request template with:
- Problem description
- Proposed solution
- Alternative solutions considered
- Additional context

## Security

### Reporting Security Issues
**Do not report security vulnerabilities publicly.** 

Send security reports to: security@riskplatform.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fixes (if any)

### Security Best Practices
- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Follow OWASP guidelines

## Performance Guidelines

### Code Performance
- Profile code for bottlenecks
- Use NumPy for numerical operations
- Implement caching where appropriate
- Consider memory usage for large datasets

### Testing Performance
```python
import time
import pytest

def test_monte_carlo_performance():
    start_time = time.time()
    # Run calculation
    end_time = time.time()
    
    # Should complete within 5 seconds
    assert end_time - start_time < 5.0
```

## Release Process

### Version Numbering
We use Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Tag created and pushed
- [ ] Release notes prepared

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion on GitHub
- Reach out to maintainers

Thank you for contributing!