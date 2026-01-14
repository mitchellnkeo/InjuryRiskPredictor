#!/bin/bash
# Test Docker build locally before deploying
# Run this script from the backend/ directory
# 
# NOTE: Docker Desktop must be installed and running
# Download from: https://www.docker.com/products/docker-desktop/

set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "Please install Docker Desktop:"
    echo "  https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "Or skip local testing and deploy directly to Railway/Render"
    echo "  (they will build the Docker image automatically)"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "🐳 Testing Docker build for backend API..."
echo ""

# Build the Docker image (from project root)
echo "📦 Building Docker image..."
cd ..
docker build -t injury-api -f backend/Dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

echo ""
echo "🚀 Starting container..."
echo "   API will be available at http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

# Run the container
docker run -p 8000:8000 -e PORT=8000 injury-api
