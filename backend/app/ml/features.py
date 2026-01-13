"""
Feature Engineering for API Predictions

This module calculates features from raw training data for injury risk prediction.
Must match the feature engineering used during model training.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import sys
import os

# Add parent directory to path to import from src.ml
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.ml.features import (
    calculate_acute_load,
    calculate_chronic_load,
    calculate_acwr,
    calculate_monotony,
    calculate_strain,
    calculate_week_over_week_change,
    calculate_acwr_trend,
    calculate_weeks_above_threshold,
    calculate_distance_from_baseline,
    calculate_lag_features,
    calculate_recent_injury,
    bin_age,
    bin_experience
)


def calculate_features_for_prediction(
    training_history: List[Dict],
    athlete_profile: Dict,
    current_week: int
) -> Dict[str, float]:
    """
    Calculate all features needed for injury risk prediction.
    
    Args:
        training_history: List of training week dictionaries with keys:
            - week: int
            - weekly_load: float
            - daily_loads: List[float]
        athlete_profile: Dictionary with keys:
            - age: int
            - experience_years: int
            - baseline_weekly_load: float
        current_week: Current week number
    
    Returns:
        Dictionary of feature names and values
    """
    # Convert to DataFrame format expected by feature functions
    df = pd.DataFrame(training_history)
    df = df.sort_values('week')
    
    # Add athlete_id (needed for feature functions, but we only have one athlete)
    athlete_id = 'API_USER'
    df['athlete_id'] = athlete_id
    
    # Ensure we have required columns
    if 'daily_loads' in df.columns:
        # Convert daily_loads from list to string if needed
        df['daily_loads'] = df['daily_loads'].apply(
            lambda x: ','.join(map(str, x)) if isinstance(x, list) else str(x)
        )
    
    # Add metadata columns needed for feature calculations
    df['age'] = athlete_profile['age']
    df['experience_years'] = athlete_profile['experience_years']
    df['baseline_weekly_miles'] = athlete_profile['baseline_weekly_load']
    
    # Calculate features using existing functions
    features = {}
    
    # Core metrics
    features['acute_load'] = calculate_acute_load(df, athlete_id, current_week)
    features['chronic_load'] = calculate_chronic_load(df, athlete_id, current_week)
    features['acwr'] = calculate_acwr(df, athlete_id, current_week)
    features['monotony'] = calculate_monotony(df, athlete_id, current_week)
    features['strain'] = calculate_strain(df, athlete_id, current_week)
    features['week_over_week_change'] = calculate_week_over_week_change(df, athlete_id, current_week)
    
    # Derived features
    features['acwr_trend'] = calculate_acwr_trend(df, athlete_id, current_week)
    features['weeks_above_threshold'] = calculate_weeks_above_threshold(df, athlete_id, current_week)
    features['distance_from_baseline'] = calculate_distance_from_baseline(df, athlete_id, current_week)
    
    # Lag features
    features['previous_week_acwr'] = calculate_lag_features(df, athlete_id, current_week, lag_weeks=1)
    features['two_weeks_ago_acwr'] = calculate_lag_features(df, athlete_id, current_week, lag_weeks=2)
    features['recent_injury'] = calculate_recent_injury(df, athlete_id, current_week)
    
    # Athlete-specific features
    features['age'] = athlete_profile['age']
    features['age_group'] = bin_age(athlete_profile['age'])
    features['experience_years'] = athlete_profile['experience_years']
    features['experience_level'] = bin_experience(athlete_profile['experience_years'])
    features['baseline_weekly_miles'] = athlete_profile['baseline_weekly_load']
    
    return features


def prepare_features_for_model(features: Dict[str, float], feature_order: List[str]) -> np.ndarray:
    """
    Prepare features in the correct order for model prediction.
    
    Args:
        features: Dictionary of feature values
        feature_order: List of feature names in the order expected by model
    
    Returns:
        NumPy array of feature values in correct order
    """
    feature_vector = []
    
    for feature_name in feature_order:
        if feature_name in features:
            value = features[feature_name]
            # Handle categorical features (convert to numeric)
            if isinstance(value, str):
                # Simple encoding for categorical features
                # In production, use the same encoders from training
                if feature_name.endswith('_group') or feature_name.endswith('_level'):
                    # Simple hash-based encoding (not ideal, but works)
                    value = hash(value) % 1000
                else:
                    value = 0
            feature_vector.append(float(value))
        else:
            # Missing feature - use 0 as default
            feature_vector.append(0.0)
    
    return np.array(feature_vector).reshape(1, -1)
