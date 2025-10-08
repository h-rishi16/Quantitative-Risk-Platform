# ✅ Render Deployment Checklist

## Backend Deployment Checklist

### 1. Create Backend Service
- [ ] Go to https://render.com → "New Web Service"
- [ ] Connect GitHub repo: `h-rishi16/Quantitative-Risk-Platform`
- [ ] Set Name: `risk-platform-api`
- [ ] Select Environment: `Python 3`
- [ ] Set Branch: `main`

### 2. Configure Build Settings
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### 3. Set Environment Variables
- [ ] Add: `PYTHONPATH` = `/opt/render/project/src`

### 4. Deploy and Test
- [ ] Click "Create Web Service"
- [ ] Wait for deployment to complete (green status)
- [ ] Copy service URL (e.g., `https://risk-platform-api-xyz.onrender.com`)
- [ ] Test: Visit `https://your-backend-url.onrender.com/health`
- [ ] Should return: `{"status": "healthy", ...}`

## Frontend Deployment Checklist

### 1. Create Frontend Service
- [ ] Create another "New Web Service"
- [ ] Connect same GitHub repo: `h-rishi16/Quantitative-Risk-Platform`
- [ ] Set Name: `risk-platform-frontend`
- [ ] Select Environment: `Python 3`
- [ ] Set Branch: `main`

### 2. Configure Build Settings
- [ ] Build Command: `pip install -r requirements-minimal.txt`
- [ ] Start Command: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### 3. Set Environment Variables
- [ ] Add: `PYTHONPATH` = `/opt/render/project/src`
- [ ] Add: `BACKEND_URL` = `https://your-actual-backend-url.onrender.com`
  - ⚠️ **Use your real backend URL from step 4 above!**

### 4. Deploy and Test
- [ ] Click "Create Web Service"
- [ ] Wait for deployment to complete
- [ ] Visit your frontend URL
- [ ] Should show: "✅ Backend API Connected"
- [ ] Test Monte Carlo simulation

## Common Issues

### ❌ "Build failed - No build command"
**Solution**: Make sure you entered the build command in the Render UI

### ❌ "Backend not connected"
**Solutions**:
- Check `BACKEND_URL` environment variable is correct
- Wait 30 seconds (free tier services sleep)
- Check backend service logs for errors

### ❌ "Import errors"
**Solutions**:
- Verify `PYTHONPATH` is set to `/opt/render/project/src`
- Check requirements files exist in repo

## Success Criteria

### ✅ Backend Working
- Health endpoint returns JSON
- Service shows "green" status in Render
- Logs show "Application startup complete"

### ✅ Frontend Working
- Shows "Backend API Connected" message
- Monte Carlo simulation runs without errors
- All pages load correctly

### ✅ Full Integration
- Frontend can call backend APIs
- Risk calculations complete successfully
- No timeout or connection errors