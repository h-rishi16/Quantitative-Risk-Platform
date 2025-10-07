"""
Simplified FastAPI Backend for Monte Carlo VaR Demo
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create FastAPI application
app = FastAPI(
    title="Risk Platform API", description="Monte Carlo VaR API", version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Risk Platform API", "version": "1.0.0", "status": "running"}


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
            {"asset": "MSFT", "weight": 0.3},
        ],
        "sample_returns": [
            {"date": "2024-01-01", "AAPL": 0.01, "GOOGL": -0.005, "MSFT": 0.008},
            {"date": "2024-01-02", "AAPL": -0.012, "GOOGL": 0.02, "MSFT": 0.005},
            {"date": "2024-01-03", "AAPL": 0.008, "GOOGL": 0.015, "MSFT": -0.003},
        ],
    }


# Monte Carlo API imports and routes
try:
    from backend.api.routes.monte_carlo_api import router as monte_carlo_router

    app.include_router(monte_carlo_router, tags=["Monte Carlo"])
    print("✅ Monte Carlo API routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not load Monte Carlo routes: {e}")

    # Fallback: Simple inline Monte Carlo endpoint
    from pydantic import BaseModel
    from typing import List
    import numpy as np

    class MonteCarloRequest(BaseModel):
        assets: List[str]
        weights: List[float]
        historical_returns: List[List[float]]
        confidence_levels: List[float] = [0.95, 0.99]
        num_simulations: int = 10000
        time_horizon: int = 1

    @app.post("/monte_carlo_var")
    async def calculate_monte_carlo_var(request: MonteCarloRequest):
        """Simple Monte Carlo VaR calculation"""
        try:
            # Convert to numpy arrays
            weights = np.array(request.weights)
            returns = np.array(request.historical_returns)

            # Calculate basic statistics
            mean_returns = np.mean(returns, axis=0)
            cov_matrix = np.cov(returns.T)

            # Portfolio statistics
            portfolio_mean = np.dot(weights, mean_returns)
            portfolio_var = np.dot(weights, np.dot(cov_matrix, weights))
            portfolio_std = np.sqrt(portfolio_var)

            # Monte Carlo simulation
            np.random.seed(42)
            simulated_returns = np.random.multivariate_normal(
                mean_returns, cov_matrix, request.num_simulations
            )
            portfolio_returns = np.dot(simulated_returns, weights)

            # Calculate VaR and CVaR
            var_results = []
            for conf_level in request.confidence_levels:
                var_value = np.percentile(portfolio_returns, (1 - conf_level) * 100)
                cvar_mask = portfolio_returns <= var_value
                cvar_value = (
                    np.mean(portfolio_returns[cvar_mask])
                    if np.any(cvar_mask)
                    else var_value
                )

                var_results.append(
                    {
                        "confidence_level": conf_level,
                        "var_value": var_value,
                        "var_dollar": var_value * 10000000,  # Assuming $10M portfolio
                        "cvar_value": cvar_value,
                        "cvar_dollar": cvar_value * 10000000,
                    }
                )

            return {
                "var_results": var_results,
                "portfolio_statistics": {
                    "mean_return": float(portfolio_mean),
                    "std_return": float(portfolio_std),
                    "skewness": float(
                        np.mean(
                            ((portfolio_returns - portfolio_mean) / portfolio_std) ** 3
                        )
                    ),
                    "kurtosis": float(
                        np.mean(
                            ((portfolio_returns - portfolio_mean) / portfolio_std) ** 4
                        )
                    ),
                },
                "simulation_parameters": {
                    "num_simulations": request.num_simulations,
                    "time_horizon": request.time_horizon,
                    "assets": request.assets,
                },
            }
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
