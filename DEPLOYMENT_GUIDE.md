# Full Stack Deployment Guide for Render

## 🚀 Deploy Backend + Frontend on Render

### Step 1: Deploy Backend API

1. **Go to Render Dashboard**: https://render.com
2. **New Web Service** → Connect GitHub repo: `h-rishi16/Quantitative-Risk-Platform`
3. **Configure Backend Service:**
   ```
   Name: risk-platform-api
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Environment Variables:**
   ```
   PYTHONPATH = /opt/render/project/src
   ```
5. **Deploy** and note the URL (e.g., `https://risk-platform-api.onrender.com`)

### Step 2: Deploy Frontend

1. **New Web Service** → Same GitHub repo
2. **Configure Frontend Service:**
   ```
   Name: risk-platform-frontend  
   Environment: Python
   Build Command: pip install -r requirements-minimal.txt
   Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```
3. **Environment Variables:**
   ```
   PYTHONPATH = /opt/render/project/src
   BACKEND_URL = https://risk-platform-api.onrender.com
   ```
   ⚠️ **Important**: Replace with your actual backend URL from Step 1!

### Step 3: Test the Connection

1. Visit your frontend URL
2. Should show "✅ Backend API Connected" if working
3. Try the Monte Carlo simulation to test full functionality

## 🎯 Alternative: Single Service Deployment

If you prefer one service, use the standalone version:

1. **Web Service Configuration:**
   ```
   Build Command: pip install -r requirements-minimal.txt
   Start Command: streamlit run frontend/app_standalone.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```

## 📋 Quick Reference

### Backend URL Examples:
- Render: `https://your-service-name.onrender.com`  
- Railway: `https://your-app-name.railway.app`
- Fly.io: `https://your-app-name.fly.dev`

### Environment Variables to Set:
```
BACKEND_URL=https://your-backend-service-url
PYTHONPATH=/opt/render/project/src
```

## 🛠️ Troubleshooting

**"Backend not connected"**:
- Check BACKEND_URL environment variable
- Verify backend service is running
- Check backend service logs

**API timeouts**:
- Increase timeout in frontend (currently 60s)
- Check if backend service is sleeping (free tier limitation)

**Import errors**:
- Ensure PYTHONPATH is set correctly
- Check all dependencies are in requirements.txt