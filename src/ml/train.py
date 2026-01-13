"""
Model Training Pipeline for Injury Risk Predictor

Handles model training, evaluation, and saving.
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, Tuple, Optional
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import warnings
warnings.filterwarnings('ignore')

from .models import get_all_models, BaselineModel
from .preprocessing import split_data_by_time, scale_features
from .evaluate import evaluate_model, compare_models, print_evaluation_report


def train_baseline_model(X_train, y_train, X_val, y_val) -> Tuple[BaselineModel, Dict]:
    """
    Train and evaluate baseline rule-based model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        Tuple of (trained model, validation metrics)
    """
    print("Training Baseline Model...")
    print("-" * 60)
    
    model = BaselineModel()
    
    # Evaluate on validation set
    val_metrics = evaluate_model(model, X_val, y_val, "Baseline")
    
    print_evaluation_report(y_val, model.predict(X_val), 
                           model.predict_proba(X_val) if hasattr(model, 'predict_proba') else None,
                           "Baseline")
    
    return model, val_metrics


def train_ml_model(model, model_name, X_train, y_train, X_val, y_val,
                   tune_hyperparameters=False, param_grid=None, cv=5) -> Tuple:
    """
    Train a machine learning model.
    
    Args:
        model: Model instance to train
        model_name: Name of the model
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
        tune_hyperparameters: Whether to tune hyperparameters
        param_grid: Parameter grid for tuning
        cv: Number of CV folds
    
    Returns:
        Tuple of (trained model, validation metrics)
    """
    print(f"\nTraining {model_name}...")
    print("-" * 60)
    
    # Hyperparameter tuning if requested
    if tune_hyperparameters and param_grid:
        print(f"Tuning hyperparameters for {model_name}...")
        if len(param_grid) > 10:  # Use RandomizedSearchCV for large grids
            search = RandomizedSearchCV(
                model, param_grid, n_iter=20, cv=cv, 
                scoring='roc_auc', n_jobs=-1, random_state=42
            )
        else:  # Use GridSearchCV for small grids
            search = GridSearchCV(
                model, param_grid, cv=cv, 
                scoring='roc_auc', n_jobs=-1
            )
        
        search.fit(X_train, y_train)
        model = search.best_estimator_
        print(f"Best parameters: {search.best_params_}")
        print(f"Best CV score: {search.best_score_:.3f}")
    else:
        # Train without tuning
        model.fit(X_train, y_train)
    
    # Evaluate on validation set
    val_metrics = evaluate_model(model, X_val, y_val, model_name)
    
    print_evaluation_report(y_val, model.predict(X_val), 
                           model.predict_proba(X_val),
                           model_name)
    
    return model, val_metrics


def train_all_models(X_train, y_train, X_val, y_val, X_test, y_test,
                    tune_hyperparameters=False) -> Dict:
    """
    Train all models and compare performance.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
        X_test: Test features
        y_test: Test labels
        tune_hyperparameters: Whether to tune hyperparameters
    
    Returns:
        Dictionary of model_name -> (trained_model, metrics_dict)
    """
    results = {}
    
    # Train baseline
    baseline_model, baseline_metrics = train_baseline_model(X_train, y_train, X_val, y_val)
    results['Baseline'] = (baseline_model, baseline_metrics)
    
    # Get all ML models
    models = get_all_models()
    
    # Hyperparameter grids for tuning
    param_grids = {
        'Random Forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [10, 20, 30]
        },
        'XGBoost': {
            'n_estimators': [50, 100, 200],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.01, 0.1, 0.2]
        }
    }
    
    # Train each ML model
    for model_name, model in models.items():
        if model_name == 'Baseline':
            continue  # Already trained
        
        param_grid = param_grids.get(model_name) if tune_hyperparameters else None
        
        trained_model, metrics = train_ml_model(
            model, model_name, X_train, y_train, X_val, y_val,
            tune_hyperparameters=tune_hyperparameters,
            param_grid=param_grid
        )
        
        results[model_name] = (trained_model, metrics)
    
    # Compare all models
    print("\n" + "="*60)
    print("Model Comparison (Validation Set)")
    print("="*60)
    
    comparison_metrics = {name: metrics for name, (_, metrics) in results.items()}
    comparison_df = compare_models(comparison_metrics)
    print(comparison_df.to_string(index=False))
    
    # Evaluate best model on test set
    print("\n" + "="*60)
    print("Best Model Evaluation on Test Set")
    print("="*60)
    
    # Find best model by ROC-AUC
    best_model_name = comparison_df.iloc[0]['Model']
    best_model = results[best_model_name][0]
    
    test_metrics = evaluate_model(best_model, X_test, y_test, f"{best_model_name} (Test)")
    print_evaluation_report(y_test, best_model.predict(X_test),
                           best_model.predict_proba(X_test) if hasattr(best_model, 'predict_proba') else None,
                           f"{best_model_name} (Test)")
    
    results['best_model'] = (best_model, test_metrics)
    results['best_model_name'] = best_model_name
    
    return results


def save_model(model, scaler, model_name, output_dir='models'):
    """
    Save trained model and scaler.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        model_name: Name of the model
        output_dir: Directory to save models
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, f'{model_name.lower().replace(" ", "_")}_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Saved model to {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✓ Saved scaler to {scaler_path}")


def load_model(model_name, models_dir='models'):
    """
    Load a saved model.
    
    Args:
        model_name: Name of the model to load
        models_dir: Directory where models are saved
    
    Returns:
        Loaded model
    """
    model_path = os.path.join(models_dir, f'{model_name.lower().replace(" ", "_")}_model.pkl')
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model


def load_scaler(models_dir='models'):
    """
    Load saved scaler.
    
    Args:
        models_dir: Directory where scaler is saved
    
    Returns:
        Loaded scaler
    """
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return scaler
