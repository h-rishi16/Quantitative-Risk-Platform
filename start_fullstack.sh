#!/bin/bash
# Local Full Stack Testing Script

echo "🚀 Starting Quantitative Risk Platform Full Stack"
echo "=============================================="

# Start backend in background
echo "🔧 Starting Backend API..."
cd "$(dirname "$0")"
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8002 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend health
echo "🩺 Testing backend health..."
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "❌ Backend health check failed!"
    kill $BACKEND_PID
    exit 1
fi

# Set environment variable for frontend
export BACKEND_URL="http://localhost:8002"

# Start frontend
echo "🎨 Starting Frontend..."
python -m streamlit run frontend/app.py --server.port 8501

# Cleanup when script exits
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID" EXIT