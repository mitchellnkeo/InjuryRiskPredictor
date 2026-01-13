"""
Model Definitions for Injury Risk Predictor

Includes baseline rule-based model and ML model configurations.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("Warning: XGBoost not available. Install with: pip install xgboost")


class BaselineModel:
    """
    Rule-based baseline model using ACWR thresholds from research.
    
    This is a simple heuristic model that doesn't use ML - just applies
    research-based rules to establish a baseline to beat.
    """
    
    def __init__(self):
        self.name = "Baseline (Rule-Based)"
    
    def predict(self, X):
        """
        Predict injury risk based on ACWR thresholds.
        
        Args:
            X: Feature matrix (must include 'acwr' column or index)
        
        Returns:
            Array of predictions (0 = low risk, 1 = high risk)
        """
        # Convert to numpy array if needed
        if hasattr(X, 'values'):
            X_array = X.values
        else:
            X_array = np.array(X)
        
        # If X is DataFrame, try to get ACWR column
        if hasattr(X, 'columns'):
            if 'acwr' in X.columns:
                acwr = X['acwr'].values
            else:
                # Try to find ACWR in column names (case-insensitive)
                acwr_cols = [col for col in X.columns if 'acwr' in col.lower()]
                if acwr_cols:
                    acwr = X[acwr_cols[0]].values
                else:
                    # Fallback: use first column
                    acwr = X_array[:, 0] if X_array.ndim > 1 else X_array
        else:
            # Assume ACWR is first feature
            acwr = X_array[:, 0] if X_array.ndim > 1 else X_array
        
        # Ensure acwr is 1D array
        acwr = np.array(acwr).flatten()
        
        # Rule-based prediction: ACWR > 1.5 = high risk
        predictions = (acwr > 1.5).astype(int)
        
        return predictions
    
    def predict_proba(self, X):
        """
        Predict injury probabilities.
        
        Args:
            X: Feature matrix
        
        Returns:
            Array of probabilities [prob_low_risk, prob_high_risk]
        """
        predictions = self.predict(X)
        
        # Convert to probabilities (simple mapping)
        proba = np.zeros((len(predictions), 2))
        for i, pred in enumerate(predictions):
            if pred == 1:  # High risk
                proba[i] = [0.3, 0.7]  # 70% chance of injury
            else:  # Low risk
                proba[i] = [0.85, 0.15]  # 15% chance of injury
        
        return proba


def create_logistic_regression(class_weight='balanced', random_state=42):
    """
    Create Logistic Regression model.
    
    Args:
        class_weight: How to handle class imbalance ('balanced' recommended)
        random_state: Random seed
    
    Returns:
        LogisticRegression model
    """
    return LogisticRegression(
        class_weight=class_weight,
        max_iter=1000,
        random_state=random_state,
        solver='lbfgs'  # Good default solver
    )


def create_random_forest(n_estimators=100, max_depth=10, min_samples_split=20,
                         class_weight='balanced', random_state=42):
    """
    Create Random Forest model.
    
    Args:
        n_estimators: Number of trees
        max_depth: Maximum tree depth
        min_samples_split: Minimum samples to split
        class_weight: How to handle class imbalance
        random_state: Random seed
    
    Returns:
        RandomForestClassifier model
    """
    return RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        class_weight=class_weight,
        random_state=random_state,
        n_jobs=-1  # Use all CPU cores
    )


def create_xgboost(n_estimators=100, max_depth=6, learning_rate=0.1,
                   scale_pos_weight=3, random_state=42):
    """
    Create XGBoost model.
    
    Args:
        n_estimators: Number of boosting rounds
        max_depth: Maximum tree depth
        learning_rate: Learning rate
        scale_pos_weight: Weight for positive class (handles imbalance)
        random_state: Random seed
    
    Returns:
        XGBClassifier model
    """
    if not HAS_XGBOOST:
        raise ImportError("XGBoost not installed. Install with: pip install xgboost")
    
    return XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        scale_pos_weight=scale_pos_weight,
        random_state=random_state,
        eval_metric='logloss',
        use_label_encoder=False
    )


def get_all_models():
    """
    Get all available models for training.
    
    Returns:
        Dictionary of model name -> model instance
    """
    models = {
        'Baseline': BaselineModel(),
        'Logistic Regression': create_logistic_regression(),
        'Random Forest': create_random_forest()
    }
    
    if HAS_XGBOOST:
        models['XGBoost'] = create_xgboost()
    
    return models
