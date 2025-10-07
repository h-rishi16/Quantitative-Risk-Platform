#!/usr/bin/env python3
"""
Setup script for initializing the Quantitative Risk Platform
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(description, command):
    """Run a command and report status"""
    print(f"RUNNING: {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print("SETUP: Setting up Risk Model development environment...")
    print("")
    
    steps = [
        ("Installing Python dependencies", "pip install -r requirements.txt"),
        ("Running database setup", "python backend/database/init_db.py"),
        ("Running tests", "python -m pytest tests/ -v"),
    ]
    
    success_count = 0
    for desc, cmd in steps:
        if run_command(desc, cmd):
            success_count += 1
    
    print("")
    if success_count == len(steps):
        print("SUCCESS: Setup completed successfully! All steps passed.")
        print("NEXT STEPS:")
        print("   1. Start the backend: cd backend && uvicorn main:app --reload")
        print("   2. Start the frontend: cd frontend && streamlit run app.py")
    else:
        print(f"WARNING: Setup completed with {len(steps) - success_count} failures.")
        print("Please check the error messages above and resolve any issues.")


if __name__ == "__main__":
    main()
