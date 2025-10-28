#!/usr/bin/env python3
"""
Test runner script for the e-commerce Clean Architecture project.

This script runs all tests with coverage reporting and provides detailed metrics.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def main():
    """Main test runner function."""
    print("🧪 E-commerce Clean Architecture Test Suite")
    print("=" * 60)
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        return 1
    
    # Run unit tests
    print("\n🔬 Running unit tests...")
    unit_success = run_command(
        "pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/unit",
        "Unit tests with coverage"
    )
    
    # Run integration tests
    print("\n🔗 Running integration tests...")
    integration_success = run_command(
        "pytest tests/integration/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/integration",
        "Integration tests with coverage"
    )
    
    # Run E2E tests
    print("\n🌐 Running E2E tests...")
    e2e_success = run_command(
        "pytest tests/e2e/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/e2e",
        "E2E tests with coverage"
    )
    
    # Run all tests with comprehensive coverage
    print("\n📊 Running comprehensive test suite...")
    all_tests_success = run_command(
        "pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/all --cov-report=xml:coverage.xml --cov-fail-under=85",
        "All tests with comprehensive coverage"
    )
    
    # Generate coverage report
    print("\n📈 Generating coverage report...")
    coverage_success = run_command(
        "coverage report --show-missing",
        "Coverage report"
    )
    
    # Run specific test categories with markers
    print("\n🏷️ Running tests by category...")
    
    # Unit tests only
    run_command("pytest -m unit -v", "Unit tests only")
    
    # Integration tests only
    run_command("pytest -m integration -v", "Integration tests only")
    
    # E2E tests only
    run_command("pytest -m e2e -v", "E2E tests only")
    
    # Authentication tests
    run_command("pytest -m auth -v", "Authentication tests only")
    
    # Products tests
    run_command("pytest -m products -v", "Products tests only")
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    if unit_success:
        print("✅ Unit tests: PASSED")
    else:
        print("❌ Unit tests: FAILED")
    
    if integration_success:
        print("✅ Integration tests: PASSED")
    else:
        print("❌ Integration tests: FAILED")
    
    if e2e_success:
        print("✅ E2E tests: PASSED")
    else:
        print("❌ E2E tests: FAILED")
    
    if all_tests_success:
        print("✅ All tests: PASSED")
        print("🎉 Coverage target (85%) achieved!")
    else:
        print("❌ Some tests failed or coverage target not met")
    
    print(f"\n📁 Coverage reports generated in:")
    print(f"   - htmlcov/unit/ (Unit tests)")
    print(f"   - htmlcov/integration/ (Integration tests)")
    print(f"   - htmlcov/e2e/ (E2E tests)")
    print(f"   - htmlcov/all/ (All tests)")
    print(f"   - coverage.xml (XML format)")
    
    print(f"\n🔍 To view HTML coverage reports:")
    print(f"   - Unit: open htmlcov/unit/index.html")
    print(f"   - Integration: open htmlcov/integration/index.html")
    print(f"   - E2E: open htmlcov/e2e/index.html")
    print(f"   - All: open htmlcov/all/index.html")
    
    return 0 if all_tests_success else 1


if __name__ == "__main__":
    sys.exit(main())
