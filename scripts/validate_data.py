"""Validation script to check generated data quality."""

import pandas as pd
import numpy as np
import sys

def validate_training_data(training_logs_path: str, athlete_metadata_path: str):
    """
    Validate generated training data against research criteria.
    
    Args:
        training_logs_path: Path to training_logs.csv
        athlete_metadata_path: Path to athlete_metadata.csv
    """
    print("Validating Training Data")
    print("=" * 50)
    
    # Load data
    try:
        training_logs = pd.read_csv(training_logs_path)
        athlete_metadata = pd.read_csv(athlete_metadata_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run generate_training_data.py first to create the data files.")
        return False
    
    # Basic checks
    print(f"\n1. Data Volume:")
    print(f"   - Athletes: {len(athlete_metadata)}")
    print(f"   - Total weeks: {len(training_logs)}")
    print(f"   - Expected: {len(athlete_metadata) * 24} weeks")
    
    if len(training_logs) < len(athlete_metadata) * 20:
        print("   ⚠️  WARNING: Less data than expected")
    else:
        print("   ✓ Data volume looks good")
    
    # Injury rate check (should be 15-30%)
    injury_rate = training_logs['injured'].mean() * 100
    print(f"\n2. Injury Rate:")
    print(f"   - Actual: {injury_rate:.1f}%")
    print(f"   - Target: 15-30%")
    if 15 <= injury_rate <= 30:
        print("   ✓ Injury rate is within research range")
    else:
        print("   ⚠️  WARNING: Injury rate outside expected range")
    
    # ACWR distribution check
    print(f"\n3. ACWR Distribution:")
    acwr_mean = training_logs['acwr'].mean()
    acwr_std = training_logs['acwr'].std()
    acwr_min = training_logs['acwr'].min()
    acwr_max = training_logs['acwr'].max()
    
    print(f"   - Mean: {acwr_mean:.2f}")
    print(f"   - Std Dev: {acwr_std:.2f}")
    print(f"   - Range: {acwr_min:.2f} - {acwr_max:.2f}")
    
    # Check ACWR zones
    sweet_spot = ((training_logs['acwr'] >= 0.8) & (training_logs['acwr'] <= 1.3)).sum()
    sweet_spot_pct = (sweet_spot / len(training_logs)) * 100
    high_risk = (training_logs['acwr'] > 1.5).sum()
    high_risk_pct = (high_risk / len(training_logs)) * 100
    
    print(f"   - Sweet spot (0.8-1.3): {sweet_spot_pct:.1f}%")
    print(f"   - High risk (>1.5): {high_risk_pct:.1f}%")
    
    if 0.8 <= acwr_mean <= 1.3:
        print("   ✓ Mean ACWR is in sweet spot range")
    else:
        print("   ⚠️  Mean ACWR outside sweet spot")
    
    # Check relationship between ACWR and injuries
    print(f"\n4. ACWR-Injury Relationship:")
    injured_acwr = training_logs[training_logs['injured'] == True]['acwr'].mean()
    non_injured_acwr = training_logs[training_logs['injured'] == False]['acwr'].mean()
    
    print(f"   - Mean ACWR (injured): {injured_acwr:.2f}")
    print(f"   - Mean ACWR (not injured): {non_injured_acwr:.2f}")
    
    if injured_acwr > non_injured_acwr:
        print("   ✓ Injured athletes have higher ACWR (as expected)")
    else:
        print("   ⚠️  WARNING: Injured athletes don't have higher ACWR")
    
    # Check for missing values
    print(f"\n5. Data Quality:")
    missing = training_logs.isnull().sum().sum()
    if missing == 0:
        print("   ✓ No missing values")
    else:
        print(f"   ⚠️  WARNING: {missing} missing values found")
    
    # Check data types
    print(f"\n6. Data Types:")
    print(f"   - ACWR: {training_logs['acwr'].dtype}")
    print(f"   - Weekly load: {training_logs['weekly_load'].dtype}")
    print(f"   - Injured: {training_logs['injured'].dtype}")
    
    print("\n" + "=" * 50)
    print("Validation complete!")
    
    return True


if __name__ == '__main__':
    validate_training_data('data/training_logs.csv', 'data/athlete_metadata.csv')
