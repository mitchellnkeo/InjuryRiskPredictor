"""
Injury Risk Prediction Service

Loads trained model and makes predictions on new training data.
"""

import pickle
import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from .features import calculate_features_for_prediction, prepare_features_for_model
from src.ml.preprocessing import encode_categorical_features

logger = logging.getLogger(__name__)


class InjuryPredictor:
    """Service for predicting injury risk from training data."""
    
    def __init__(self, models_dir: str = None):
        """
        Initialize predictor by loading model and scaler.
        
        Args:
            models_dir: Directory containing model files (default: backend/models)
        """
        if models_dir is None:
            # Default to backend/models relative to this file
            models_dir = os.path.join(
                os.path.dirname(__file__), 
                '../../models'
            )
        
        self.models_dir = models_dir
        self.model = None
        self.scaler = None
        self.feature_order = None
        self.encoders = {}
        
        self._load_model()
        self._load_scaler()
        self._determine_feature_order()
    
    def _load_model(self):
        """Load the trained ML model."""
        try:
            # Try to find model file
            model_files = [f for f in os.listdir(self.models_dir) 
                          if f.endswith('_model.pkl')]
            
            if not model_files:
                raise FileNotFoundError(f"No model file found in {self.models_dir}")
            
            # Load first model found (or could be more specific)
            model_path = os.path.join(self.models_dir, model_files[0])
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info(f"Loaded model from {model_path}")
            logger.info(f"Model type: {type(self.model).__name__}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _load_scaler(self):
        """Load the feature scaler."""
        try:
            scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
            
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            logger.info(f"Loaded scaler from {scaler_path}")
            
        except Exception as e:
            logger.error(f"Error loading scaler: {e}")
            raise
    
    def _determine_feature_order(self):
        """Determine the order of features expected by the model."""
        # Try to get feature names from model or scaler
        if hasattr(self.scaler, 'feature_names_in_'):
            self.feature_order = list(self.scaler.feature_names_in_)
        elif hasattr(self.model, 'feature_names_in_'):
            self.feature_order = list(self.model.feature_names_in_)
        else:
            # Fallback: use a standard feature order based on training
            # This should match the order used during training
            self.feature_order = [
                'acute_load', 'chronic_load', 'acwr', 'monotony', 'strain',
                'week_over_week_change', 'acwr_trend', 'weeks_above_threshold',
                'distance_from_baseline', 'previous_week_acwr', 'two_weeks_ago_acwr',
                'recent_injury', 'age', 'age_group', 'experience_years',
                'experience_level', 'baseline_weekly_miles'
            ]
            logger.warning("Using default feature order - may not match training")
    
    def predict(self, training_history: List[Dict], athlete_profile: Dict) -> Dict:
        """
        Predict injury risk from training data.
        
        Args:
            training_history: List of training week dictionaries
            athlete_profile: Athlete profile dictionary
        
        Returns:
            Dictionary with prediction results
        """
        if not training_history:
            raise ValueError("Training history cannot be empty")
        
        # Get current week (last week in history)
        current_week = max(week['week'] for week in training_history)
        
        # Calculate features
        features = calculate_features_for_prediction(
            training_history,
            athlete_profile,
            current_week
        )
        
        # Prepare features for model (in correct order)
        feature_vector = prepare_features_for_model(features, self.feature_order)
        
        # Encode categorical features if needed
        # Create a DataFrame for encoding
        feature_df = pd.DataFrame([features])
        feature_df_encoded, encoders = encode_categorical_features(feature_df)
        
        # Reorder encoded features
        encoded_features = []
        for feature_name in self.feature_order:
            if feature_name in feature_df_encoded.columns:
                encoded_features.append(float(feature_df_encoded[feature_name].iloc[0]))
            else:
                encoded_features.append(0.0)
        
        feature_array = np.array(encoded_features).reshape(1, -1)
        
        # Scale features
        feature_scaled = self.scaler.transform(feature_array)
        
        # Predict
        if hasattr(self.model, 'predict_proba'):
            risk_prob = self.model.predict_proba(feature_scaled)[0][1]
        else:
            # Fallback for models without predict_proba
            prediction = self.model.predict(feature_scaled)[0]
            risk_prob = float(prediction)
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_prob)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(features, risk_prob)
        
        # Get feature contributions (if available)
        feature_contributions = self._get_feature_contributions(feature_scaled, features)
        
        return {
            "risk_level": risk_level,
            "risk_score": float(risk_prob),
            "acwr": features.get('acwr', 0.0),
            "monotony": features.get('monotony', 0.0),
            "strain": features.get('strain', 0.0),
            "week_over_week_change": features.get('week_over_week_change', 0.0),
            "recommendations": recommendations,
            "feature_contributions": feature_contributions
        }
    
    def _get_risk_level(self, prob: float) -> str:
        """Convert probability to risk level."""
        if prob < 0.3:
            return "LOW"
        elif prob < 0.6:
            return "MODERATE"
        else:
            return "HIGH"
    
    def _generate_recommendations(self, features: Dict, risk_prob: float) -> List[str]:
        """Generate personalized training recommendations."""
        recommendations = []
        
        acwr = features.get('acwr', 0.0)
        monotony = features.get('monotony', 0.0)
        week_change = features.get('week_over_week_change', 0.0)
        strain = features.get('strain', 0.0)
        
        # ACWR-based recommendations
        if acwr > 1.5:
            recommendations.append("⚠️ HIGH RISK: ACWR is above 1.5. Reduce training volume by 20-30% this week.")
        elif acwr > 1.3:
            recommendations.append("⚠️ MODERATE RISK: ACWR is elevated. Consider reducing volume by 10-15%.")
        elif acwr < 0.8:
            recommendations.append("ℹ️ ACWR is low. You may be undertrained. Consider gradual volume increase.")
        else:
            recommendations.append("✅ ACWR is in the optimal range (0.8-1.3). Keep up the good work!")
        
        # Week-over-week change recommendations
        if week_change > 0.2:
            recommendations.append("⚠️ Large week-over-week increase detected. Maintain current volume to avoid injury risk.")
        elif week_change > 0.15:
            recommendations.append("ℹ️ Moderate week-over-week increase. Monitor for any signs of overuse.")
        
        # Monotony recommendations
        if monotony > 2.0:
            recommendations.append("💡 High training monotony detected. Add variety to your training routine.")
        
        # Strain recommendations
        if strain > 150:
            recommendations.append("⚠️ High training strain. Ensure adequate recovery between sessions.")
        
        # Overall risk recommendations
        if risk_prob < 0.3:
            recommendations.append("✅ You're in a low-risk zone. Continue your current training plan.")
        elif risk_prob > 0.7:
            recommendations.append("🚨 HIGH INJURY RISK: Consider taking a deload week or consulting a sports medicine professional.")
        
        return recommendations
    
    def _get_feature_contributions(self, feature_scaled: np.ndarray, features: Dict) -> Optional[Dict[str, float]]:
        """Get feature importance contributions (if model supports it)."""
        contributions = {}
        
        # For tree-based models, get feature importances
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            # Get top 5 features
            top_indices = np.argsort(importances)[-5:][::-1]
            
            for idx in top_indices:
                if idx < len(self.feature_order):
                    feature_name = self.feature_order[idx]
                    contributions[feature_name] = float(importances[idx])
        
        return contributions if contributions else None
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        info = {
            "model_type": type(self.model).__name__,
            "features": self.feature_order,
            "model_loaded": self.model is not None,
            "scaler_loaded": self.scaler is not None
        }
        
        # Try to get model attributes if available
        if hasattr(self.model, 'n_estimators'):
            info["n_estimators"] = self.model.n_estimators
        if hasattr(self.model, 'max_depth'):
            info["max_depth"] = self.model.max_depth
        
        return info
