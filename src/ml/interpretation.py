"""
Model Interpretation Module for Injury Risk Predictor

Provides tools for understanding model predictions and validating against research.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import os

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False
    print("Warning: SHAP not available. Install with: pip install shap")


def plot_feature_importance(model, feature_names: List[str], top_n: int = 15,
                           save_path: Optional[str] = None) -> pd.DataFrame:
    """
    Plot feature importance for tree-based models or coefficients for linear models.
    
    Args:
        model: Trained model
        feature_names: List of feature names
        top_n: Number of top features to display
        save_path: Path to save figure (optional)
    
    Returns:
        DataFrame with feature importance/coefficients
    """
    if hasattr(model, 'feature_importances_'):
        # Tree-based models (Random Forest, XGBoost)
        importance = model.feature_importances_
        importance_type = 'importance'
    elif hasattr(model, 'coef_'):
        # Linear models (Logistic Regression)
        importance = np.abs(model.coef_[0])
        importance_type = 'coefficient_magnitude'
    else:
        raise ValueError("Model does not support feature importance or coefficients")
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        importance_type: importance
    }).sort_values(importance_type, ascending=False)
    
    # Plot top N features
    top_features = importance_df.head(top_n)
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(top_features)), top_features[importance_type])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel(importance_type.replace('_', ' ').title())
    plt.title(f'Top {top_n} Feature {importance_type.replace("_", " ").title()}')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved feature importance plot to {save_path}")
    
    plt.close()
    
    return importance_df


def calculate_shap_values(model, X: pd.DataFrame, max_samples: int = 100) -> Optional[Dict]:
    """
    Calculate SHAP values for model interpretability.
    
    Args:
        model: Trained model
        X: Feature matrix
        max_samples: Maximum samples to use (for speed)
    
    Returns:
        Dictionary with SHAP explainer and values, or None if SHAP not available
    """
    if not HAS_SHAP:
        print("SHAP not available. Install with: pip install shap")
        return None
    
    # Sample data if too large
    if len(X) > max_samples:
        X_sample = X.sample(n=max_samples, random_state=42)
    else:
        X_sample = X
    
    try:
        # Create explainer based on model type
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            explainer = shap.TreeExplainer(model)
        else:
            # Linear models or others
            explainer = shap.Explainer(model, X_sample)
        
        shap_values = explainer(X_sample)
        
        return {
            'explainer': explainer,
            'shap_values': shap_values,
            'X_sample': X_sample
        }
    except Exception as e:
        print(f"Error calculating SHAP values: {e}")
        return None


def plot_shap_summary(shap_values, X: pd.DataFrame, top_n: int = 15,
                      save_path: Optional[str] = None):
    """
    Plot SHAP summary plot.
    
    Args:
        shap_values: SHAP values object
        X: Feature matrix
        top_n: Number of top features to display
        save_path: Path to save figure (optional)
    """
    if not HAS_SHAP:
        print("SHAP not available")
        return
    
    try:
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X, max_display=top_n, show=False)
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved SHAP summary plot to {save_path}")
        
        plt.close()
    except Exception as e:
        print(f"Error plotting SHAP summary: {e}")


def plot_partial_dependence(model, X: pd.DataFrame, feature_name: str,
                           feature_range: Optional[Tuple[float, float]] = None,
                           n_points: int = 50, save_path: Optional[str] = None):
    """
    Plot partial dependence for a single feature.
    
    Shows how predictions change as we vary one feature while keeping others constant.
    
    Args:
        model: Trained model
        X: Feature matrix
        feature_name: Name of feature to plot
        feature_range: (min, max) range for feature (auto-detected if None)
        n_points: Number of points to evaluate
        save_path: Path to save figure (optional)
    """
    if feature_name not in X.columns:
        raise ValueError(f"Feature '{feature_name}' not found in data")
    
    # Get feature range
    if feature_range is None:
        feature_min = X[feature_name].min()
        feature_max = X[feature_name].max()
    else:
        feature_min, feature_max = feature_range
    
    # Create feature values to test
    feature_values = np.linspace(feature_min, feature_max, n_points)
    
    # Create data matrix with feature varied
    X_pd = X.copy()
    predictions = []
    
    for val in feature_values:
        X_pd[feature_name] = val
        
        # Get predictions (probability of positive class)
        if hasattr(model, 'predict_proba'):
            pred = model.predict_proba(X_pd)[:, 1]
        else:
            pred = model.predict(X_pd)
        
        predictions.append(pred.mean())
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(feature_values, predictions, linewidth=2)
    plt.xlabel(feature_name.replace('_', ' ').title())
    plt.ylabel('Average Predicted Injury Risk')
    plt.title(f'Partial Dependence Plot: {feature_name.replace("_", " ").title()}')
    plt.grid(True, alpha=0.3)
    
    # Add research thresholds if ACWR
    if feature_name.lower() == 'acwr':
        plt.axvline(x=1.3, color='orange', linestyle='--', label='Moderate Risk Threshold')
        plt.axvline(x=1.5, color='red', linestyle='--', label='High Risk Threshold')
        plt.legend()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved partial dependence plot to {save_path}")
    
    plt.close()


def analyze_errors(y_true: np.ndarray, y_pred: np.ndarray, X: pd.DataFrame,
                  feature_names: List[str]) -> Dict:
    """
    Analyze prediction errors to identify patterns.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        X: Feature matrix
        feature_names: List of feature names
    
    Returns:
        Dictionary with error analysis
    """
    errors = y_true != y_pred
    
    # False positives (predicted injury but didn't happen)
    false_positives = (y_pred == 1) & (y_true == 0)
    
    # False negatives (missed injury)
    false_negatives = (y_pred == 0) & (y_true == 1)
    
    analysis = {
        'total_errors': errors.sum(),
        'error_rate': errors.mean(),
        'false_positives': false_positives.sum(),
        'false_negatives': false_negatives.sum(),
        'false_positive_rate': false_positives.mean(),
        'false_negative_rate': false_negatives.mean()
    }
    
    # Analyze feature distributions for errors
    if false_positives.sum() > 0:
        fp_features = X[false_positives].mean()
        analysis['false_positive_features'] = fp_features.to_dict()
    
    if false_negatives.sum() > 0:
        fn_features = X[false_negatives].mean()
        analysis['false_negative_features'] = fn_features.to_dict()
    
    # Compare to correct predictions
    correct = ~errors
    if correct.sum() > 0:
        correct_features = X[correct].mean()
        analysis['correct_prediction_features'] = correct_features.to_dict()
    
    return analysis


def validate_against_research(model, X: pd.DataFrame, feature_names: List[str]) -> Dict[str, bool]:
    """
    Validate model predictions against sports science research.
    
    Checks:
    1. ACWR > 1.3 should predict higher risk
    2. ACWR > 1.5 should predict much higher risk
    3. Rapid week-over-week changes should increase risk
    4. Higher strain should increase risk
    
    Args:
        model: Trained model
        X: Feature matrix
        feature_names: List of feature names
    
    Returns:
        Dictionary of validation results
    """
    validations = {}
    
    # Get predictions
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X)[:, 1]
    else:
        y_proba = model.predict(X)
    
    # Check 1: ACWR > 1.3 should predict higher risk
    if 'acwr' in X.columns:
        low_acwr = X['acwr'] < 1.3
        high_acwr = X['acwr'] > 1.3
        
        if low_acwr.sum() > 0 and high_acwr.sum() > 0:
            low_risk = y_proba[low_acwr].mean()
            high_risk = y_proba[high_acwr].mean()
            validations['acwr_1.3_threshold'] = high_risk > low_risk
            validations['acwr_1.3_risk_low'] = low_risk
            validations['acwr_1.3_risk_high'] = high_risk
        else:
            validations['acwr_1.3_threshold'] = None
    
    # Check 2: ACWR > 1.5 should predict much higher risk
    if 'acwr' in X.columns:
        moderate_acwr = (X['acwr'] >= 1.3) & (X['acwr'] <= 1.5)
        very_high_acwr = X['acwr'] > 1.5
        
        if moderate_acwr.sum() > 0 and very_high_acwr.sum() > 0:
            moderate_risk = y_proba[moderate_acwr].mean()
            very_high_risk = y_proba[very_high_acwr].mean()
            validations['acwr_1.5_threshold'] = very_high_risk > moderate_risk
            validations['acwr_1.5_risk_moderate'] = moderate_risk
            validations['acwr_1.5_risk_very_high'] = very_high_risk
        else:
            validations['acwr_1.5_threshold'] = None
    
    # Check 3: Week-over-week change > 20% should increase risk
    if 'week_over_week_change' in X.columns:
        low_change = X['week_over_week_change'] < 0.2
        high_change = X['week_over_week_change'] > 0.2
        
        if low_change.sum() > 0 and high_change.sum() > 0:
            low_change_risk = y_proba[low_change].mean()
            high_change_risk = y_proba[high_change].mean()
            validations['week_over_week_spike'] = high_change_risk > low_change_risk
            validations['week_over_week_risk_low'] = low_change_risk
            validations['week_over_week_risk_high'] = high_change_risk
        else:
            validations['week_over_week_spike'] = None
    
    # Check 4: Higher strain should increase risk
    if 'strain' in X.columns:
        low_strain = X['strain'] < X['strain'].median()
        high_strain = X['strain'] >= X['strain'].median()
        
        if low_strain.sum() > 0 and high_strain.sum() > 0:
            low_strain_risk = y_proba[low_strain].mean()
            high_strain_risk = y_proba[high_strain].mean()
            validations['strain_relationship'] = high_strain_risk > low_strain_risk
            validations['strain_risk_low'] = low_strain_risk
            validations['strain_risk_high'] = high_strain_risk
        else:
            validations['strain_relationship'] = None
    
    return validations


def print_validation_report(validations: Dict):
    """
    Print validation report in readable format.
    
    Args:
        validations: Dictionary from validate_against_research()
    """
    print("\n" + "="*60)
    print("Model Validation Against Research")
    print("="*60)
    
    if 'acwr_1.3_threshold' in validations:
        result = validations['acwr_1.3_threshold']
        if result is not None:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"\n1. ACWR > 1.3 predicts higher risk: {status}")
            print(f"   Low ACWR risk: {validations.get('acwr_1.3_risk_low', 0):.3f}")
            print(f"   High ACWR risk: {validations.get('acwr_1.3_risk_high', 0):.3f}")
    
    if 'acwr_1.5_threshold' in validations:
        result = validations['acwr_1.5_threshold']
        if result is not None:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"\n2. ACWR > 1.5 predicts much higher risk: {status}")
            print(f"   Moderate ACWR risk: {validations.get('acwr_1.5_risk_moderate', 0):.3f}")
            print(f"   Very High ACWR risk: {validations.get('acwr_1.5_risk_very_high', 0):.3f}")
    
    if 'week_over_week_spike' in validations:
        result = validations['week_over_week_spike']
        if result is not None:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"\n3. Week-over-week spikes increase risk: {status}")
            print(f"   Low change risk: {validations.get('week_over_week_risk_low', 0):.3f}")
            print(f"   High change risk: {validations.get('week_over_week_risk_high', 0):.3f}")
    
    if 'strain_relationship' in validations:
        result = validations['strain_relationship']
        if result is not None:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"\n4. Higher strain increases risk: {status}")
            print(f"   Low strain risk: {validations.get('strain_risk_low', 0):.3f}")
            print(f"   High strain risk: {validations.get('strain_risk_high', 0):.3f}")
    
    print("\n" + "="*60 + "\n")
