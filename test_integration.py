#!/usr/bin/env python3
"""
Integration test script for the Quantitative Risk Platform
Tests both backend API and frontend integration
"""

import requests
import json
import time
import sys

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Health: {result['status']}")
            return True
        else:
            print(f"❌ API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False

def test_var_calculation():
    """Test VaR calculation endpoint"""
    print("🎲 Testing Monte Carlo VaR calculation...")
    try:
        response = requests.post("http://localhost:8000/api/v1/risk/var", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ VaR Calculation successful!")
            print(f"   Portfolio ID: {result['portfolio_id']}")
            print(f"   Method: {result['method_used']}")
            print(f"   Simulations: {result['parameters']['num_simulations']}")
            
            # Display VaR results
            for var_result in result['var_results']:
                conf = var_result['confidence_level']
                var_val = var_result['var_value']
                var_dollar = var_result['var_dollar']
                print(f"   {conf:.0%} VaR: {var_val:.4f} (${var_dollar:,.0f})")
            
            return True
        else:
            print(f"❌ VaR Calculation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ VaR Calculation error: {e}")
        return False

def test_portfolio_endpoint():
    """Test portfolio data endpoint"""
    print("📈 Testing portfolio endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/portfolio/", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Portfolio data retrieved!")
            portfolio = result['portfolios'][0]
            print(f"   Name: {portfolio['name']}")
            print(f"   Total Value: ${portfolio['total_value']:,.0f}")
            print(f"   Assets: {len(portfolio['assets'])}")
            for asset in portfolio['assets']:
                print(f"     - {asset['symbol']}: {asset['weight']:.1%} (${asset['value']:,.0f})")
            return True
        else:
            print(f"❌ Portfolio endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Portfolio endpoint error: {e}")
        return False

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("🎨 Testing frontend accessibility...")
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend accessibility error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting Quantitative Risk Platform Integration Tests")
    print("=" * 60)
    
    tests = [
        ("API Health", test_api_health),
        ("Portfolio Data", test_portfolio_endpoint),
        ("VaR Calculation", test_var_calculation),
        ("Frontend Access", test_frontend_accessibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The platform is ready to use.")
        print("\n📍 Access URLs:")
        print("   Frontend Dashboard: http://localhost:8501")
        print("   Backend API Docs: http://localhost:8000/docs")
        print("   API Health: http://localhost:8000/health")
        return True
    else:
        print("⚠️  Some tests failed. Please check the backend and frontend services.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)