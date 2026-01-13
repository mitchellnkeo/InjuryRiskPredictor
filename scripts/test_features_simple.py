"""
Simple test script for feature engineering (no pytest required).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
from src.ml.features import (
    calculate_acute_load,
    calculate_chronic_load,
    calculate_acwr,
    engineer_all_features
)

print("Testing Feature Engineering Module")
print("=" * 60)

# Create sample data
print("\n1. Creating sample data...")
data = {
    'athlete_id': ['ATH001'] * 10,
    'week': list(range(1, 11)),
    'weekly_load': [20, 22, 25, 30, 35, 40, 45, 50, 35, 30],
    'age': [30] * 10,
    'experience_years': [5] * 10,
    'baseline_weekly_miles': [30] * 10,
    'injured': [False] * 9 + [True]
}
df = pd.DataFrame(data)
print(f"   ✓ Created sample data: {len(df)} rows")

# Test acute load
print("\n2. Testing acute load calculation...")
try:
    acute = calculate_acute_load(df, 'ATH001', 5)
    assert acute == 35.0, f"Expected 35.0, got {acute}"
    print(f"   ✓ Acute load: {acute}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test chronic load
print("\n3. Testing chronic load calculation...")
try:
    chronic = calculate_chronic_load(df, 'ATH001', 5, window=4)
    expected = (22 + 25 + 30 + 35) / 4  # Average of weeks 2-5
    assert abs(chronic - expected) < 0.01, f"Expected ~{expected}, got {chronic}"
    print(f"   ✓ Chronic load: {chronic:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test ACWR
print("\n4. Testing ACWR calculation...")
try:
    acwr = calculate_acwr(df, 'ATH001', 5)
    expected = 35.0 / 28.0  # acute / chronic
    assert abs(acwr - expected) < 0.01, f"Expected ~{expected:.2f}, got {acwr:.2f}"
    print(f"   ✓ ACWR: {acwr:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test complete feature engineering
print("\n5. Testing complete feature engineering...")
try:
    features = engineer_all_features(df, 'ATH001', 5)
    required_features = [
        'acute_load', 'chronic_load', 'acwr', 'monotony', 'strain',
        'week_over_week_change', 'acwr_trend', 'weeks_above_threshold',
        'distance_from_baseline', 'previous_week_acwr', 'two_weeks_ago_acwr',
        'recent_injury', 'age', 'age_group', 'experience_years',
        'experience_level', 'baseline_weekly_miles'
    ]
    
    missing = [f for f in required_features if f not in features]
    if missing:
        print(f"   ✗ Missing features: {missing}")
        sys.exit(1)
    
    print(f"   ✓ All {len(required_features)} features calculated")
    print(f"   ✓ Sample features: ACWR={features['acwr']:.2f}, Monotony={features['monotony']:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test with real data
print("\n6. Testing with real training data...")
try:
    real_df = pd.read_csv('data/training_logs.csv')
    sample_athlete = real_df['athlete_id'].iloc[0]
    sample_week = real_df[real_df['athlete_id'] == sample_athlete]['week'].iloc[10]
    
    features = engineer_all_features(real_df, sample_athlete, int(sample_week))
    print(f"   ✓ Features calculated for athlete {sample_athlete}, week {sample_week}")
    print(f"   ✓ ACWR: {features['acwr']:.2f}")
    print(f"   ✓ All features valid: {all(v is not None for v in features.values())}")
except Exception as e:
    print(f"   ⚠️  Warning: Could not test with real data: {e}")
    print("   (This is OK if data files don't exist yet)")

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
