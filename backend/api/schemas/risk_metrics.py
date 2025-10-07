"""
Risk metrics schemas for API responses
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class VaRRequest(BaseModel):
    """Request schema for VaR calculation"""

    portfolio_id: int = Field(..., description="Portfolio identifier")
    confidence_levels: List[float] = Field(
        [0.95, 0.99], description="Confidence levels for VaR"
    )
    time_horizon: int = Field(252, description="Time horizon in days")
    method: str = Field("monte_carlo", description="VaR calculation method")
    num_simulations: Optional[int] = Field(
        10000, description="Number of Monte Carlo simulations"
    )


class VaRResult(BaseModel):
    """VaR calculation result"""

    confidence_level: float
    var_value: float
    cvar_value: float
    var_dollar: float
    cvar_dollar: float


class RiskMetrics(BaseModel):
    """Risk metrics response"""

    portfolio_id: int
    calculation_date: datetime
    var_results: List[VaRResult]
    portfolio_statistics: Dict[str, float]
    method_used: str
    parameters: Dict[str, float]


class StressTestScenario(BaseModel):
    """Stress test scenario definition"""

    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    modifications: Dict[str, float] = Field(..., description="Parameter modifications")


class StressTestRequest(BaseModel):
    """Stress testing request"""

    portfolio_id: int
    scenarios: List[StressTestScenario]
    base_config: VaRRequest


class StressTestResult(BaseModel):
    """Stress test results"""

    scenario_name: str
    risk_metrics: RiskMetrics
    impact_summary: Dict[str, float]
