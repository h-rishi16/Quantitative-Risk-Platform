# Quantitative Risk Modeling Platform

A comprehensive quantitative risk modeling platform for the banking sector built with **Python**, **FastAPI**, and **Streamlit**. This platform provides advanced mathematical models for Value at Risk (VaR), Conditional VaR, Monte Carlo simulations, and real-time risk monitoring.


## Features

### Core Risk Analytics
- **Monte Carlo Value at Risk (VaR)** - Advanced Monte Carlo simulations with correlation matrices
- **Conditional VaR (Expected Shortfall)** - Risk measures beyond standard VaR
- **Portfolio Risk Analytics** - Comprehensive portfolio statistics and risk metrics
- **Multi-Asset Support** - Handle diverse asset classes and portfolios
- **Multiple Confidence Levels** - 90%, 95%, 99%, 99.9% VaR calculations

### Interactive Platform
- **Web-based Interface** - Modern Streamlit dashboard with real-time calculations
- **📁 CSV File Upload** - Easy portfolio data import with validation
- **Interactive Visualizations** - Professional charts using Plotly
- **⚡ RESTful API** - FastAPI backend for programmatic access
- **Real-time Processing** - Live risk calculations and updates

### Data Processing
- **Portfolio Weights Management** - Upload and validate portfolio compositions
- **Historical Returns Analysis** - Process historical market data
- **Data Validation** - Comprehensive input validation and error handling
- **Sample Data** - Ready-to-use test datasets for quick start

## Project Structure

```
quantitative-risk-platform/
├── backend/                       # FastAPI backend application
│   ├── api/                        # API routes and schemas
│   ├── app/                        # Main application setup
│   ├── core/                       # Core configuration
│   ├── data_processing/            # Data processing modules
│   ├── models/                     # Database models
│   ├── risk_engines/               # Risk calculation engines
│   └── utils/                      # Utility functions
├── frontend/                      # Streamlit frontend application
│   ├── components/                 # Reusable UI components
│   ├── pages/                      # Page modules
│   ├── utils/                      # Frontend utilities
│   └── app.py                      # Main Streamlit app
├── tests/                         # Test suite
│   ├── test_api.py                 # API endpoint tests
│   └── test_integration.py         # Integration tests
├── scripts/                       # Utility scripts
│   ├── setup.py                    # Environment setup script
│   └── simple_main.py              # Simple application runner
├── config/                        # Configuration templates
│   ├── .env.example                # Development environment template
│   └── .env.staging.example        # Staging environment template
├── deployment/                    # Deployment scripts
│   └── deploy.sh                   # Simple deployment script
├── docs/                          # Project documentation
│   ├── USER_GUIDE.md               # User guide
│   ├── API.md                      # API documentation
│   └── CHANGELOG.md                # Version history
├── sample_data/                   # Sample datasets for testing
├── .github/                       # GitHub Actions workflows
├── README.md                      # This file
├── requirements.txt                # All Python dependencies
├── pyproject.toml                  # Python project configuration
└── .gitignore                      # Git ignore rules
```

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/h-rishi16/quantitative-risk-platform.git
cd quantitative-risk-platform
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp config/.env.example .env
# Edit .env with your configuration
```

5. **Start the backend API**
```bash
python -m uvicorn scripts.simple_main:app --reload --host 0.0.0.0 --port 8002
```

6. **Start the frontend (in a new terminal)**
```bash
streamlit run frontend/app.py --server.port 8501
```

7. **Access the platform**
- **Web Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8002/docs
- **API Health Check**: http://localhost:8002/health

### Quick Deployment (Alternative)

For automated setup and deployment:

```bash
# Run the deployment script
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

This script will:
- Set up virtual environment
- Install all dependencies
- Run tests to verify setup
- Provide startup instructions

## Configuration

### Environment Setup

1. **Copy environment templates:**
```bash
cp config/.env.example .env
cp config/.env.staging.example .env.staging
```

2. **Edit configuration files with your specific values:**
- Database connection strings
- API keys and secrets
- Environment-specific settings

**Security Note:** Never commit actual `.env` files with real credentials to version control.

### Python Dependencies

**All Dependencies (Consolidated):**
```bash
pip install -r requirements.txt
```

**Using pip-tools (Recommended):**
```bash
pip install pip-tools
pip-compile pyproject.toml
pip-sync requirements.txt
```

## Deployment

### Automated Deployment

Use the deployment script for easy setup:

```bash
# Run the deployment script
./deployment/deploy.sh
```

### Manual Deployment

**Step-by-step setup:**

```bash
# 1. Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp config/.env.example .env
# Edit .env with your settings

# 4. Run tests
python -m pytest tests/ -v

# 5. Start services
python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002 &
streamlit run frontend/app.py --server.port 8501
```

### Prerequisites for Deployment
- Python 3.11 or higher
- Environment files configured (see Configuration section)

## Testing

### Run Tests

**All Tests:**
```bash
python -m pytest tests/ -v
```

**Integration Tests:**
```bash
python tests/test_integration.py
```

**API Tests:**
```bash
python -m pytest tests/test_api.py -v
```

### Test Coverage

The test suite includes:
- API endpoint testing
- Integration testing
- Portfolio risk calculation validation
- Frontend accessibility testing

## Features

### Core Risk Models
- **Value at Risk (VaR)** - Historical, Parametric, and Monte Carlo methods
- **Conditional VaR (CVaR/Expected Shortfall)** - Tail risk measurement
- **Monte Carlo Simulations** - Portfolio risk assessment with multiple stochastic processes
- **Stochastic Differential Equations** - Advanced mathematical modeling
- **Stress Testing** - Scenario-based risk analysis
- **Back-testing** - Model validation and performance assessment

