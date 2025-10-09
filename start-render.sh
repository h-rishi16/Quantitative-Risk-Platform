#!/bin/bash
# Render Start Script for Full-Stack Deployment

echo "🚀 Starting Quantitative Risk Platform..."

# Set environment variables
export PYTHONPATH=/opt/render/project/src:$PYTHONPATH

# Start backend API in background
echo "📡 Starting Backend API on port 8002..."
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8002 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if kill -0 $BACKEND_PID > /dev/null 2>&1; then
    echo "✅ Backend API started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Backend API failed to start"
    exit 1
fi

# Start frontend on main port
echo "🖥️  Starting Frontend on port $PORT..."
exec streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true