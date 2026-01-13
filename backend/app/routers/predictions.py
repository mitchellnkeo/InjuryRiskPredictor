"""
Prediction API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging

from ..models import PredictionRequest, PredictionResponse, ModelInfoResponse
from ..ml.predictor import get_predictor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["predictions"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_injury_risk(request: PredictionRequest):
    """
    Predict injury risk from training data.
    
    Requires:
    - Athlete profile (age, experience, baseline load)
    - Training history (at least 4 weeks recommended for accurate ACWR)
    
    Returns:
    - Risk level (LOW, MODERATE, HIGH)
    - Risk score (0-1 probability)
    - Key metrics (ACWR, monotony, strain)
    - Personalized recommendations
    """
    try:
        predictor = get_predictor()
        
        # Convert Pydantic models to dictionaries
        athlete_dict = request.athlete.dict()
        training_list = [week.dict() for week in request.training_history]
        
        logger.info(f"Making prediction for athlete age={athlete_dict['age']}, weeks={len(training_list)}")
        
        # Make prediction
        result = predictor.predict(training_list, athlete_dict)
        
        logger.info(f"Prediction successful: risk_level={result['risk_level']}, risk_score={result['risk_score']:.3f}")
        
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.error(f"Validation error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """
    Get information about the loaded ML model.
    
    Returns:
    - Model type
    - Features used
    - Model parameters
    """
    try:
        predictor = get_predictor()
        info = predictor.get_model_info()
        
        return ModelInfoResponse(
            model_type=info.get("model_type", "Unknown"),
            features=info.get("features", []),
            accuracy=None,  # Could be stored in model metadata
            recall=None,  # Could be stored in model metadata
            last_trained=None  # Could be stored in model metadata
        )
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
