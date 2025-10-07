"""
FastAPI Backend Application for Quantitative Risk Modeling Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from contextlib import asynccontextmanager
import logging

# Import routes
from backend.api.routes import portfolio, risk_analysis, market_data, monte_carlo_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Quantitative Risk Modeling Platform API")
    yield
    logger.info("Shutting down API")

# Create FastAPI application
app = FastAPI(
    title="Quantitative Risk Modeling Platform",
    description="Advanced risk analytics and portfolio management API for banking sector",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio"])
app.include_router(risk_analysis.router, prefix="/api/v1/risk", tags=["Risk Analysis"])
app.include_router(market_data.router, prefix="/api/v1/market", tags=["Market Data"])
app.include_router(monte_carlo_api.router, tags=["Monte Carlo"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quantitative Risk Modeling Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/sample_data")
async def get_sample_data():
    """Get sample data for testing"""
    return {
        "portfolio_weights": [
            {"asset": "AAPL", "weight": 0.4},
            {"asset": "GOOGL", "weight": 0.3},
            {"asset": "MSFT", "weight": 0.3}
        ],
        "sample_returns": [
            {"date": "2024-01-01", "AAPL": 0.01, "GOOGL": -0.005, "MSFT": 0.008},
            {"date": "2024-01-02", "AAPL": -0.012, "GOOGL": 0.02, "MSFT": 0.005},
            {"date": "2024-01-03", "AAPL": 0.008, "GOOGL": 0.015, "MSFT": -0.003}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )