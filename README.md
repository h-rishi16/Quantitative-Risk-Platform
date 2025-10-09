# 🏦 Quantitative Risk Modeling Platform

A comprehensive quantitative risk modeling platform for the banking sector built with Python, FastAPI, and Streamlit. This platform provides advanced risk analytics, Monte Carlo simulations, and portfolio management tools used in modern quantitative finance.

## 🌐 **Live Application**

### **[🚀 Try the Live Demo](https://risk-platform-frontend.onrender.com)**

Experience the full quantitative risk modeling platform featuring:
- **Portfolio Risk Analysis** with real-time calculations
- **Monte Carlo VaR Simulations** with customizable parameters  
- **Interactive Visualizations** and risk dashboards
- **CSV File Upload** for portfolio data analysis
- **Stress Testing** and scenario analysis tools

### **[📊 API Documentation](https://risk-platform-api.onrender.com/docs)**
Complete FastAPI documentation with interactive endpoint testing

---

## 🎯 **Key Features**

### **Risk Analytics Engine**
- **Value at Risk (VaR)** calculations using multiple methodologies
- **Conditional VaR (Expected Shortfall)** analysis  
- **Monte Carlo simulations** for portfolio risk assessment
- **Stochastic Differential Equations** modeling
- **Stress testing** and scenario analysis

### **Interactive Frontend**
- **Real-time risk monitoring** and visualization
- **Portfolio composition** analysis and optimization
- **Dynamic charting** with Plotly integration
- **File upload** support for CSV portfolio data
- **Responsive design** optimized for financial workflows

### **Robust Backend API**
- **FastAPI** with automatic OpenAPI documentation
- **RESTful endpoints** for all risk calculations
- **Data validation** with Pydantic models
- **Health monitoring** and error handling
- **CORS support** for web integration

## 📋 Features

- **Value at Risk (VaR)** calculations using multiple methodologies
- **Conditional VaR (Expected Shortfall)** analysis
- **Monte Carlo simulations** for portfolio risk assessment
- **Stochastic Differential Equations** modeling
- **Real-time risk monitoring** and visualization
- **Stress testing** and scenario analysis

## 🏗️ **Architecture**

### **Technology Stack**
- **Backend**: FastAPI with advanced mathematical models
- **Frontend**: Streamlit for interactive risk dashboards  
- **Deployment**: Render (production-ready cloud platform)
- **Mathematical Libraries**: NumPy, SciPy, Pandas, Plotly
- **Python Version**: 3.13.1 (latest stable)

### **System Design**
- **Microservices Architecture** with separate API and frontend services
- **RESTful API** design with comprehensive documentation
- **Real-time calculations** with optimized numerical algorithms
- **Scalable deployment** on cloud infrastructure
- **Professional logging** and error handling

## 🚀 **Local Development**

### **Prerequisites**
- Python 3.9+ (3.13.1 recommended)
- Git
- 8GB+ RAM recommended for Monte Carlo simulations

### **Quick Setup**
```bash
# Clone the repository
git clone https://github.com/h-rishi16/Quantitative-Risk-Platform.git
cd Quantitative-Risk-Platform

# Install dependencies
pip install -r requirements.txt

# Start backend (Terminal 1)
python -m uvicorn backend.app.main:app --reload --port 8002

# Start frontend (Terminal 2)  
streamlit run frontend/app.py
```

### **Development Options**
- **Full Development**: `pip install -r requirements.txt`
- **Production Build**: `pip install -r requirements/requirements-render.txt`
- **Minimal Setup**: `pip install -r requirements/requirements-minimal.txt`

### **Code Quality**
Automated formatting and validation:
```bash
# Format code before committing
./format-code.sh

# Validate environment
python validate.py

# Commit changes
git add .
git commit -m "Your message"
git push origin main
```

## 🌐 **Production Deployment**

### **Current Live Deployment**
- **Platform**: Render (Professional Cloud Hosting)
- **Frontend**: https://risk-platform-frontend.onrender.com
- **Backend API**: https://risk-platform-api.onrender.com
- **Architecture**: Two-service microservices deployment

### **Deployment Configurations**

**✅ Two Services (Current Production Setup)**
- **API Service**: Dedicated FastAPI backend
- **Frontend Service**: Streamlit user interface
- **Benefits**: Better scaling, resource isolation, professional setup

**Alternative Configurations Available:**
- **Single Service**: `configs/render.yaml` (cost-effective)
- **Stable Build**: `configs/render-stable.yaml` (enhanced reliability)
- **Docker**: Ready for containerized deployment

### **Environment Configuration**
```yaml
Production Environment Variables:
- PYTHONPATH: /opt/render/project/src
- BACKEND_URL: https://risk-platform-api.onrender.com
- Python Runtime: 3.13.1
```

### **Other Platform Support**
- **Docker**: Container-ready configurations
- **Heroku**: Compatible with minor config changes
- **AWS/GCP**: Scalable cloud deployment options## 📁 Project Structure
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