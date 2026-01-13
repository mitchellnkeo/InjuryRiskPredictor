"""
Simple test script to verify model training pipeline works.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np

# Import modules
from src.ml.features import engineer_features_for_dataset
from src.ml.preprocessing import (
    handle_missing_values,
    encode_categorical_features,
    split_data_by_time,
    scale_features
)
from src.ml.train import train_baseline_model, train_ml_model
from src.ml.models import create_logistic_regression, create_random_forest

print("Testing Model Training Pipeline...")
print("=" * 60)

# Load data
print("\n1. Loading data...")
training_logs = pd.read_csv('data/training_logs.csv')
print(f"   ✓ Loaded {len(training_logs)} training records")

# Engineer features
print("\n2. Engineering features...")
df = engineer_features_for_dataset(training_logs)
print(f"   ✓ Engineered features: {df.shape[1]} features")

# Preprocessing
print("\n3. Preprocessing...")
df = handle_missing_values(df, method='forward_fill')
df, encoders = encode_categorical_features(df)
print(f"   ✓ Preprocessed data")

# Split data
print("\n4. Splitting data by time...")
X_train, y_train, X_val, y_val, X_test, y_test = split_data_by_time(
    df,
    train_weeks=(1, 14),
    val_weeks=(15, 19),
    test_weeks=(20, 24)
)
print(f"   ✓ Train: {X_train.shape[0]} samples")
print(f"   ✓ Val: {X_val.shape[0]} samples")
print(f"   ✓ Test: {X_test.shape[0]} samples")

# Scale features
print("\n5. Scaling features...")
X_train_scaled, scaler = scale_features(X_train, fit=True, scaler_type='standard')
X_val_scaled, _ = scale_features(X_val, fit=False, scaler=scaler)
X_test_scaled, _ = scale_features(X_test, fit=False, scaler=scaler)
print(f"   ✓ Features scaled")

# Test baseline model
print("\n6. Testing baseline model...")
baseline_model, baseline_metrics = train_baseline_model(
    X_train_scaled, y_train, X_val_scaled, y_val
)
print(f"   ✓ Baseline accuracy: {baseline_metrics['accuracy']:.3f}")

# Test Logistic Regression
print("\n7. Testing Logistic Regression...")
lr_model = create_logistic_regression()
lr_trained, lr_metrics = train_ml_model(
    lr_model, "Logistic Regression",
    X_train_scaled, y_train, X_val_scaled, y_val
)
print(f"   ✓ LR accuracy: {lr_metrics['accuracy']:.3f}")
print(f"   ✓ LR recall: {lr_metrics['recall']:.3f}")

# Test Random Forest
print("\n8. Testing Random Forest...")
rf_model = create_random_forest()
rf_trained, rf_metrics = train_ml_model(
    rf_model, "Random Forest",
    X_train_scaled, y_train, X_val_scaled, y_val
)
print(f"   ✓ RF accuracy: {rf_metrics['accuracy']:.3f}")
print(f"   ✓ RF recall: {rf_metrics['recall']:.3f}")

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
