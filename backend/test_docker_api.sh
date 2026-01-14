#!/bin/bash
# Test Docker container API endpoints
# Run this after starting the Docker container

set -e

API_URL="http://localhost:8000"

echo "🧪 Testing Docker container API..."
echo ""

# Test 1: Health Check
echo "1️⃣ Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s "$API_URL/health")
echo "$HEALTH_RESPONSE" | python3 -m json.tool
echo ""

# Check if model is loaded
if echo "$HEALTH_RESPONSE" | grep -q '"model_loaded": true'; then
    echo "✅ Model loaded successfully!"
else
    echo "⚠️  Model not loaded - check logs"
fi
echo ""

# Test 2: Root endpoint
echo "2️⃣ Testing root endpoint..."
curl -s "$API_URL/" | python3 -m json.tool
echo ""

# Test 3: Model Info
echo "3️⃣ Testing /api/model/info endpoint..."
curl -s "$API_URL/api/model/info" | python3 -m json.tool
echo ""

# Test 4: API Docs (check if accessible)
echo "4️⃣ Checking API documentation..."
if curl -s -o /dev/null -w "%{http_code}" "$API_URL/docs" | grep -q "200"; then
    echo "✅ API docs accessible at: $API_URL/docs"
else
    echo "⚠️  API docs not accessible"
fi
echo ""

# Test 5: Prediction endpoint (if test_request.json exists)
if [ -f "test_request.json" ]; then
    echo "5️⃣ Testing /api/predict endpoint..."
    PREDICTION_RESPONSE=$(curl -s -X POST "$API_URL/api/predict" \
        -H "Content-Type: application/json" \
        -d @test_request.json)
    
    if echo "$PREDICTION_RESPONSE" | grep -q "risk_level"; then
        echo "$PREDICTION_RESPONSE" | python3 -m json.tool
        echo "✅ Prediction endpoint working!"
    else
        echo "⚠️  Prediction endpoint error:"
        echo "$PREDICTION_RESPONSE" | python3 -m json.tool
    fi
else
    echo "5️⃣ Skipping prediction test (test_request.json not found)"
fi

echo ""
echo "✅ All tests complete!"
echo ""
echo "📝 Next steps:"
echo "   - Check Docker Desktop logs for any warnings"
echo "   - Visit $API_URL/docs for interactive API documentation"
echo "   - If all tests pass, you're ready to deploy!"
