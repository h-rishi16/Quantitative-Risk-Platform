# API Documentation

## Base URL
- Development: `http://localhost:8002`
- Production: `https://api.riskplatform.com`

## Authentication
Currently, the API doesn't require authentication. This will be added in future versions.

## Endpoints

### Health Check

#### `GET /health`
Check the health status of the API.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is unhealthy

---

### Sample Data

#### `GET /sample_data`
Get sample portfolio and returns data for testing.

**Response:**
```json
{
  "portfolio_weights": [
    {"asset": "AAPL", "weight": 0.4},
    {"asset": "GOOGL", "weight": 0.3},
    {"asset": "MSFT", "weight": 0.3}
  ],
  "sample_returns": [
    {"date": "2024-01-01", "AAPL": 0.01, "GOOGL": -0.005, "MSFT": 0.008},
    {"date": "2024-01-02", "AAPL": -0.012, "GOOGL": 0.02, "MSFT": 0.005}
  ]
}
```

---

### Monte Carlo VaR Calculation

#### `POST /monte_carlo_var`
Calculate Value at Risk using Monte Carlo simulation.

**Request Body:**
```json
{
  "assets": ["AAPL", "GOOGL", "MSFT"],
  "weights": [0.4, 0.3, 0.3],
  "historical_returns": [
    [0.01, -0.005, 0.008],
    [-0.012, 0.02, 0.005],
    [0.008, 0.015, -0.003]
  ],
  "confidence_levels": [0.95, 0.99],
  "num_simulations": 10000,
  "time_horizon": 1
}
```

**Request Schema:**
- `assets` (array of strings, required): List of asset identifiers
- `weights` (array of numbers, required): Portfolio weights (must sum to 1.0)
- `historical_returns` (array of arrays, required): Historical return data matrix
- `confidence_levels` (array of numbers, optional): VaR confidence levels (default: [0.95, 0.99])
- `num_simulations` (integer, optional): Number of Monte Carlo simulations (default: 10000)
- `time_horizon` (integer, optional): Time horizon in days (default: 1)

**Response:**
```json
{
  "var_results": [
    {
      "confidence_level": 0.95,
      "var_value": 0.0234,
      "var_dollar": 234000,
      "cvar_value": 0.0289,
      "cvar_dollar": 289000
    }
  ],
  "portfolio_statistics": {
    "mean_return": 0.0048,
    "std_return": 0.0205,
    "skewness": -0.167,
    "kurtosis": 2.876
  },
  "simulation_parameters": {
    "num_simulations": 10000,
    "time_horizon": 1,
    "assets": ["AAPL", "GOOGL", "MSFT"]
  }
}
```

**Status Codes:**
- `200 OK` - Calculation successful
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Calculation error

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "error": "Error description",
  "detail": "Detailed error message"
}
```

## Rate Limiting
Currently no rate limiting is implemented. This will be added in future versions.

## Examples

### Python Example
```python
import requests

# Basic VaR calculation
data = {
    "assets": ["AAPL", "GOOGL", "MSFT"],
    "weights": [0.4, 0.3, 0.3],
    "historical_returns": [
        [0.01, -0.005, 0.008],
        [-0.012, 0.02, 0.005],
        [0.008, 0.015, -0.003]
    ],
    "confidence_levels": [0.95, 0.99],
    "num_simulations": 10000
}

response = requests.post("http://localhost:8002/monte_carlo_var", json=data)
result = response.json()

print(f"95% VaR: ${result['var_results'][0]['var_dollar']:,.0f}")
```

### cURL Example
```bash
curl -X POST "http://localhost:8002/monte_carlo_var" \
     -H "Content-Type: application/json" \
     -d '{
       "assets": ["AAPL", "GOOGL", "MSFT"],
       "weights": [0.4, 0.3, 0.3],
       "historical_returns": [
         [0.01, -0.005, 0.008],
         [-0.012, 0.02, 0.005]
       ],
       "confidence_levels": [0.95, 0.99],
       "num_simulations": 1000
     }'
```

### JavaScript Example
```javascript
const data = {
  assets: ["AAPL", "GOOGL", "MSFT"],
  weights: [0.4, 0.3, 0.3],
  historical_returns: [
    [0.01, -0.005, 0.008],
    [-0.012, 0.02, 0.005]
  ],
  confidence_levels: [0.95, 0.99],
  num_simulations: 10000
};

fetch('http://localhost:8002/monte_carlo_var', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
  console.log('VaR Results:', result.var_results);
});
```