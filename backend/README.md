# Injury Risk Predictor API

FastAPI backend for injury risk prediction using ML models.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Ensure model files exist:**
   - `models/random_forest_model.pkl` (or similar)
   - `models/scaler.pkl`
   
   These should be copied from the root `models/` directory.

## Running the API

### Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
```
GET /health
```
Returns API status and whether model is loaded.

### Predict Injury Risk
```
POST /api/predict
```
Predicts injury risk from training data.

**Request Body:**
```json
{
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
    }
    // ... more weeks (at least 4 recommended)
  ]
}
```

**Response:**
```json
{
  "risk_level": "MODERATE",
  "risk_score": 0.45,
  "acwr": 1.35,
  "monotony": 1.2,
  "strain": 88.5,
  "week_over_week_change": 0.1,
  "recommendations": [
    "⚠️ MODERATE RISK: ACWR is elevated. Consider reducing volume by 10-15%.",
    "✅ You're in a low-risk zone. Continue your current training plan."
  ],
  "feature_contributions": {
    "week_over_week_change": 0.26,
    "strain": 0.18,
    "acwr": 0.15
  }
}
```

### Model Info
```
GET /api/model/info
```
Returns information about the loaded ML model.

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/health

# Prediction (with sample data)
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic schemas
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── predictor.py    # Prediction service
│   │   └── features.py     # Feature engineering
│   └── routers/
│       ├── __init__.py
│       └── predictions.py   # API routes
├── models/                  # ML model files
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── requirements.txt
└── README.md
```
