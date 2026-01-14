"""
Test script for Injury Risk Predictor API

Tests the prediction endpoint with sample data.
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("=" * 60)
    print("Testing Health Check Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("model_loaded"):
            print("✓ Model is loaded successfully")
        else:
            print("⚠ Model is not loaded")
    
    print()

def test_prediction():
    """Test the prediction endpoint."""
    print("=" * 60)
    print("Testing Prediction Endpoint")
    print("=" * 60)
    
    # Sample request data
    request_data = {
        "athlete": {
            "age": 30,
            "experience_years": 5,
            "baseline_weekly_load": 25.0
        },
        "training_history": [
            {
                "week": 1,
                "weekly_load": 20.0,
                "daily_loads": [3.0, 4.0, 0.0, 5.0, 0.0, 4.0, 4.0]
            },
            {
                "week": 2,
                "weekly_load": 22.0,
                "daily_loads": [3.5, 4.5, 0.0, 5.5, 0.0, 4.5, 4.0]
            },
            {
                "week": 3,
                "weekly_load": 24.0,
                "daily_loads": [4.0, 5.0, 0.0, 6.0, 0.0, 5.0, 4.0]
            },
            {
                "week": 4,
                "weekly_load": 26.0,
                "daily_loads": [4.5, 5.5, 0.0, 6.5, 0.0, 5.5, 4.0]
            },
            {
                "week": 5,
                "weekly_load": 35.0,  # Large spike!
                "daily_loads": [6.0, 7.0, 0.0, 8.0, 0.0, 7.0, 7.0]
            }
        ]
    }
    
    print("Request Data:")
    print(json.dumps(request_data, indent=2))
    print()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ Prediction Successful!")
            print("\nPrediction Results:")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Risk Score: {result['risk_score']:.3f} ({result['risk_score']*100:.1f}%)")
            print(f"  ACWR: {result['acwr']:.3f}")
            print(f"  Monotony: {result.get('monotony', 'N/A')}")
            print(f"  Strain: {result.get('strain', 'N/A')}")
            print(f"  Week-over-Week Change: {result.get('week_over_week_change', 'N/A')}")
            
            print("\nRecommendations:")
            for i, rec in enumerate(result.get('recommendations', []), 1):
                print(f"  {i}. {rec}")
            
            if result.get('feature_contributions'):
                print("\nTop Feature Contributions:")
                for feature, importance in result['feature_contributions'].items():
                    print(f"  {feature}: {importance:.3f}")
        else:
            print(f"\n✗ Prediction Failed")
            print(f"Response: {response.text}")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                pass
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_model_info():
    """Test the model info endpoint."""
    print("\n" + "=" * 60)
    print("Testing Model Info Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/model/info")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print("\nModel Information:")
            print(f"  Model Type: {info['model_type']}")
            print(f"  Number of Features: {len(info['features'])}")
            print(f"  Features: {', '.join(info['features'][:10])}...")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Injury Risk Predictor API Test Suite")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  python3 -m uvicorn app.main:app --reload --port 8000")
    print()
    
    # Test health check
    test_health_check()
    
    # Test prediction
    test_prediction()
    
    # Test model info
    test_model_info()
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)
