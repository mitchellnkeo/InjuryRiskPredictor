"""
Pydantic Models for API Request/Response Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TrainingWeek(BaseModel):
    """Represents a single week of training data."""
    week: int = Field(..., ge=1, description="Week number")
    weekly_load: float = Field(..., gt=0, description="Total weekly training load (miles)")
    daily_loads: List[float] = Field(..., min_items=1, description="Daily training loads for the week")


class AthleteProfile(BaseModel):
    """Athlete demographic and baseline information."""
    age: int = Field(..., ge=18, le=100, description="Athlete age")
    experience_years: int = Field(..., ge=0, description="Years of training experience")
    baseline_weekly_load: float = Field(..., gt=0, description="Baseline weekly training load (miles)")


class PredictionRequest(BaseModel):
    """Request body for injury risk prediction."""
    athlete: AthleteProfile = Field(..., description="Athlete profile information")
    training_history: List[TrainingWeek] = Field(..., min_items=1, description="Historical training data (at least 4 weeks recommended)")


class PredictionResponse(BaseModel):
    """Response body for injury risk prediction."""
    risk_level: str = Field(..., description="Risk level: LOW, MODERATE, or HIGH")
    risk_score: float = Field(..., ge=0, le=1, description="Injury risk probability (0-1)")
    acwr: float = Field(..., description="Acute:Chronic Workload Ratio")
    monotony: Optional[float] = Field(None, description="Training monotony score")
    strain: Optional[float] = Field(None, description="Training strain score")
    week_over_week_change: Optional[float] = Field(None, description="Week-over-week load change percentage")
    recommendations: List[str] = Field(default_factory=list, description="Personalized training recommendations")
    feature_contributions: Optional[Dict[str, float]] = Field(None, description="Top feature contributions to risk score")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    version: str = Field(default="1.0.0", description="API version")


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_type: str = Field(..., description="Type of ML model")
    accuracy: Optional[float] = Field(None, description="Model accuracy")
    recall: Optional[float] = Field(None, description="Model recall")
    features: List[str] = Field(..., description="List of features used by model")
    last_trained: Optional[str] = Field(None, description="Date model was last trained")
