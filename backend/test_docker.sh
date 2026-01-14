#!/bin/bash
# Test Docker build locally before deploying

set -e

echo "🐳 Testing Docker build for backend API..."
echo ""

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t injury-api -f Dockerfile ..

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
