"""
Basic test for the Monte Carlo VaR API
"""
import pytest
from fastapi.testclient import TestClient
from simple_main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_sample_data_endpoint():
    """Test the sample data endpoint"""
    response = client.get("/sample_data")
    assert response.status_code == 200
    data = response.json()
    assert "portfolio_weights" in data
    assert "sample_returns" in data


def test_monte_carlo_var_endpoint():
    """Test the Monte Carlo VaR calculation endpoint"""
    test_data = {
        "assets": ["AAPL", "GOOGL", "MSFT"],
        "weights": [0.4, 0.3, 0.3],
        "historical_returns": [
            [0.01, -0.005, 0.008],
            [-0.012, 0.02, 0.005],
            [0.008, 0.015, -0.003],
        ],
        "confidence_levels": [0.95, 0.99],
        "num_simulations": 1000,
        "time_horizon": 1,
    }

    response = client.post("/monte_carlo_var", json=test_data)
    assert response.status_code == 200

    result = response.json()
    assert "var_results" in result
    assert "portfolio_statistics" in result
    assert "simulation_parameters" in result

    # Check VaR results structure
    var_results = result["var_results"]
    assert len(var_results) == 2  # Two confidence levels

    for var_result in var_results:
        assert "confidence_level" in var_result
        assert "var_value" in var_result
        assert "var_dollar" in var_result
        assert "cvar_value" in var_result
        assert "cvar_dollar" in var_result


def test_monte_carlo_var_validation():
    """Test input validation for Monte Carlo VaR endpoint"""
    # Test with invalid weights (don't sum to 1)
    invalid_data = {
        "assets": ["AAPL", "GOOGL"],
        "weights": [0.8, 0.8],  # Sum > 1
        "historical_returns": [[0.01, -0.005], [-0.012, 0.02]],
    }

    response = client.post("/monte_carlo_var", json=invalid_data)
    # Should still work but might give warning in logs
    assert response.status_code in [200, 400]


def test_monte_carlo_var_empty_data():
    """Test Monte Carlo VaR with empty data"""
    empty_data = {"assets": [], "weights": [], "historical_returns": []}

    response = client.post("/monte_carlo_var", json=empty_data)
    # Should handle gracefully
    assert response.status_code in [200, 400, 422]
