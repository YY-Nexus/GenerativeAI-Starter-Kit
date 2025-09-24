#!/bin/bash

# ============================================
# 🧹 Linting & Formatting Script
# 用于自动清理格式、检查语法、统一代码风格
# ============================================

set -e

echo "🔍 Running pre-commit hooks..."
pre-commit run --all-files

echo "🎨 Running black for auto-formatting..."
black .

echo "🔎 Running flake8 for style checks..."
flake8 . --max-line-length=88 --show-source --statistics

echo "✅ Linting complete!"
