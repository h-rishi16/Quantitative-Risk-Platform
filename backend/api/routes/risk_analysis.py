"""
Risk analysis API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import logging

from ..schemas.risk_metrics import (
    VaRRequest, RiskMetrics, StressTestRequest, StressTestResult
)
from ...risk_engines.monte_carlo import (
    MonteCarloVaR, AssetParameters, SimulationConfig, VaRResults
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/var", response_model=RiskMetrics)
async def calculate_var(request: VaRRequest):
    """
    Calculate Value at Risk for a portfolio using specified method
    """
    try:
        logger.info(f"Calculating VaR for portfolio {request.portfolio_id}")
        
        # Mock asset data - in production, this would come from database
        assets = [
            AssetParameters("AAPL", 150.0, 0.12, 0.25, 0.4),
            AssetParameters("GOOGL", 2500.0, 0.15, 0.30, 0.3),
            AssetParameters("MSFT", 300.0, 0.10, 0.22, 0.3),
        ]
        
        # Create simulation configuration
        config = SimulationConfig(
            num_simulations=request.num_simulations or 10000,
            time_horizon=request.time_horizon,
            confidence_levels=request.confidence_levels,
            random_seed=42
        )
        
        # Calculate VaR using Monte Carlo
        mc_var = MonteCarloVaR(assets)
        results = mc_var.calculate_var(config)
        
        # Convert to API response format
        var_results = []
        portfolio_value = 10_000_000  # Mock portfolio value
        
        for conf_level in request.confidence_levels:
            var_results.append({
                "confidence_level": conf_level,
                "var_value": results.var_estimates[conf_level],
                "cvar_value": results.cvar_estimates[conf_level],
                "var_dollar": results.var_estimates[conf_level] * portfolio_value,
                "cvar_dollar": results.cvar_estimates[conf_level] * portfolio_value
            })
        
        return RiskMetrics(
            portfolio_id=request.portfolio_id,
            calculation_date=datetime.now(),
            var_results=var_results,
            portfolio_statistics=results.statistics,
            method_used=request.method,
            parameters={
                "num_simulations": config.num_simulations,
                "time_horizon": config.time_horizon
            }
        )
        
    except Exception as e:
        logger.error(f"Error calculating VaR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"VaR calculation failed: {str(e)}")

@router.post("/monte-carlo")
async def run_monte_carlo_simulation(request: VaRRequest):
    """
    Run Monte Carlo simulation for portfolio risk assessment
    """
    try:
        # This would use the same logic as calculate_var but with more detailed output
        # including the full simulation results
        return await calculate_var(request)
        
    except Exception as e:
        logger.error(f"Error in Monte Carlo simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Monte Carlo simulation failed: {str(e)}")

@router.post("/stress-test", response_model=List[StressTestResult])
async def run_stress_test(request: StressTestRequest):
    """
    Perform stress testing on portfolio under various scenarios
    """
    try:
        logger.info(f"Running stress test for portfolio {request.portfolio_id}")
        
        results = []
        
        for scenario in request.scenarios:
            # Mock stress test results
            # In production, this would apply the scenario modifications
            # and recalculate risk metrics
            
            mock_result = StressTestResult(
                scenario_name=scenario.name,
                risk_metrics=RiskMetrics(
                    portfolio_id=request.portfolio_id,
                    calculation_date=datetime.now(),
                    var_results=[
                        {
                            "confidence_level": 0.95,
                            "var_value": 0.05,
                            "cvar_value": 0.07,
                            "var_dollar": 500000,
                            "cvar_dollar": 700000
                        }
                    ],
                    portfolio_statistics={"stressed_volatility": 0.35},
                    method_used="stress_test",
                    parameters=scenario.modifications
                ),
                impact_summary={
                    "var_change": 0.15,
                    "volatility_change": 0.25
                }
            )
            
            results.append(mock_result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in stress testing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stress test failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for risk analysis service"""
    return {"status": "healthy", "service": "risk_analysis"}