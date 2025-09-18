#!/bin/bash

# GenerativeAI Starter Kit Setup Script
# This script sets up the development environment for the starter kit

set -e

echo "🚀 Setting up GenerativeAI Starter Kit..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version is not compatible. Requires Python >= $required_version"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "🔤 Downloading NLTK data..."
python3 -c "
import nltk
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    print('✅ NLTK data downloaded successfully')
except Exception as e:
    print(f'⚠️ Warning: Could not download NLTK data: {e}')
"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/{raw,processed}
mkdir -p models/checkpoints
mkdir -p logs
mkdir -p outputs

# Set up environment file
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cat > .env << EOL
# API Keys (fill in your own)
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Model settings
DEVICE=cpu
MODEL_CACHE_DIR=./models

# Logging
LOG_LEVEL=INFO
EOL
    echo "⚠️ Please edit .env file with your API keys"
fi

echo "🎉 Setup complete! Run 'source venv/bin/activate' to activate the environment"
echo "📖 Check the README.md and docs/ folder for usage instructions"