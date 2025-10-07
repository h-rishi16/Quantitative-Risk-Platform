"""
Simple FastAPI test application to verify setup
"""

from datetime import datetime
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Quantitative Risk Modeling Platform - Test",
    description="Test API for risk analytics platform",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quantitative Risk Modeling Platform API - Test Version",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "risk_modeling_api"}


@app.post("/api/v1/risk/var")
async def calculate_var_simple():
    """Simple VaR calculation endpoint for testing"""
    # Mock VaR results for testing
    mock_results = {
        "portfolio_id": 1,
        "calculation_date": datetime.now().isoformat(),
        "var_results": [
            {
                "confidence_level": 0.95,
                "var_value": 0.0234,
                "cvar_value": 0.0312,
                "var_dollar": 234000,
                "cvar_dollar": 312000,
            },
            {
                "confidence_level": 0.99,
                "var_value": 0.0456,
                "cvar_value": 0.0587,
                "var_dollar": 456000,
                "cvar_dollar": 587000,
            },
        ],
        "portfolio_statistics": {
            "mean_return": 0.001,
            "std_return": 0.02,
            "skewness": -0.1,
            "kurtosis": 3.2,
            "num_simulations": 10000,
        },
        "method_used": "monte_carlo",
        "parameters": {"num_simulations": 10000, "time_horizon": 252},
    }

    return mock_results


@app.get("/api/v1/portfolio/")
async def get_portfolios():
    """Get portfolio information"""
    return {
        "portfolios": [
            {
                "id": 1,
                "name": "Sample Portfolio",
                "total_value": 10000000,
                "assets": [
                    {"symbol": "AAPL", "weight": 0.4, "value": 4000000},
                    {"symbol": "GOOGL", "weight": 0.3, "value": 3000000},
                    {"symbol": "MSFT", "weight": 0.3, "value": 3000000},
                ],
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "test_api:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
