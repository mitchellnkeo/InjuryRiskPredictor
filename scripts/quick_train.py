"""
Quick script to train and save a model for testing interpretation notebook.
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
from src.ml.train import train_all_models, save_model
from src.ml.models import create_random_forest

print("Quick Model Training for Interpretation Testing...")
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

# Train Random Forest (quick, good for interpretation)
print("\n6. Training Random Forest model...")
rf_model = create_random_forest(n_estimators=50, max_depth=10)  # Smaller for speed
rf_model.fit(X_train_scaled, y_train)

# Evaluate
from src.ml.evaluate import evaluate_model
val_metrics = evaluate_model(rf_model, X_val_scaled, y_val, "Random Forest")
print(f"   ✓ Validation Accuracy: {val_metrics['accuracy']:.3f}")
print(f"   ✓ Validation Recall: {val_metrics['recall']:.3f}")

# Save model and scaler
print("\n7. Saving model...")
save_model(rf_model, scaler, "Random Forest", output_dir='models')

print("\n" + "=" * 60)
print("✓ Model trained and saved!")
print("✓ You can now run the interpretation notebook")
print("=" * 60)
