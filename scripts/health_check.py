#!/usr/bin/env python3
"""
Comprehensive Health Check Script for Quantitative Risk Platform
"""

import json
import os
import subprocess
import sys
import time
from typing import Dict, List, Tuple

import requests


class HealthChecker:
    def __init__(self):
        self.results = {}
        self.backend_url = "http://localhost:8002"
        self.frontend_url = "http://localhost:8501"

    def print_header(self, title: str):
        """Print section header"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")

    def print_result(self, test_name: str, success: bool, message: str = ""):
        """Print test result"""
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
        if message:
            print(f"      {message}")

    def check_python_environment(self) -> bool:
        """Check Python version and environment"""
        self.print_header("PYTHON ENVIRONMENT")

        # Python version
        python_version = sys.version
        print(f"Python Version: {python_version}")

        # Check if we're in the right directory
        cwd = os.getcwd()
        expected_files = ["backend", "frontend", "requirements.txt", "README.md"]
        missing_files = [f for f in expected_files if not os.path.exists(f)]

        if missing_files:
            self.print_result("Project Structure", False, f"Missing: {missing_files}")
            return False
        else:
            self.print_result(
                "Project Structure", True, "All expected directories found"
            )
            return True

    def check_dependencies(self) -> bool:
        """Check if all required packages are installed"""
        self.print_header("DEPENDENCY CHECK")

        # Core dependencies
        core_packages = [
            "fastapi",
            "uvicorn",
            "streamlit",
            "plotly",
            "requests",
            "numpy",
            "pandas",
            "scipy",
            "pydantic",
            "python_multipart",
            "python_dotenv",
            "aiofiles",
        ]

        # Development dependencies
        dev_packages = [
            "pytest",
            "httpx",
            "black",
            "isort",
            "flake8",
            "bandit",
            "safety",
            "coverage",
        ]

        failed_packages = []

        print("\nCore Dependencies:")
        for package in core_packages:
            try:
                __import__(package.replace("-", "_").replace("python_", ""))
                self.print_result(f"  {package}", True)
            except ImportError as e:
                self.print_result(f"  {package}", False, str(e))
                failed_packages.append(package)

        print("\nDevelopment Dependencies:")
        for package in dev_packages:
            try:
                __import__(package.replace("-", "_"))
                self.print_result(f"  {package}", True)
            except ImportError as e:
                self.print_result(f"  {package}", False, str(e))
                failed_packages.append(package)

        if failed_packages:
            print(f"\nFailed packages: {failed_packages}")
            print("Run: pip install -r requirements.txt")
            return False

        return True

    def check_backend_api(self) -> bool:
        """Check if backend API is running and responding"""
        self.print_header("BACKEND API CHECK")

        try:
            # Health endpoint
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                self.print_result(
                    "Health Endpoint", True, f"Response: {response.json()}"
                )
            else:
                self.print_result(
                    "Health Endpoint", False, f"Status: {response.status_code}"
                )
                return False

            # Sample data endpoint
            response = requests.get(f"{self.backend_url}/sample_data", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_result(
                    "Sample Data Endpoint",
                    True,
                    f"Assets: {len(data.get('portfolio_weights', []))}",
                )
            else:
                self.print_result(
                    "Sample Data Endpoint", False, f"Status: {response.status_code}"
                )
                return False

            # Monte Carlo API test
            test_payload = {
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

            response = requests.post(
                f"{self.backend_url}/monte_carlo_var", json=test_payload, timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                var_results = result.get("var_results", [])
                self.print_result(
                    "Monte Carlo API", True, f"VaR calculations: {len(var_results)}"
                )
            else:
                self.print_result(
                    "Monte Carlo API", False, f"Status: {response.status_code}"
                )
                return False

            return True

        except requests.exceptions.ConnectionError:
            self.print_result(
                "Backend Connection", False, "Cannot connect - is backend running?"
            )
            print(
                "      Start with: python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002"
            )
            return False
        except Exception as e:
            self.print_result("Backend API", False, str(e))
            return False

    def check_frontend(self) -> bool:
        """Check if frontend can be started"""
        self.print_header("FRONTEND CHECK")

        # Check if frontend files exist
        frontend_files = ["frontend/app.py"]
        missing_files = [f for f in frontend_files if not os.path.exists(f)]

        if missing_files:
            self.print_result("Frontend Files", False, f"Missing: {missing_files}")
            return False

        self.print_result("Frontend Files", True, "All frontend files found")

        # Try to import streamlit modules used in frontend
        try:
            import streamlit
            import plotly.express
            import plotly.graph_objects

            self.print_result(
                "Frontend Dependencies", True, "All required modules available"
            )
        except ImportError as e:
            self.print_result("Frontend Dependencies", False, str(e))
            return False

        # Test frontend startup (without actually running it)
        try:
            # Just check if the file can be parsed
            with open("frontend/app.py", "r") as f:
                content = f.read()

            # Basic syntax check
            compile(content, "frontend/app.py", "exec")
            self.print_result("Frontend Syntax", True, "No syntax errors found")
            return True

        except SyntaxError as e:
            self.print_result("Frontend Syntax", False, f"Syntax error: {e}")
            return False
        except Exception as e:
            self.print_result("Frontend Check", False, str(e))
            return False

    def run_tests(self) -> bool:
        """Run the test suite"""
        self.print_header("TEST SUITE")

        try:
            # Run pytest
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                # Count passed tests
                passed_tests = result.stdout.count(" PASSED")
                self.print_result("Unit Tests", True, f"{passed_tests} tests passed")
                return True
            else:
                self.print_result("Unit Tests", False, "Some tests failed")
                print("      Run: python -m pytest tests/ -v for details")
                return False

        except subprocess.TimeoutExpired:
            self.print_result("Unit Tests", False, "Tests timed out")
            return False
        except FileNotFoundError:
            self.print_result("Unit Tests", False, "pytest not found")
            return False
        except Exception as e:
            self.print_result("Unit Tests", False, str(e))
            return False

    def check_deployment_scripts(self) -> bool:
        """Check deployment scripts"""
        self.print_header("DEPLOYMENT SCRIPTS")

        scripts = {
            "deployment/deploy.sh": "Main deployment script",
            "scripts/simple_main.py": "Simple main runner",
        }

        all_good = True
        for script, description in scripts.items():
            if os.path.exists(script):
                # Check if executable (for shell scripts)
                if script.endswith(".sh"):
                    is_executable = os.access(script, os.X_OK)
                    if is_executable:
                        self.print_result(description, True, "Found and executable")
                    else:
                        self.print_result(
                            description, False, "Found but not executable"
                        )
                        print(f"      Run: chmod +x {script}")
                        all_good = False
                else:
                    self.print_result(description, True, "Found")
            else:
                self.print_result(description, False, "Not found")
                all_good = False

        return all_good

    def generate_summary(self) -> Dict:
        """Generate summary report"""
        self.print_header("HEALTH CHECK SUMMARY")

        # Run all checks
        checks = {
            "Python Environment": self.check_python_environment(),
            "Dependencies": self.check_dependencies(),
            "Backend API": self.check_backend_api(),
            "Frontend": self.check_frontend(),
            "Test Suite": self.run_tests(),
            "Deployment Scripts": self.check_deployment_scripts(),
        }

        # Summary
        total_checks = len(checks)
        passed_checks = sum(checks.values())

        print(f"\nOVERALL HEALTH: {passed_checks}/{total_checks} checks passed")

        if passed_checks == total_checks:
            print("[SUCCESS] All systems operational!")
        elif passed_checks >= total_checks * 0.8:
            print("[WARNING] Most systems operational, minor issues detected")
        else:
            print("[ERROR] Major issues detected, system may not function properly")

        # Recommendations
        print(f"\n{'='*60}")
        print(" RECOMMENDATIONS")
        print(f"{'='*60}")

        if not checks["Dependencies"]:
            print("- Install missing dependencies: pip install -r requirements.txt")

        if not checks["Backend API"]:
            print(
                "- Start backend: python -m uvicorn scripts.simple_main:app --host 0.0.0.0 --port 8002"
            )

        if not checks["Test Suite"]:
            print("- Fix failing tests: python -m pytest tests/ -v")

        if not checks["Deployment Scripts"]:
            print("- Make scripts executable: chmod +x deployment/deploy.sh")

        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "success_rate": passed_checks / total_checks,
            "checks": checks,
        }


def main():
    """Main function"""
    print("Quantitative Risk Platform - Health Check")
    print("=" * 60)

    checker = HealthChecker()
    summary = checker.generate_summary()

    # Exit with appropriate code
    if summary["success_rate"] == 1.0:
        sys.exit(0)  # All checks passed
    elif summary["success_rate"] >= 0.8:
        sys.exit(1)  # Minor issues
    else:
        sys.exit(2)  # Major issues


if __name__ == "__main__":
    main()
