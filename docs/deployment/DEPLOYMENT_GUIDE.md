# Full Stack Deployment Guide for Render

## Deploy Backend + Frontend on Render

### Step 1: Deploy Backend API

1. **Go to Render Dashboard**: https://render.com
2. **New Web Service** → Connect GitHub repo: `h-rishi16/Quantitative-Risk-Platform`
3. **Configure Backend Service:**
   ```
   Name: risk-platform-api
   Environment: Python 3
   Region: Select your preferred region
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Environment Variables (click "Add Environment Variable"):**
   ```
   Key: PYTHONPATH
   Value: /opt/render/project/src
   ```
5. **Deploy** and wait for build to complete
6. **Copy the service URL** (e.g., `https://risk-platform-api.onrender.com`)

### Step 2: Deploy Frontend

1. **New Web Service** → Same GitHub repo
2. **Configure Frontend Service:**
   ```
   Name: risk-platform-frontend  
   Environment: Python 3
   Region: Same as backend (for faster communication)
   Branch: main
   Build Command: pip install -r requirements-minimal.txt
   Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```
3. **Environment Variables:**
   ```
   Key: PYTHONPATH
   Value: /opt/render/project/src
   
   Key: BACKEND_URL
   Value: https://risk-platform-api.onrender.com
   ```
   WARNING: **Important**: Replace with your actual backend URL from Step 1!

4. **Deploy** and wait for build to complete

### Step 3: Test the Connection

1. Visit your frontend URL
2. Should show "Backend API Connected" if working
3. Try the Monte Carlo simulation to test full functionality

## Alternative: Single Service Deployment

If you prefer one service, use the standalone version:

1. **Web Service Configuration:**
   ```
   Build Command: pip install -r requirements-minimal.txt
   Start Command: streamlit run frontend/app_standalone.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```

## Quick Reference

### Backend URL Examples:
- Render: `https://your-service-name.onrender.com`  
- Railway: `https://your-app-name.railway.app`
- Fly.io: `https://your-app-name.fly.dev`

### Environment Variables to Set:
```
BACKEND_URL=https://your-backend-service-url
PYTHONPATH=/opt/render/project/src
```

## Troubleshooting

### Build Issues

**"No build command specified"**:
- Make sure you enter the build command in the Render UI: `pip install -r requirements.txt`
- For frontend: Use `pip install -r requirements-minimal.txt`

**"Requirements file not found"**:
- Check that `requirements.txt` (backend) or `requirements-minimal.txt` (frontend) exists in repo
- Verify the file path is correct in your build command

**"Python version issues"**:
- Select "Python 3" as environment (Render will use a recent version)
- If needed, add `python_version = "3.11"` to requirements file

### Connection Issues

**"Backend not connected"**:
- Check BACKEND_URL environment variable is set correctly
- Verify backend service is running (green status in Render dashboard)
- Check backend service logs for errors
- Test backend URL directly: `https://your-backend-url.onrender.com/health`

**API timeouts**:
- Increase timeout in frontend (currently 60s for Monte Carlo)
- Check if backend service is sleeping (free tier limitation - takes ~30s to wake up)
- Consider upgrading to paid tier for always-on services

**Import errors**:
- Ensure PYTHONPATH is set to `/opt/render/project/src`
- Check all dependencies are in requirements.txt
- Look for missing imports in service logs

### Free Tier Limitations

**Services sleep after 15 minutes**:
- First request after sleep takes 30+ seconds
- Consider using paid tier for production
- Backend might show "disconnected" until first request wakes it up