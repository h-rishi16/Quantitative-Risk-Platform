# Render Deployment Instructions

## Two-Service Deployment (Recommended)

### Backend Service Configuration:
Name: risk-platform-api
Build Command: python --version && pip install --upgrade pip setuptools wheel && pip install -r requirements/requirements-render.txt
Start Command: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  PYTHONPATH=/opt/render/project/src

### Frontend Service Configuration:
Name: risk-platform-frontend  
Build Command: python --version && pip install --upgrade pip setuptools wheel && pip install -r requirements/requirements-render.txt
Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
Environment Variables:
  PYTHONPATH=/opt/render/project/src
  BACKEND_URL=https://risk-platform-api.onrender.com

## Single-Service Deployment

### Service Configuration:
Name: quantitative-risk-platform
Build Command: python --version && pip install --upgrade pip setuptools wheel && pip install -r requirements/requirements-render.txt  
Start Command: ./start-render.sh
Environment Variables:
  PYTHONPATH=/opt/render/project/src
  BACKEND_URL=http://localhost:8002

## Health Check URLs:
- Backend: https://risk-platform-api.onrender.com/health
- Frontend: https://risk-platform-frontend.onrender.com
- API Docs: https://risk-platform-api.onrender.com/docs

## Deployment Steps:
1. Push code to GitHub
2. Connect repository in Render
3. Use configurations above
4. Deploy services (backend first for two-service setup)
5. Update BACKEND_URL in frontend to actual backend URL
6. Test application

## Cost Estimate:
- Two services: ~$14/month (2 x $7/month)
- Single service: ~$7/month
- Free tier: Available with limitations