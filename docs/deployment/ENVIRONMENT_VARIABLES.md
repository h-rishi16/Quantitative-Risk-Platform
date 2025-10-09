# Environment Variables Configuration Guide

## Required Environment Variables

### Frontend Service (Streamlit)
```
PYTHONPATH=/opt/render/project/src
BACKEND_URL=https://your-backend-service-name.onrender.com
```

### Backend Service (FastAPI)
```
PYTHONPATH=/opt/render/project/src
PORT=$PORT
```

## Setting Environment Variables in Render

### Option 1: Via Render Dashboard UI
1. **During Initial Setup:**
   - In "Environment Variables" section
   - Click "Add Environment Variable"
   - Enter key-value pairs

2. **After Service Creation:**
   - Go to service dashboard
   - Click "Environment" tab
   - Click "Add Environment Variable"

### Option 2: Via render.yaml (Blueprint)
Environment variables are already configured in the YAML files:

#### Single Service (render.yaml):
```yaml
envVars:
  - key: PYTHONPATH
    value: /opt/render/project/src
  - key: BACKEND_URL
    value: https://your-backend-url.onrender.com
```

#### Full Stack (render-fullstack.yaml):
```yaml
# Backend service
envVars:
  - key: PYTHONPATH
    value: /opt/render/project/src

# Frontend service  
envVars:
  - key: PYTHONPATH
    value: /opt/render/project/src
  - key: BACKEND_URL
    value: https://risk-platform-api.onrender.com
```

## Environment Variable Values to Use

### For Frontend-Only Deployment:
- **PYTHONPATH**: `/opt/render/project/src`
- **BACKEND_URL**: `https://your-backend-service-name.onrender.com`

### For Full-Stack Deployment:
- **Backend PYTHONPATH**: `/opt/render/project/src`
- **Frontend PYTHONPATH**: `/opt/render/project/src`  
- **Frontend BACKEND_URL**: `https://risk-platform-api.onrender.com`

## Important Notes

1. **BACKEND_URL Format**: Must include `https://` and `.onrender.com`
2. **Service Names**: Use the exact service name you create in Render
3. **PYTHONPATH**: Always use `/opt/render/project/src` for Render deployments
4. **PORT**: Automatically set by Render, use `$PORT` in start commands

## Troubleshooting

### Common Issues:
- **Backend not connected**: Check BACKEND_URL is correct and backend service is running
- **Module import errors**: Verify PYTHONPATH is set to `/opt/render/project/src`
- **Service not starting**: Ensure all required environment variables are set

### Testing Environment Variables:
Add this to your Streamlit app to debug:
```python
import os
st.write(f"Backend URL: {os.getenv('BACKEND_URL')}")
st.write(f"Python Path: {os.getenv('PYTHONPATH')}")
```