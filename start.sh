#!/bin/bash

# Quick Start Script for Quantitative Risk Platform
# This script starts both backend and frontend services

echo "Starting Quantitative Risk Platform..."
echo "======================================"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "[ERROR] Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "Shutting down services..."
    jobs -p | xargs -r kill
    exit 0
}
trap cleanup INT TERM

# Start backend
echo "[INFO] Starting FastAPI backend on port 8002..."
python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "[INFO] Waiting for backend to start..."
sleep 5

# Test backend health
if curl -s -f http://localhost:8002/health > /dev/null; then
    echo "[SUCCESS] Backend started successfully"
else
    echo "[ERROR] Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "[INFO] Starting Streamlit frontend on port 8501..."
streamlit run frontend/app.py --server.port 8501 --browser.gatherUsageStats false &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 3

echo ""
echo "======================================"
echo "Services started successfully!"
echo "======================================"
echo "Backend API:  http://localhost:8002"
echo "Frontend App: http://localhost:8501"
echo "API Docs:     http://localhost:8002/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "======================================"

# Wait for user interrupt
wait