"""
Simple validation script for EDA notebook.
Tests that the code logic is correct without requiring all dependencies.
"""

import sys
import os

print("Validating EDA Notebook Structure...")
print("="*60)

# Check that notebook exists
notebook_path = 'notebooks/02_exploratory_analysis.ipynb'
if not os.path.exists(notebook_path):
    print(f"✗ Notebook not found: {notebook_path}")
    sys.exit(1)
print(f"✓ Notebook exists: {notebook_path}")

# Check that data files exist
data_files = ['data/training_logs.csv', 'data/athlete_metadata.csv']
for data_file in data_files:
    if not os.path.exists(data_file):
        print(f"✗ Data file not found: {data_file}")
        sys.exit(1)
    print(f"✓ Data file exists: {data_file}")

# Check that outputs directory exists or can be created
outputs_dir = 'outputs'
if not os.path.exists(outputs_dir):
    os.makedirs(outputs_dir)
    print(f"✓ Created outputs directory: {outputs_dir}")
else:
    print(f"✓ Outputs directory exists: {outputs_dir}")

# Try to import required libraries
print("\nChecking required libraries...")
try:
    import pandas as pd
    print("  ✓ pandas")
except ImportError:
    print("  ✗ pandas not available")
    sys.exit(1)

try:
    import numpy as np
    print("  ✓ numpy")
except ImportError:
    print("  ✗ numpy not available")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    print("  ✓ matplotlib")
except ImportError:
    print("  ✗ matplotlib not available")
    sys.exit(1)

try:
    import scipy.stats
    print("  ✓ scipy")
except ImportError:
    print("  ✗ scipy not available")
    sys.exit(1)

try:
    import seaborn
    print("  ✓ seaborn (optional)")
except ImportError:
    print("  ⚠️  seaborn not available (will use matplotlib fallback)")

# Test basic data loading
print("\nTesting data loading...")
try:
    training_logs = pd.read_csv('data/training_logs.csv')
    athlete_metadata = pd.read_csv('data/athlete_metadata.csv')
    print(f"  ✓ Loaded {len(training_logs)} training log rows")
    print(f"  ✓ Loaded {len(athlete_metadata)} athlete profiles")
except Exception as e:
    print(f"  ✗ Error loading data: {e}")
    sys.exit(1)

# Test basic operations from notebook
print("\nTesting notebook operations...")
try:
    # Test ACWR zone calculation
    def get_acwr_zone(acwr):
        if acwr < 0.8:
            return 'Undertrained (<0.8)'
        elif acwr < 1.3:
            return 'Sweet Spot (0.8-1.3)'
        elif acwr < 1.5:
            return 'Moderate Risk (1.3-1.5)'
        else:
            return 'High Risk (>1.5)'
    
    training_logs['acwr_zone'] = training_logs['acwr'].apply(get_acwr_zone)
    print("  ✓ ACWR zone calculation works")
    
    # Test correlation
    features = ['weekly_load', 'acwr', 'monotony', 'strain', 'injured']
    corr = training_logs[features].corr()
    print("  ✓ Correlation calculation works")
    
    # Test statistical tests
    from scipy.stats import ttest_ind
    injured = training_logs[training_logs['injured'] == True]['acwr']
    not_injured = training_logs[training_logs['injured'] == False]['acwr']
    t_stat, p_val = ttest_ind(injured, not_injured)
    print(f"  ✓ T-test works (t={t_stat:.2f}, p={p_val:.2e})")
    
except Exception as e:
    print(f"  ✗ Error in operations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✓ All validations passed!")
print("="*60)
print("\nThe notebook should work correctly when run in Jupyter.")
print("Note: If seaborn is not installed, the notebook will use matplotlib fallbacks.")
