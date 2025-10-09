#!/usr/bin/env python3
"""
Validation script to test key components before deployment
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    # Test basic dependencies
    try:
        import streamlit
        import numpy
        import pandas 
        import plotly
        import requests
        print("✅ Basic dependencies: OK")
    except ImportError as e:
        print(f"❌ Basic dependencies failed: {e}")
        return False
    
    # Test backend imports
    try:
        from backend.risk_engines.monte_carlo import MonteCarloVaR, SimulationConfig
        from backend.data_processing.data_processor import DataProcessor
        print("✅ Backend components: OK")
    except ImportError as e:
        print(f"❌ Backend components failed: {e}")
        return False
        
    # Test API imports  
    try:
        from fastapi import FastAPI
        import uvicorn
        print("✅ API components: OK")
    except ImportError as e:
        print(f"❌ API components failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test critical files exist"""
    print("\n📁 Testing file structure...")
    
    critical_files = [
        "frontend/app.py",
        "backend/app/main.py",
        "backend/risk_engines/monte_carlo.py",
        "requirements.txt",
        "requirements/requirements-render.txt",
        "configs/render.yaml",
        "configs/render-stable.yaml",
        "configs/render-fullstack.yaml"
    ]
    
    missing_files = []
    for file_path in critical_files:
        full_path = os.path.join(project_root, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All critical files present")
        return True

def test_syntax():
    """Test Python syntax of key files"""
    print("\n🔍 Testing Python syntax...")
    
    python_files = [
        "frontend/app.py",
        "backend/app/main.py",
        "backend/risk_engines/monte_carlo.py"
    ]
    
    for file_path in python_files:
        full_path = os.path.join(project_root, file_path)
        try:
            with open(full_path, 'r') as f:
                compile(f.read(), full_path, 'exec')
            print(f"✅ {file_path}: Syntax OK")
        except SyntaxError as e:
            print(f"❌ {file_path}: Syntax error - {e}")
            return False
        except Exception as e:
            print(f"❌ {file_path}: Error - {e}")
            return False
    
    return True

def main():
    """Run all validation tests"""
    print("🚀 Quantitative Risk Platform - Deployment Validation")
    print("=" * 60)
    
    success = True
    success &= test_file_structure()
    success &= test_syntax() 
    success &= test_imports()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All validation tests passed! Ready for deployment.")
        print("\n📋 Next steps:")
        print("   1. git add .")
        print("   2. git commit -m 'Ready for deployment'")
        print("   3. git push origin main")
        print("   4. Deploy using:")
        print("      - Single service: configs/render.yaml or configs/render-stable.yaml")
        print("      - Two services: configs/render-fullstack.yaml")
    else:
        print("❌ Some validation tests failed. Please fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()