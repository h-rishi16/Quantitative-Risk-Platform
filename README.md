# 🏦 Quantitative Risk Modeling Platform

A comprehensive quantitative risk modeling platform for the banking sector built with Python, FastAPI, and Streamlit.

## 🚀 Quick Start

### Full-Stack Mode (Production Ready)
```bash
# Local Development - Terminal 1 (Backend)
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8002

# Local Development - Terminal 2 (Frontend)  
streamlit run frontend/app.py
```
*Complete system with FastAPI backend and Streamlit frontend*

## 📋 Features

- **Value at Risk (VaR)** calculations using multiple methodologies
- **Conditional VaR (Expected Shortfall)** analysis
- **Monte Carlo simulations** for portfolio risk assessment
- **Stochastic Differential Equations** modeling
- **Real-time risk monitoring** and visualization
- **Stress testing** and scenario analysis

## 🏗️ Architecture

- **Backend**: FastAPI with advanced mathematical models
- **Frontend**: Streamlit for interactive risk dashboards
- **Database**: PostgreSQL for data storage, Redis for caching
- **Mathematical Libraries**: NumPy, SciPy, QuantLib, PyMC3

## 🔧 Development Setup

### Prerequisites
- Python 3.13.1
- Git

### Installation
```bash
git clone https://github.com/h-rishi16/Quantitative-Risk-Platform.git
cd Quantitative-Risk-Platform
pip install -r requirements.txt
```

### Quick Start Options
- **Full Development**: `pip install -r requirements.txt`
- **Production Deployment**: `pip install -r requirements/requirements-render.txt`
- **Minimal Setup**: `pip install -r requirements/requirements-minimal.txt`

### Code Quality (Important!)
Before committing any code:
```bash
./format-code.sh
git add .
git commit -m "Your message"
git push origin main
```

## 📦 Deployment

### Render Full-Stack Deployment
Choose one of these configurations:

**Option A: Single Service (Simpler)**
- Use `configs/render.yaml` or `configs/render-stable.yaml`
- Runs both backend and frontend in one service
- More cost-effective

**Option B: Two Services (More Scalable)**
- Use `configs/render-fullstack.yaml`
- Separate backend API and frontend services
- Better for production load

**Environment Variables:**
- `PYTHONPATH`: `/opt/render/project/src`
- `BACKEND_URL`: Set automatically based on your deployment choice

### Other Platforms
- **HuggingFace**: Use `requirements/requirements_hf.txt`
- **Minimal Setup**: Use `requirements/requirements-minimal.txt`

## 📁 Project Structure
```
├── backend/           # FastAPI backend services
├── frontend/          # Streamlit frontend application  
├── configs/           # Deployment configurations
│   ├── render.yaml    # Main Render config
│   └── render-stable.yaml # Stable deployment config
├── docs/              # Documentation
│   ├── deployment/    # Deployment guides
│   ├── API.md         # API documentation
│   └── USER_GUIDE.md  # User guide
├── requirements/      # Dependency management
│   ├── requirements-render.txt # Production
│   ├── requirements-minimal.txt # Lightweight
│   └── requirements_hf.txt # HuggingFace
├── scripts/           # Utility scripts
├── tests/             # Test suites
└── sample_data/       # Sample datasets
```

## 📚 Documentation

- [`docs/deployment/DEPLOYMENT_GUIDE.md`](docs/deployment/DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [`docs/CODE_QUALITY_GUIDE.md`](docs/CODE_QUALITY_GUIDE.md) - Development workflow
- [`docs/deployment/ENVIRONMENT_VARIABLES.md`](docs/deployment/ENVIRONMENT_VARIABLES.md) - Environment setup
- [`docs/GIT_ALIASES.md`](docs/GIT_ALIASES.md) - Helpful git shortcuts
- [`docs/API.md`](docs/API.md) - API reference
- [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) - User guide

## 🧪 Testing

```bash
pytest --cov=backend --cov=frontend
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Run code formatting**: `./format-code.sh`
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

---

**Built with ❤️ for quantitative finance and risk management**