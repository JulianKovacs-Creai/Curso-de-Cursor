#!/usr/bin/env python3
"""
Test Runner for Authentication Examples

This script provides comprehensive test execution with coverage reporting,
performance metrics, and detailed reporting.

Target: >85% coverage with comprehensive testing
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any


def run_command(command: List[str], description: str) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"\n🔧 {description}")
    print(f"Command: {' '.join(command)}")
    print("-" * 50)
    
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    return result


def install_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    
    # Install requirements
    result = run_command(
        ["pip", "install", "-r", "requirements-test.txt"],
        "Installing test dependencies"
    )
    
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        return False
    
    print("✅ Dependencies installed successfully")
    return True


def run_unit_tests():
    """Run unit tests."""
    print("\n🧪 Running Unit Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_unit_comprehensive.py",
            "-m", "unit",
            "-v",
            "--tb=short"
        ],
        "Unit Tests"
    )
    
    return result.returncode == 0


def run_integration_tests():
    """Run integration tests."""
    print("\n🔗 Running Integration Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_integration.py",
            "-m", "integration",
            "-v",
            "--tb=short"
        ],
        "Integration Tests"
    )
    
    return result.returncode == 0


def run_e2e_tests():
    """Run end-to-end tests."""
    print("\n🌐 Running End-to-End Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_e2e.py",
            "-m", "e2e",
            "-v",
            "--tb=short"
        ],
        "End-to-End Tests"
    )
    
    return result.returncode == 0


def run_mocking_tests():
    """Run mocking tests."""
    print("\n🎭 Running Mocking Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_mocking.py",
            "-m", "mocking",
            "-v",
            "--tb=short"
        ],
        "Mocking Tests"
    )
    
    return result.returncode == 0


def run_all_tests():
    """Run all tests with coverage."""
    print("\n🚀 Running All Tests with Coverage...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_*.py",
            "-v",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml:coverage.xml",
            "--cov-fail-under=85",
            "--junitxml=test-results.xml",
            "--html=test-report.html",
            "--self-contained-html"
        ],
        "All Tests with Coverage"
    )
    
    return result.returncode == 0


def run_performance_tests():
    """Run performance tests."""
    print("\n⚡ Running Performance Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_*.py",
            "-m", "performance",
            "-v",
            "--benchmark-only",
            "--benchmark-sort=mean"
        ],
        "Performance Tests"
    )
    
    return result.returncode == 0


def run_security_tests():
    """Run security tests."""
    print("\n🔒 Running Security Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_*.py",
            "-m", "security",
            "-v",
            "--tb=short"
        ],
        "Security Tests"
    )
    
    return result.returncode == 0


def run_slow_tests():
    """Run slow tests."""
    print("\n🐌 Running Slow Tests...")
    
    result = run_command(
        [
            "python", "-m", "pytest",
            "test_*.py",
            "-m", "slow",
            "-v",
            "--tb=short",
            "--timeout=600"
        ],
        "Slow Tests"
    )
    
    return result.returncode == 0


def generate_coverage_report():
    """Generate detailed coverage report."""
    print("\n📊 Generating Coverage Report...")
    
    result = run_command(
        [
            "python", "-m", "coverage", "html",
            "--directory=htmlcov",
            "--title=Authentication Examples Coverage Report"
        ],
        "Coverage Report"
    )
    
    if result.returncode == 0:
        print("✅ Coverage report generated: htmlcov/index.html")
    
    return result.returncode == 0


def run_linting():
    """Run code linting."""
    print("\n🔍 Running Code Linting...")
    
    # Run flake8
    flake8_result = run_command(
        ["python", "-m", "flake8", ".", "--max-line-length=100"],
        "Flake8 Linting"
    )
    
    # Run black check
    black_result = run_command(
        ["python", "-m", "black", "--check", "."],
        "Black Format Check"
    )
    
    # Run isort check
    isort_result = run_command(
        ["python", "-m", "isort", "--check-only", "."],
        "Import Sort Check"
    )
    
    return all([
        flake8_result.returncode == 0,
        black_result.returncode == 0,
        isort_result.returncode == 0
    ])


def run_security_scan():
    """Run security scanning."""
    print("\n🛡️ Running Security Scan...")
    
    # Run bandit
    bandit_result = run_command(
        ["python", "-m", "bandit", "-r", ".", "-f", "json", "-o", "bandit-report.json"],
        "Bandit Security Scan"
    )
    
    # Run safety
    safety_result = run_command(
        ["python", "-m", "safety", "check", "--json", "--output", "safety-report.json"],
        "Safety Dependency Scan"
    )
    
    return bandit_result.returncode == 0 and safety_result.returncode == 0


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Authentication Examples Test Runner")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--mocking", action="store_true", help="Run mocking tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--slow", action="store_true", help="Run slow tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--lint", action="store_true", help="Run linting")
    parser.add_argument("--scan", action="store_true", help="Run security scan")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    
    args = parser.parse_args()
    
    print("🧪 Authentication Examples Test Runner")
    print("=" * 50)
    
    success = True
    
    # Install dependencies if requested
    if args.install or args.full:
        if not install_dependencies():
            success = False
    
    # Run specific test types
    if args.unit:
        if not run_unit_tests():
            success = False
    
    if args.integration:
        if not run_integration_tests():
            success = False
    
    if args.e2e:
        if not run_e2e_tests():
            success = False
    
    if args.mocking:
        if not run_mocking_tests():
            success = False
    
    if args.performance:
        if not run_performance_tests():
            success = False
    
    if args.security:
        if not run_security_tests():
            success = False
    
    if args.slow:
        if not run_slow_tests():
            success = False
    
    # Run all tests if requested
    if args.all or args.full:
        if not run_all_tests():
            success = False
    
    # Generate coverage report if requested
    if args.coverage or args.full:
        if not generate_coverage_report():
            success = False
    
    # Run linting if requested
    if args.lint or args.full:
        if not run_linting():
            success = False
    
    # Run security scan if requested
    if args.scan or args.full:
        if not run_security_scan():
            success = False
    
    # Default: run all tests if no specific option provided
    if not any([args.unit, args.integration, args.e2e, args.mocking, 
                args.performance, args.security, args.slow, args.all, 
                args.coverage, args.lint, args.scan, args.full]):
        print("No specific test type selected. Running all tests...")
        if not run_all_tests():
            success = False
    
    # Print results
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests completed successfully!")
        print("📊 Coverage target: >85%")
        print("📁 Reports generated:")
        print("   - HTML Coverage: htmlcov/index.html")
        print("   - XML Coverage: coverage.xml")
        print("   - Test Results: test-results.xml")
        print("   - Test Report: test-report.html")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
