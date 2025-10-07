"""
Updated API endpoints that accept portfolio data uploads
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import numpy as np
import json
import logging
from io import StringIO

# Import our data processing and risk calculation modules
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.data_processing.data_processor import DataProcessor, validate_api_request
from backend.risk_engines.monte_carlo import MonteCarloVaR, SimulationConfig, VaRResults

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for API requests
from pydantic import BaseModel


class MonteCarloRequest(BaseModel):
    """Request model for Monte Carlo VaR calculation with uploaded data"""

    assets: List[str]
    weights: List[float]
    historical_returns: List[List[float]]  # Matrix: [observations][assets]
    confidence_levels: List[float] = [0.95, 0.99]
    num_simulations: int = 10000
    time_horizon: int = 1  # days
    correlation_matrix: Optional[List[List[float]]] = None


class VaRResponse(BaseModel):
    """Response model for VaR calculations"""

    portfolio_id: str
    calculation_date: str
    method: str
    assets: List[str]
    weights: List[float]
    var_results: List[Dict]
    portfolio_statistics: Dict
    simulation_parameters: Dict


@router.post("/monte_carlo_var", response_model=VaRResponse)
async def calculate_monte_carlo_var(request: MonteCarloRequest):
    """
    Calculate Monte Carlo VaR from uploaded portfolio data

    This endpoint accepts portfolio weights and historical returns data
    and returns comprehensive risk metrics.
    """
    try:
        logger.info(f"Calculating Monte Carlo VaR for {len(request.assets)} assets")

        # Validate request data
        is_valid, error_msg = validate_api_request(
            {
                "weights": request.weights,
                "historical_returns": request.historical_returns,
                "assets": request.assets,
            }
        )

        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Convert data to numpy arrays
        weights = np.array(request.weights)
        returns_matrix = np.array(request.historical_returns)

        # Validate dimensions
        if len(weights) != len(request.assets):
            raise HTTPException(
                status_code=400, detail="Number of weights must match number of assets"
            )

        if returns_matrix.shape[1] != len(request.assets):
            raise HTTPException(
                status_code=400,
                detail="Returns matrix columns must match number of assets",
            )

        # Use provided correlation matrix or calculate from data
        if request.correlation_matrix:
            correlation_matrix = np.array(request.correlation_matrix)
        else:
            correlation_matrix = np.corrcoef(returns_matrix.T)

        # Create Monte Carlo VaR calculator from historical data
        mc_var = MonteCarloVaR.from_historical_data(
            asset_names=request.assets,
            weights=weights,
            returns_matrix=returns_matrix,
            correlation_matrix=correlation_matrix,
        )

        # Configure simulation
        config = SimulationConfig(
            num_simulations=request.num_simulations,
            time_horizon=request.time_horizon,
            confidence_levels=request.confidence_levels,
            random_seed=42,  # For reproducible results
        )

        # Calculate VaR
        results = mc_var.calculate_var(config)

        # Format results for API response
        var_results = []
        for conf_level in request.confidence_levels:
            var_results.append(
                {
                    "confidence_level": conf_level,
                    "var_value": float(results.var_estimates[conf_level]),
                    "cvar_value": float(results.cvar_estimates[conf_level]),
                    "percentile": float(results.percentiles[conf_level]),
                }
            )

        # Calculate portfolio value impact (assuming $1M portfolio)
        portfolio_value = 1_000_000
        for result in var_results:
            result["var_dollar"] = result["var_value"] * portfolio_value
            result["cvar_dollar"] = result["cvar_value"] * portfolio_value

        return VaRResponse(
            portfolio_id="uploaded_portfolio",
            calculation_date=datetime.now().isoformat(),
            method="monte_carlo",
            assets=request.assets,
            weights=request.weights,
            var_results=var_results,
            portfolio_statistics=results.statistics,
            simulation_parameters={
                "num_simulations": config.num_simulations,
                "time_horizon": config.time_horizon,
                "observations_used": returns_matrix.shape[0],
            },
        )

    except Exception as e:
        logger.error(f"Error in Monte Carlo VaR calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"VaR calculation failed: {str(e)}")


@router.post("/upload_csv_var")
async def calculate_var_from_csv(
    portfolio_file: UploadFile = File(..., description="Portfolio weights CSV file"),
    returns_file: UploadFile = File(..., description="Historical returns CSV file"),
    confidence_levels: str = Form(
        "0.95,0.99", description="Comma-separated confidence levels"
    ),
    num_simulations: int = Form(10000, description="Number of Monte Carlo simulations"),
    time_horizon: int = Form(1, description="Time horizon in days"),
):
    """
    Calculate VaR from uploaded CSV files

    Accepts two CSV files:
    1. Portfolio weights: asset,weight
    2. Historical returns: date,asset1,asset2,...
    """
    try:
        # Validate file types
        if not portfolio_file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="Portfolio file must be CSV format"
            )
        if not returns_file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="Returns file must be CSV format"
            )

        # Read CSV files
        portfolio_content = await portfolio_file.read()
        returns_content = await returns_file.read()

        # Decode content
        portfolio_csv = portfolio_content.decode("utf-8")
        returns_csv = returns_content.decode("utf-8")

        # Process data using DataProcessor
        processor = DataProcessor()

        # Load portfolio weights
        portfolio_df = processor.load_portfolio_weights(portfolio_csv)
        if portfolio_df is None:
            raise HTTPException(
                status_code=400, detail="Invalid portfolio weights format"
            )

        # Load historical returns
        returns_df = processor.load_historical_returns(returns_csv)
        if returns_df is None:
            raise HTTPException(
                status_code=400, detail="Invalid historical returns format"
            )

        # Get processed portfolio data
        portfolio_data = processor.get_portfolio_data()
        if not portfolio_data:
            raise HTTPException(
                status_code=400, detail="Failed to process portfolio data"
            )

        # Parse confidence levels
        try:
            conf_levels = [float(x.strip()) for x in confidence_levels.split(",")]
        except:
            raise HTTPException(
                status_code=400, detail="Invalid confidence levels format"
            )

        # Create Monte Carlo request
        mc_request = MonteCarloRequest(
            assets=portfolio_data["assets"],
            weights=portfolio_data["weights"].tolist(),
            historical_returns=portfolio_data["returns_matrix"].tolist(),
            confidence_levels=conf_levels,
            num_simulations=num_simulations,
            time_horizon=time_horizon,
            correlation_matrix=portfolio_data["correlation_matrix"].tolist(),
        )

        # Calculate VaR
        result = await calculate_monte_carlo_var(mc_request)

        # Add file information to response
        result_dict = result.dict()
        result_dict["uploaded_files"] = {
            "portfolio_file": portfolio_file.filename,
            "returns_file": returns_file.filename,
            "portfolio_assets": len(portfolio_data["assets"]),
            "historical_observations": portfolio_data["num_observations"],
        }

        return result_dict

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing uploaded files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")


@router.get("/sample_data")
async def get_sample_data():
    """
    Get sample portfolio and returns data for testing
    """
    try:
        # Read sample files
        portfolio_path = (
            "/Users/hrishi/Projects/Risk Model/sample_data/portfolio_weights.csv"
        )
        returns_path = (
            "/Users/hrishi/Projects/Risk Model/sample_data/historical_returns.csv"
        )

        portfolio_df = pd.read_csv(portfolio_path)
        returns_df = pd.read_csv(returns_path)

        return {
            "portfolio_sample": portfolio_df.to_dict("records"),
            "returns_sample": returns_df.head(10).to_dict("records"),  # First 10 rows
            "total_observations": len(returns_df),
            "assets": [col for col in returns_df.columns if col != "date"],
            "description": {
                "portfolio_format": "CSV with columns: asset, weight",
                "returns_format": "CSV with columns: date, asset1, asset2, ...",
                "weight_constraint": "Portfolio weights must sum to 1.0",
                "date_format": "YYYY-MM-DD format recommended",
            },
        }

    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Could not load sample data: {str(e)}"
        )


@router.get("/validate_data")
async def validate_portfolio_data(
    portfolio_file: UploadFile = File(...), returns_file: UploadFile = File(...)
):
    """
    Validate uploaded portfolio data without running calculations
    """
    try:
        # Read and validate files
        portfolio_content = (await portfolio_file.read()).decode("utf-8")
        returns_content = (await returns_file.read()).decode("utf-8")

        processor = DataProcessor()

        # Validate portfolio
        portfolio_df = processor.load_portfolio_weights(portfolio_content)
        portfolio_valid = portfolio_df is not None

        # Validate returns
        returns_df = None
        returns_valid = False
        if portfolio_valid:
            returns_df = processor.load_historical_returns(returns_content)
            returns_valid = returns_df is not None

        # Get validation details
        validation_result = {
            "portfolio_valid": portfolio_valid,
            "returns_valid": returns_valid,
            "overall_valid": portfolio_valid and returns_valid,
        }

        if portfolio_valid:
            validation_result["portfolio_info"] = {
                "num_assets": len(portfolio_df),
                "assets": portfolio_df["asset"].tolist(),
                "weight_sum": float(portfolio_df["weight"].sum()),
                "weights": portfolio_df["weight"].tolist(),
            }

        if returns_valid:
            validation_result["returns_info"] = {
                "num_observations": len(returns_df),
                "date_range": [
                    str(returns_df["date"].min()),
                    str(returns_df["date"].max()),
                ],
                "assets_with_data": [
                    col for col in returns_df.columns if col != "date"
                ],
            }

        return validation_result

    except Exception as e:
        logger.error(f"Error validating data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for risk calculation service"""
    return {
        "status": "healthy",
        "service": "monte_carlo_var_api",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/monte_carlo_var - JSON API for VaR calculation",
            "/upload_csv_var - File upload API for VaR calculation",
            "/sample_data - Get sample data for testing",
            "/validate_data - Validate uploaded data",
            "/health - This health check",
        ],
    }
