# Quantitative Risk Modeling Platform

A comprehensive quantitative risk modeling platform for financial institutions built with **Python**, **FastAPI**, and **Streamlit**. This platform provides advanced mathematical models for Value at Risk (VaR), Monte Carlo simulations, and real-time risk monitoring with a simplified, Docker-free architecture.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

## Features

- **Monte Carlo Value at Risk (VaR)** - Advanced simulations with correlation matrices
- **Multiple Confidence Levels** - 90%, 95%, 99%, 99.9% VaR calculations
- **Streamlit Dashboard** - Professional web interface with CSV file upload
- **Interactive Visualizations** - Professional charts using Plotly
- **RESTful API** - FastAPI backend with auto-generated documentation
- **Data Validation** - Comprehensive input validation and error handling
- **Sample Datasets** - Ready-to-use test data for quick start

## Architecture

```
quantitative-risk-platform/
├── backend/                       # FastAPI backend application
│   ├── api/                       # API routes and schemas
│   ├── risk_engines/              # Monte Carlo VaR calculation engines
│   └── data_processing/           # Data validation and processing
├── frontend/                      # Streamlit web application
│   └── app.py                     # Interactive dashboard
├── tests/                         # Test suite (4/4 passing)
├── scripts/                       # Utility and startup scripts
│   ├── simple_main.py             # Backend application runner
│   └── health_check.py            # System health verification
├── deployment/                    # Simple deployment tools
│   └── deploy.sh                  # Automated setup script
├── docs/                          # Documentation
├── sample_data/                   # Test datasets
├── requirements.txt               # Consolidated Python dependencies
├── start.sh                       # Quick start script
└── README.md                      # This file
```

## Quick Start

### Option 1: One-Command Startup
```bash
git clone https://github.com/h-rishi16/Quantitative-Risk-Platform.git
cd Quantitative-Risk-Platform
./start.sh
```

### Option 2: Manual Setup

**Prerequisites:** Python 3.11+, Git

1. **Clone and setup**
```bash
git clone https://github.com/h-rishi16/Quantitative-Risk-Platform.git
cd Quantitative-Risk-Platform
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start services**
```bash
# Terminal 1 - Start backend
python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002

# Terminal 2 - Start frontend  
streamlit run frontend/app.py --server.port 8501
```

3. **Access platform**
- **Web Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8002/docs
- **Health Check**: http://localhost:8002/health

## Technology Stack

**Backend:** FastAPI, NumPy, Pandas, SciPy, Pydantic, Uvicorn  
**Frontend:** Streamlit, Plotly  
**Development:** Python 3.11+, Pytest, GitHub Actions

## Usage

**Web Interface:** Upload portfolio weights CSV and historical returns CSV, configure simulation parameters, run Monte Carlo VaR analysis, view interactive results.

**API Usage:**
```python
import requests

# Run Monte Carlo VaR calculation
payload = {
    "assets": ["AAPL", "GOOGL", "MSFT"],
    "weights": [0.4, 0.3, 0.3],
    "historical_returns": [[0.01, -0.005, 0.008], [-0.012, 0.02, 0.005]],
    "confidence_levels": [0.95, 0.99],
    "num_simulations": 10000,
    "time_horizon": 1
}

response = requests.post("http://localhost:8002/monte_carlo_var", json=payload)
```

## System Health & Testing

### Health Check
```bash
# Comprehensive system verification
python scripts/health_check.py

# Expected output: 6/6 checks passed
# [PASS] Python Environment
# [PASS] Dependencies  
# [PASS] Backend API
# [PASS] Frontend
# [PASS] Test Suite
# [PASS] Deployment Scripts
```

### Testing
```bash
# Run all tests (4/4 passing)
python -m pytest tests/ -v

# Individual test components
python -m pytest tests/test_integration.py -v  # API integration
# Tests cover: health endpoints, VaR calculations, sample data, frontend accessibility
```

## Monte Carlo VaR Implementation

Uses Geometric Brownian Motion (`dS_t = μS_t dt + σS_t dW_t`) for multi-asset portfolio simulations with correlation matrix support. Flexible simulation size (1,000 to 100,000 paths) and time horizons (1 day to 1 year).

**Example Output:**
```
Portfolio Value: $1,000,000 | Simulation Paths: 10,000

Confidence Level    VaR Value    VaR Percentage
95.0%              $23,400      2.34%
99.0%              $45,600      4.56%
99.9%              $67,800      6.78%
```

## API Endpoints

- `GET /health` - System health check
- `GET /sample_data` - Download sample portfolio and returns data  
- `POST /monte_carlo_var` - Calculate Monte Carlo VaR

Interactive documentation: `http://localhost:8002/docs`

## Development

**Philosophy:** Simplicity and reliability over complexity. No Docker dependencies, consolidated requirements, comprehensive testing (4/4 passing), built-in health checks.

**System Requirements:** Python 3.11+, 2GB+ RAM, 100MB storage

**Contributing:** Fork repository, create feature branch, run tests (`python -m pytest tests/ -v`), run health check (`python scripts/health_check.py`), submit pull request.

---

**Quantitative Risk Modeling Platform** - Built for simplicity, reliability, and performance.