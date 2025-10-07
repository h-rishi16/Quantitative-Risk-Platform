"""
Portfolio data models and schemas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class AssetClass(str, Enum):
    """Asset classification"""
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"  
    COMMODITY = "commodity"
    CURRENCY = "currency"
    ALTERNATIVE = "alternative"

class Position(BaseModel):
    """Individual position in portfolio"""
    symbol: str = Field(..., description="Asset symbol (e.g., AAPL)")
    quantity: float = Field(..., description="Number of shares/units")
    market_value: float = Field(..., description="Current market value")
    weight: float = Field(..., description="Portfolio weight (0-1)")
    asset_class: AssetClass = Field(..., description="Asset classification")
    expected_return: Optional[float] = Field(None, description="Expected annual return")
    volatility: Optional[float] = Field(None, description="Annual volatility")
    
    @validator('weight')
    def validate_weight(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Weight must be between 0 and 1')
        return v

class PortfolioCreate(BaseModel):
    """Portfolio creation schema"""
    name: str = Field(..., description="Portfolio name")
    description: Optional[str] = Field(None, description="Portfolio description")
    positions: List[Position] = Field(..., description="List of positions")
    base_currency: str = Field("USD", description="Base currency")
    
    @validator('positions')
    def validate_positions(cls, v):
        if not v:
            raise ValueError('Portfolio must have at least one position')
        
        total_weight = sum(pos.weight for pos in v)
        if not 0.99 <= total_weight <= 1.01:  # Allow small rounding errors
            raise ValueError(f'Position weights must sum to 1.0, got {total_weight}')
        
        return v

class Portfolio(PortfolioCreate):
    """Portfolio response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    total_value: float
    
    class Config:
        from_attributes = True