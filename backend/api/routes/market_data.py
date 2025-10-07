"""
Market data API endpoints
"""

import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/prices")
async def get_current_prices():
    """Get current market prices"""
    return {"prices": {}}


@router.get("/historical")
async def get_historical_data():
    """Get historical market data"""
    return {"historical_data": []}
