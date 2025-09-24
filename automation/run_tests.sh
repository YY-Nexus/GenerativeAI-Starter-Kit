#!/bin/bash

# Test Runner Script for GenerativeAI Starter Kit
# This script runs all tests and generates coverage reports

set -e

echo "🧪 Running GenerativeAI Starter Kit Test Suite"
echo "============================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing..."
    pip install pytest pytest-cov
fi

# Create logs directory
mkdir -p logs

# Run tests with coverage
echo "🔍 Running tests with coverage..."
pytest tests/ \
    --verbose \
    --cov=examples \
    --cov=automation \
    --cov-report=html:logs/coverage_html \
    --cov-report=term-missing \
    --junit-xml=logs/test_results.xml \
    --tb=short

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in logs/coverage_html/"
    echo "📋 Test results saved to logs/test_results.xml"
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
    exit 1
fi

# Run code quality checks if tools are available
echo ""
echo "🔍 Running code quality checks..."

# Black code formatting check
if command -v black &> /dev/null; then
    echo "📝 Checking code formatting with black..."
    black --check --diff examples/ automation/ tests/ || echo "⚠️ Code formatting issues found"
else
    echo "⚠️ black not installed, skipping formatting check"
fi

# Flake8 linting
if command -v flake8 &> /dev/null; then
    echo "🔍 Running flake8 linting..."
    flake8 examples/ automation/ tests/ --max-line-length=100 --extend-ignore=E203,W503 || echo "⚠️ Linting issues found"
else
    echo "⚠️ flake8 not installed, skipping linting check"
fi

echo ""
echo "🎉 Test suite completed!"
echo "📖 Check logs/ directory for detailed reports"
