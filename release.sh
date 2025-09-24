#!/bin/bash

set -e

echo "🔧 Bumping version..."
bump-my-version patch

echo "🧪 Running tests..."
pytest

echo "📦 Building package..."
python setup.py sdist bdist_wheel

echo "🚀 Publishing to PyPI..."
twine upload dist/*

echo "✅ Done. Version bumped, package published, tag created."
