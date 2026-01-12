"""
Test script to validate EDA notebook code works correctly.
This extracts and runs the key code from the notebook.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("Testing EDA Notebook Code")
print("="*60)

# Test 1: Load data
print("\n1. Testing data loading...")
try:
    training_logs = pd.read_csv('data/training_logs.csv')
    athlete_metadata = pd.read_csv('data/athlete_metadata.csv')
    print(f"   ✓ Data loaded: {training_logs.shape[0]} rows, {training_logs.shape[1]} columns")
except Exception as e:
    print(f"   ✗ Error loading data: {e}")
    sys.exit(1)

# Test 2: Check for missing values
print("\n2. Testing missing value check...")
try:
    missing = training_logs.isnull().sum()
    missing_count = missing.sum()
    if missing_count == 0:
        print(f"   ✓ No missing values")
    else:
        print(f"   ⚠️  {missing_count} missing values found")
except Exception as e:
    print(f"   ✗ Error checking missing values: {e}")
    sys.exit(1)

# Test 3: ACWR zone calculation
print("\n3. Testing ACWR zone calculation...")
try:
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
    zone_counts = training_logs['acwr_zone'].value_counts()
    print(f"   ✓ ACWR zones calculated: {len(zone_counts)} zones")
except Exception as e:
    print(f"   ✗ Error calculating ACWR zones: {e}")
    sys.exit(1)

# Test 4: Injury statistics
print("\n4. Testing injury statistics...")
try:
    injury_rate = training_logs['injured'].mean() * 100
    print(f"   ✓ Injury rate: {injury_rate:.1f}%")
    if 15 <= injury_rate <= 30:
        print(f"   ✓ Within expected range (15-30%)")
except Exception as e:
    print(f"   ✗ Error calculating injury stats: {e}")
    sys.exit(1)

# Test 5: Statistical tests
print("\n5. Testing statistical tests...")
try:
    injured_acwr = training_logs[training_logs['injured'] == True]['acwr']
    non_injured_acwr = training_logs[training_logs['injured'] == False]['acwr']
    
    t_stat, p_value = ttest_ind(injured_acwr, non_injured_acwr)
    print(f"   ✓ T-test completed: t={t_stat:.3f}, p={p_value:.2e}")
    
    contingency_table = pd.crosstab(training_logs['acwr_zone'], training_logs['injured'])
    chi2, p_value_chi, dof, expected = chi2_contingency(contingency_table)
    print(f"   ✓ Chi-square test completed: chi2={chi2:.3f}, p={p_value_chi:.2e}")
except Exception as e:
    print(f"   ✗ Error in statistical tests: {e}")
    sys.exit(1)

# Test 6: Correlation matrix
print("\n6. Testing correlation analysis...")
try:
    features_for_corr = ['weekly_load', 'acute_load', 'chronic_load', 'acwr', 'monotony', 
                         'strain', 'week_over_week_change', 'age', 'experience_years', 'injured']
    corr_matrix = training_logs[features_for_corr].corr()
    print(f"   ✓ Correlation matrix calculated: {corr_matrix.shape}")
    injury_corr = corr_matrix['injured'].sort_values(ascending=False)
    print(f"   ✓ Top correlation with injury: {injury_corr.index[1]} = {injury_corr.iloc[1]:.3f}")
except Exception as e:
    print(f"   ✗ Error in correlation analysis: {e}")
    sys.exit(1)

# Test 7: Visualization creation (without displaying)
print("\n7. Testing visualization creation...")
try:
    # Create outputs directory
    os.makedirs('outputs', exist_ok=True)
    
    # Test ACWR distribution plot
    fig, ax = plt.subplots(figsize=(10, 6))
    injured_acwr = training_logs[training_logs['injured'] == True]['acwr']
    non_injured_acwr = training_logs[training_logs['injured'] == False]['acwr']
    
    ax.hist(non_injured_acwr, bins=30, alpha=0.7, label='Not Injured', color='green', density=True)
    ax.hist(injured_acwr, bins=30, alpha=0.7, label='Injured', color='red', density=True)
    ax.set_xlabel('ACWR')
    ax.set_ylabel('Density')
    ax.set_title('ACWR Distribution by Injury Status')
    ax.legend()
    plt.savefig('outputs/test_acwr_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✓ ACWR distribution plot created")
    
    # Test injury rate by zone plot
    zone_stats = training_logs.groupby('acwr_zone').agg({
        'injured': ['sum', 'count', 'mean']
    }).round(3)
    zone_stats.columns = ['Injured_Count', 'Total_Weeks', 'Injury_Rate']
    zone_stats['Injury_Rate_Pct'] = (zone_stats['Injury_Rate'] * 100).round(1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    zones = ['Undertrained (<0.8)', 'Sweet Spot (0.8-1.3)', 'Moderate Risk (1.3-1.5)', 'High Risk (>1.5)']
    injury_rates = [zone_stats.loc[zone, 'Injury_Rate_Pct'] for zone in zones]
    colors = ['gray', 'green', 'orange', 'red']
    ax.bar(zones, injury_rates, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Injury Rate (%)')
    ax.set_xlabel('ACWR Zone')
    ax.set_title('Injury Rate by ACWR Zone')
    plt.xticks(rotation=15, ha='right')
    plt.savefig('outputs/test_injury_rate_by_zone.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✓ Injury rate by zone plot created")
    
    # Test correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, ax=ax)
    ax.set_title('Correlation Matrix of Features')
    plt.savefig('outputs/test_correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✓ Correlation heatmap created")
    
except Exception as e:
    print(f"   ✗ Error creating visualizations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("All tests passed! ✓")
print("="*60)
print("\nThe notebook code is working correctly.")
print("You can now run the full notebook in Jupyter to generate all visualizations.")
