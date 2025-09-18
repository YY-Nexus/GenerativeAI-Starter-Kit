FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy source code
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/
COPY examples/ examples/
COPY notebooks/ notebooks/
COPY docs/ docs/

# Copy configuration files
COPY .env.example .env
COPY README.md .

# Create necessary directories
RUN mkdir -p data/vector_stores data/sample_datasets logs outputs

# Set Python path
ENV PYTHONPATH=/app/src

# Expose port for web services
EXPOSE 8000

# Default command
CMD ["bash"]