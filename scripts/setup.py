#!/usr/bin/env python3
"""
Setup script for initializing the Quantitative Risk Platform
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None


def main():
    """Main setup function"""
    print("🚀 Setting up Quantitative Risk Modeling Platform")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        sys.exit(1)

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Install dependencies
    requirements_files = ["requirements/base.txt", "requirements/development.txt"]

    for req_file in requirements_files:
        if Path(req_file).exists():
            run_command(f"pip install -r {req_file}", f"Installing {req_file}")

    # Create necessary directories
    directories = ["logs", "data", "models", "tmp"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

    # Copy environment file
    if not Path(".env").exists() and Path(".env.example").exists():
        run_command("cp .env.example .env", "Creating .env file")
        print("⚠️  Please edit .env file with your configuration")

    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Start backend: cd backend && uvicorn app.main:app --reload")
    print("3. Start frontend: cd frontend && streamlit run app.py")


if __name__ == "__main__":
    main()
