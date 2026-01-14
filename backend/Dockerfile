# Backend Dockerfile for Injury Risk Predictor API

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
# Build context is project root, so backend/requirements.txt
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app/ ./app/
COPY backend/models/ ./models/

# Copy src directory (needed for ML feature engineering imports)
# Build context is project root, so src/ is at same level as backend/
COPY src/ ./src/

# Set Python path to include current directory
ENV PYTHONPATH=/app:$PYTHONPATH

# Expose port (can be overridden by PORT env var)
EXPOSE 8000

# Run the application
# Use PORT environment variable if set (for Railway/Render)
# Default to 8000 if PORT is not set
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
