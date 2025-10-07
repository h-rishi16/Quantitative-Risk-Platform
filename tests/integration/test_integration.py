#!/usr/bin/env python3
"""
Integration test script for the Quantitative Risk Platform
Tests both backend API and frontend integration
"""

import pytest

import json
import sys
import time

import requests


def test_api_health():
    """Test API health endpoint"""
    print("TESTING: Testing API health endpoint...")
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: API Health: {result['status']}")
            return True
        else:
            print(f"ERROR: API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: API Health error: {e}")
        return False


def test_var_calculation():
    """Test VaR calculation endpoint"""
    print("TESTING: Testing Monte Carlo VaR calculation...")

    # Sample request data
    sample_request = {
        "assets": ["AAPL", "GOOGL", "MSFT"],
        "weights": [0.4, 0.3, 0.3],
        "historical_returns": [
            [0.01, 0.02, 0.015],
            [-0.005, 0.01, 0.008],
            [0.02, -0.01, 0.012],
        ],
        "confidence_levels": [0.95, 0.99],
        "num_simulations": 1000,
    }

    try:
        response = requests.post(
            "http://localhost:8002/monte_carlo_var", json=sample_request, timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: VaR Calculation successful!")
            print(f"   Portfolio ID: {result['portfolio_id']}")
            print(f"   Method: {result['method']}")
            print(f"   Assets: {len(result['assets'])}")

            # Display VaR results
            for var_result in result["var_results"]:
                conf = var_result["confidence_level"]
                var_val = var_result["var_value"]
                print(f"   {conf:.0%} VaR: {var_val:.4f}")

            return True
        else:
            print(f"ERROR: VaR Calculation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: VaR Calculation error: {e}")
        return False


def test_sample_data_endpoint():
    """Test sample data endpoint"""
    print("TESTING: Testing sample data endpoint...")
    try:
        response = requests.get("http://localhost:8002/sample_data", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Sample data retrieved!")
            print(f"   Assets: {len(result.get('assets', []))}")
            print(f"   Weights available: {len(result.get('weights', []))}")
            print(
                f"   Returns data points: {len(result.get('historical_returns', []))}"
            )
            return True
        else:
            print(f"ERROR: Sample data endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Sample data endpoint error: {e}")
        return False


def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("TESTING: Testing frontend accessibility...")
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Frontend is accessible!")
            return True
        else:
            print(f"ERROR: Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Frontend accessibility error: {e}")
        return False


def main():
    """Run all integration tests"""
    print("STARTING: Starting Quantitative Risk Platform Integration Tests")
    print("=" * 60)

    tests = [
        ("API Health", test_api_health),
        ("Sample Data", test_sample_data_endpoint),
        ("VaR Calculation", test_var_calculation),
        ("Frontend Access", test_frontend_accessibility),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nRUNNING: Running {test_name} test...")
        if test_func():
            passed += 1
        time.sleep(0.5)  # Small delay between tests

    print("\n" + "=" * 60)
    print(f"RESULTS: Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: All tests passed! The platform is ready to use.")
        print("\nACCESS URLs:")
        print("   Frontend Dashboard: http://localhost:8501")
        print("   Backend API Docs: http://localhost:8000/docs")
        print("   API Health: http://localhost:8000/health")
        return True
    else:
        print(
            "WARNING: Some tests failed. Please check the backend and frontend services."
        )
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
