"""
Test script to verify interpretation module works correctly.
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
from src.ml.train import load_model, load_scaler
from src.ml.interpretation import (
    plot_feature_importance,
    calculate_shap_values,
    plot_shap_summary,
    plot_partial_dependence,
    analyze_errors,
    validate_against_research,
    print_validation_report
)

print("Testing Model Interpretation Module...")
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
print(f"   ✓ Test: {X_test.shape[0]} samples")

# Load scaler
print("\n5. Loading scaler...")
try:
    scaler = load_scaler('models')
    X_train_scaled, _ = scale_features(X_train, fit=False, scaler=scaler)
    X_test_scaled, _ = scale_features(X_test, fit=False, scaler=scaler)
    print(f"   ✓ Scaler loaded and applied")
except FileNotFoundError:
    print("   ⚠ No scaler found, creating new one...")
    X_train_scaled, scaler = scale_features(X_train, fit=True, scaler_type='standard')
    X_test_scaled, _ = scale_features(X_test, fit=False, scaler=scaler)

# Load model
print("\n6. Loading model...")
model_names = ['random_forest', 'Random Forest', 'xgboost', 'XGBoost', 'logistic_regression', 'Logistic Regression']
model = None
model_name = None

for name in model_names:
    try:
        model = load_model(name, 'models')
        model_name = name
        print(f"   ✓ Loaded model: {name}")
        print(f"   Model type: {type(model).__name__}")
        break
    except (FileNotFoundError, Exception) as e:
        continue

if model is None:
    print("   ✗ No model found!")
    print("   Available files in models/:")
    import os
    if os.path.exists('models'):
        for f in os.listdir('models'):
            print(f"     - {f}")
    exit(1)

# Test feature importance
print("\n7. Testing feature importance...")
try:
    feature_importance_df = plot_feature_importance(
        model,
        X_train_scaled.columns.tolist(),
        top_n=10,
        save_path='outputs/feature_importance_test.png'
    )
    print(f"   ✓ Feature importance calculated")
    print(f"   Top 5 features:")
    print(feature_importance_df.head(5).to_string(index=False))
    
    # Check if ACWR is in top 3
    top_3 = feature_importance_df.head(3)['feature'].tolist()
    if 'acwr' in top_3:
        print(f"   ✓ ACWR is in top 3 features (validation passed)")
    else:
        print(f"   ⚠ ACWR not in top 3 (top 3: {top_3})")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test partial dependence
print("\n8. Testing partial dependence plots...")
try:
    if 'acwr' in X_test_scaled.columns:
        plot_partial_dependence(
            model,
            X_test_scaled,
            'acwr',
            save_path='outputs/partial_dependence_acwr_test.png'
        )
        print(f"   ✓ Partial dependence plot created for ACWR")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test error analysis
print("\n9. Testing error analysis...")
try:
    y_test_pred = model.predict(X_test_scaled)
    error_analysis = analyze_errors(
        y_test.values,
        y_test_pred,
        X_test_scaled,
        X_test_scaled.columns.tolist()
    )
    print(f"   ✓ Error analysis completed")
    print(f"   Total errors: {error_analysis['total_errors']} ({error_analysis['error_rate']:.2%})")
    print(f"   False positives: {error_analysis['false_positives']}")
    print(f"   False negatives: {error_analysis['false_negatives']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test research validation
print("\n10. Testing research validation...")
try:
    validations = validate_against_research(
        model,
        X_test_scaled,
        X_test_scaled.columns.tolist()
    )
    print_validation_report(validations)
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test SHAP (optional, may not be available)
print("\n11. Testing SHAP values (optional)...")
try:
    shap_results = calculate_shap_values(model, X_test_scaled, max_samples=50)
    if shap_results:
        print(f"   ✓ SHAP values calculated")
        plot_shap_summary(
            shap_results['shap_values'],
            shap_results['X_sample'],
            top_n=10,
            save_path='outputs/shap_summary_test.png'
        )
        print(f"   ✓ SHAP summary plot created")
    else:
        print(f"   ⚠ SHAP not available (install with: pip install shap)")
except Exception as e:
    print(f"   ⚠ SHAP error (this is okay if SHAP not installed): {e}")

print("\n" + "=" * 60)
print("✓ Interpretation module testing complete!")
print("=" * 60)
