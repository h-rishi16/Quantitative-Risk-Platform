# API Documentation

This document provides comprehensive API documentation for the Quantitative Risk Platform backend services.

## Overview

The Risk Platform API provides endpoints for portfolio risk analysis, including Value at Risk (VaR) calculations, Monte Carlo simulations, and portfolio optimization features.

**Base URL**: `https://risk-platform-api.onrender.com`

## Authentication

Currently, the API uses simple token-based authentication for development. Production deployments should implement OAuth2 or JWT-based authentication.

```python
headers = {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
}
```

## Core Endpoints

### Portfolio Risk Analysis

#### POST /api/v1/portfolio/risk
Calculate comprehensive risk metrics for a given portfolio.

**Request Body:**
```json
{
    "assets": [
        {
            "symbol": "AAPL",
            "weight": 0.3,
            "current_price": 150.00
        },
        {
            "symbol": "GOOGL", 
            "weight": 0.4,
            "current_price": 2800.00
        },
        {
            "symbol": "MSFT",
            "weight": 0.3,
            "current_price": 300.00
        }
    ],
    "confidence_levels": [0.95, 0.99],
    "time_horizon": 252,
    "simulation_count": 10000
}
```

**Response:**
```json
{
    "portfolio_value": 1000000,
    "var_calculations": {
        "monte_carlo": {
            "95%": {
                "value_at_risk": 85000,
                "percentage": 8.5
            },
            "99%": {
                "value_at_risk": 125000,
                "percentage": 12.5
            }
        },
        "historical_simulation": {
            "95%": {
                "value_at_risk": 82000,
                "percentage": 8.2
            }
        }
    },
    "expected_shortfall": {
        "95%": 95000,
        "99%": 140000
    },
    "correlation_matrix": [
        [1.0, 0.45, 0.52],
        [0.45, 1.0, 0.38],
        [0.52, 0.38, 1.0]
    ],
    "portfolio_statistics": {
        "expected_return": 0.12,
        "volatility": 0.18,
        "sharpe_ratio": 1.25
    }
}
```

#### GET /api/v1/portfolio/risk/{portfolio_id}
Retrieve previously calculated risk metrics for a specific portfolio.

### Market Data

#### GET /api/v1/market/prices
Fetch current market prices for specified assets.

**Query Parameters:**
- `symbols`: Comma-separated list of asset symbols
- `period`: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y)

#### GET /api/v1/market/historical/{symbol}
Get historical price data for a specific asset.

### Stress Testing

#### POST /api/v1/stress-test
Perform stress testing scenarios on portfolio.

**Request Body:**
```json
{
    "portfolio_id": "uuid-here",
    "scenarios": [
        {
            "name": "Market Crash 2008",
            "market_shock": -0.4,
            "correlation_increase": 0.8
        },
        {
            "name": "Interest Rate Rise", 
            "rate_change": 0.02,
            "sector_impacts": {
                "TECH": -0.15,
                "FINANCIALS": 0.05
            }
        }
    ]
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in JSON format:

```json
{
    "error": {
        "code": "INVALID_PORTFOLIO",
        "message": "Portfolio weights must sum to 1.0",
        "details": {
            "current_sum": 1.15,
            "expected_sum": 1.0
        }
    }
}
```

### Common Error Codes

- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server processing error

## Rate Limiting

- **Development**: 100 requests per minute
- **Production**: 1000 requests per minute
- **Enterprise**: Custom limits based on subscription

## SDK Examples

### Python
```python
import requests

# Initialize client
api_base = "https://risk-platform-api.onrender.com"
headers = {"Authorization": "Bearer your-token"}

# Calculate portfolio risk
portfolio_data = {
    "assets": [
        {"symbol": "AAPL", "weight": 0.6, "current_price": 150},
        {"symbol": "BONDS", "weight": 0.4, "current_price": 100}
    ],
    "confidence_levels": [0.95, 0.99]
}

response = requests.post(
    f"{api_base}/api/v1/portfolio/risk",
    json=portfolio_data,
    headers=headers
)

risk_metrics = response.json()
print(f"95% VaR: ${risk_metrics['var_calculations']['monte_carlo']['95%']['value_at_risk']:,.2f}")
```

### JavaScript
```javascript
const apiClient = {
    baseURL: 'https://risk-platform-api.onrender.com',
    token: 'your-token-here',
    
    async calculatePortfolioRisk(portfolioData) {
        const response = await fetch(`${this.baseURL}/api/v1/portfolio/risk`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(portfolioData)
        });
        
        return await response.json();
    }
};
```

## Performance Considerations

- **Batch Requests**: Use batch endpoints for multiple portfolio calculations
- **Caching**: Market data is cached for 5 minutes during trading hours
- **Async Processing**: Large simulations (>50,000 iterations) are processed asynchronously
- **Response Pagination**: Large datasets are paginated with `limit` and `offset` parameters

## Monitoring and Health Checks

### Health Endpoints
- `GET /health`: Basic health check
- `GET /health/detailed`: Comprehensive system status
- `GET /metrics`: Prometheus-compatible metrics

### Response Format
```json
{
    "status": "healthy",
    "timestamp": "2025-01-15T10:30:00Z",
    "version": "1.2.3",
    "dependencies": {
        "database": "healthy",
        "redis_cache": "healthy",
        "market_data_provider": "healthy"
    },
    "performance": {
        "avg_response_time_ms": 245,
        "requests_per_minute": 156
    }
}
```

## Changelog

### Version 1.2.3 (Current)
- Added stress testing endpoints
- Improved Monte Carlo simulation performance
- Enhanced error handling and validation

### Version 1.2.2
- Added historical simulation VaR method
- Implemented portfolio correlation analysis
- Added batch processing capabilities

### Version 1.2.1
- Initial API release
- Basic VaR calculations
- Market data integration