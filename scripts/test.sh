#!/bin/bash

# ============================================
# 🧪 Test Runner Script
# 用于运行所有测试并生成报告
# ============================================

set -e

echo "🔍 Running tests with pytest..."
pytest tests/ --maxfail=3 --disable-warnings --tb=short

echo "✅ All tests completed!"