### Risk Analytics
- Real-time portfolio risk monitoring
- Multi-asset correlation analysis
- Volatility modeling and forecasting
- Risk decomposition and attribution
- Regulatory capital calculations
- Performance metrics (Sharpe ratio, Maximum Drawdown, etc.)

### Visualization & Reporting
- Interactive risk dashboards
- Real-time market data integration
- Comprehensive risk reports
- Scenario analysis visualization
- Portfolio optimization tools

## 📁 Project Structure

```
quantitative-risk-platform/
├── backend/                    # FastAPI backend application
│   ├── app/                   # Application configuration
│   ├── core/                  # Core utilities (database, security)
│   ├── models/                # Data models
│   ├── risk_engines/          # Mathematical risk models
│   │   └── monte_carlo.py     # Monte Carlo VaR implementation
│   ├── data_processing/       # Data ingestion and processing
│   ├── api/                   # REST API endpoints
│   └── utils/                 # Utility functions
├── frontend/                  # Streamlit frontend
│   ├── app.py                # Main application
│   ├── pages/                # Individual page components
│   ├── components/           # Reusable UI components
│   └── utils/                # Frontend utilities
├── tests/                    # Test suites
└── scripts/                  # Setup and utility scripts
```

## 🛠️ Technology Stack

### Backend Technologies
- **Python 3.11+**: Core programming language
- **FastAPI**: Modern web framework for building APIs
- **NumPy & SciPy**: Numerical computing foundations
- **Pandas**: Data manipulation and analysis
- **QuantLib**: Comprehensive quantitative finance library
- **PyMC3**: Bayesian modeling and MCMC simulations
- **scikit-learn**: Machine learning algorithms

### Frontend Technologies
- **Streamlit**: Interactive web applications for data science
- **Plotly**: Interactive financial charts and visualizations
- **Altair**: Statistical visualization grammar

### Data & Infrastructure
- **PostgreSQL**: Primary database for structured financial data
- **Redis**: Caching and session management
- **InfluxDB**: Time-series data storage for market data
- **Docker**: Containerization and deployment

## Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Redis server (optional, for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quantitative-risk-platform
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

1. **Start the backend API**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend (in a new terminal)**
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501
   ```

3. **Access the application**
   - Frontend: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## 🧮 Monte Carlo VaR Implementation

The platform includes a comprehensive **Monte Carlo Value at Risk** implementation with the following features:

### Mathematical Foundation
- **Geometric Brownian Motion**: `dS_t = μS_t dt + σS_t dW_t`
- **Mean Reversion Models**: Ornstein-Uhlenbeck process
- **Correlation Handling**: Multi-asset portfolio simulations
- **Multiple Confidence Levels**: 95%, 99%, 99.9% VaR calculations

### Key Features
```python
from backend.risk_engines.monte_carlo import MonteCarloVaR, AssetParameters, SimulationConfig

# Define portfolio assets
assets = [
    AssetParameters("AAPL", 150.0, 0.12, 0.25, 0.4),
    AssetParameters("GOOGL", 2500.0, 0.15, 0.30, 0.3),
    AssetParameters("MSFT", 300.0, 0.10, 0.22, 0.3),
]

# Configure simulation
config = SimulationConfig(
    num_simulations=50000,
    time_horizon=252,
    confidence_levels=[0.95, 0.99, 0.999]
)

# Calculate VaR
mc_var = MonteCarloVaR(assets, correlation_matrix)
results = mc_var.calculate_var(config)
```

### Output Example
```
Value at Risk Estimates:
Confidence    VaR (%)    VaR ($)         CVaR (%)   CVaR ($)
95.0%        0.0234    $234,000        0.0312    $312,000
99.0%        0.0456    $456,000        0.0587    $587,000
99.9%        0.0678    $678,000        0.0834    $834,000
```

## Testing & Validation

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_risk_engines/

# Run with coverage
pytest --cov=backend tests/
```

### Model Validation
- Back-testing framework for VaR model validation
- Statistical tests for model accuracy
- Stress testing under extreme scenarios
- Performance benchmarking against industry standards

## API Endpoints

### Portfolio Management
- `GET /api/v1/portfolio/` - Get portfolio overview
- `POST /api/v1/portfolio/` - Create new portfolio
- `PUT /api/v1/portfolio/{id}` - Update portfolio

### Risk Analysis
- `POST /api/v1/risk/var` - Calculate VaR
- `POST /api/v1/risk/monte-carlo` - Run Monte Carlo simulation
- `POST /api/v1/risk/stress-test` - Perform stress testing

### Market Data
- `GET /api/v1/market/prices` - Get current market prices
- `GET /api/v1/market/historical` - Get historical data

## 🔒 Security & Compliance

- **Data Encryption**: All sensitive data encrypted at rest and in transit
- **Access Control**: Role-based authentication and authorization
- **Audit Logging**: Comprehensive audit trails for regulatory compliance
- **Input Validation**: Robust validation for all user inputs and API calls

## Performance Optimization

- **Parallel Processing**: Multi-threaded Monte Carlo simulations
- **Caching Strategy**: Redis caching for frequently accessed data
- **Database Optimization**: Efficient queries and indexing strategies
- **Memory Management**: Optimized memory usage for large-scale simulations

---

**Built with ❤️ for the financial services industry**