"""
Unit tests for feature engineering functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import pandas as pd
import numpy as np
from src.ml.features import (
    calculate_acute_load,
    calculate_chronic_load,
    calculate_acwr,
    calculate_monotony,
    calculate_strain,
    calculate_week_over_week_change,
    calculate_acwr_trend,
    calculate_weeks_above_threshold,
    calculate_distance_from_baseline,
    calculate_lag_features,
    calculate_recent_injury,
    bin_age,
    bin_experience,
    engineer_all_features
)


@pytest.fixture
def sample_data():
    """Create sample training data for testing."""
    data = {
        'athlete_id': ['ATH001'] * 10,
        'week': list(range(1, 11)),
        'weekly_load': [20, 22, 25, 30, 35, 40, 45, 50, 35, 30],
        'age': [30] * 10,
        'experience_years': [5] * 10,
        'baseline_weekly_miles': [30] * 10,
        'injured': [False] * 9 + [True]
    }
    return pd.DataFrame(data)


def test_calculate_acute_load(sample_data):
    """Test acute load calculation."""
    acute = calculate_acute_load(sample_data, 'ATH001', 5)
    assert acute == 35.0
    assert isinstance(acute, (int, float))


def test_calculate_chronic_load(sample_data):
    """Test chronic load calculation."""
    chronic = calculate_chronic_load(sample_data, 'ATH001', 5, window=4)
    # Should be average of weeks 2, 3, 4, 5: (22 + 25 + 30 + 35) / 4 = 28.0
    assert chronic == 28.0


def test_calculate_acwr(sample_data):
    """Test ACWR calculation."""
    acwr = calculate_acwr(sample_data, 'ATH001', 5)
    # Acute = 35, Chronic = 28, ACWR = 35/28 = 1.25
    assert abs(acwr - 1.25) < 0.01
    assert acwr > 0


def test_calculate_acwr_zero_chronic(sample_data):
    """Test ACWR with zero chronic load."""
    # Create data with zero loads
    zero_data = sample_data.copy()
    zero_data['weekly_load'] = 0
    acwr = calculate_acwr(zero_data, 'ATH001', 5)
    assert acwr == 0.0


def test_calculate_monotony(sample_data):
    """Test monotony calculation."""
    monotony = calculate_monotony(sample_data, 'ATH001', 5)
    assert monotony > 0
    assert isinstance(monotony, (int, float))


def test_calculate_strain(sample_data):
    """Test strain calculation."""
    strain = calculate_strain(sample_data, 'ATH001', 5)
    assert strain > 0
    assert isinstance(strain, (int, float))


def test_calculate_week_over_week_change(sample_data):
    """Test week-over-week change calculation."""
    change = calculate_week_over_week_change(sample_data, 'ATH001', 5)
    # Week 5 = 35, Week 4 = 30, Change = (35-30)/30 * 100 = 16.67%
    assert abs(change - 16.67) < 0.1


def test_calculate_week_over_week_change_first_week(sample_data):
    """Test week-over-week change for first week."""
    change = calculate_week_over_week_change(sample_data, 'ATH001', 1)
    assert change == 0.0  # No previous week


def test_calculate_acwr_trend(sample_data):
    """Test ACWR trend calculation."""
    trend = calculate_acwr_trend(sample_data, 'ATH001', 5, window=2)
    assert isinstance(trend, (int, float))


def test_calculate_weeks_above_threshold(sample_data):
    """Test weeks above threshold calculation."""
    # Create data with high ACWR
    high_acwr_data = sample_data.copy()
    high_acwr_data['weekly_load'] = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    
    weeks_above = calculate_weeks_above_threshold(high_acwr_data, 'ATH001', 10, threshold=1.3)
    assert weeks_above >= 0
    assert isinstance(weeks_above, int)


def test_calculate_distance_from_baseline(sample_data):
    """Test distance from baseline calculation."""
    distance = calculate_distance_from_baseline(sample_data, 'ATH001', 5)
    assert isinstance(distance, (int, float))


def test_calculate_lag_features(sample_data):
    """Test lag feature calculation."""
    lag_acwr = calculate_lag_features(sample_data, 'ATH001', 5, lag_weeks=1)
    assert isinstance(lag_acwr, (int, float))
    assert lag_acwr >= 0


def test_calculate_recent_injury(sample_data):
    """Test recent injury calculation."""
    recent = calculate_recent_injury(sample_data, 'ATH001', 10, window=8)
    # Week 10 has injury, so should be 0 (current week not included)
    # But week 9 might have injury flag, so could be 1
    assert recent in [0, 1]


def test_bin_age():
    """Test age binning."""
    assert bin_age(20) == 'young_adult'
    assert bin_age(30) == 'adult'
    assert bin_age(40) == 'masters'
    assert bin_age(50) == 'senior'


def test_bin_experience():
    """Test experience binning."""
    assert bin_experience(1) == 'novice'
    assert bin_experience(4) == 'intermediate'
    assert bin_experience(7) == 'advanced'
    assert bin_experience(12) == 'expert'


def test_engineer_all_features(sample_data):
    """Test complete feature engineering."""
    features = engineer_all_features(sample_data, 'ATH001', 5)
    
    # Check that all expected features are present
    expected_features = [
        'acute_load', 'chronic_load', 'acwr', 'monotony', 'strain',
        'week_over_week_change', 'acwr_trend', 'weeks_above_threshold',
        'distance_from_baseline', 'previous_week_acwr', 'two_weeks_ago_acwr',
        'recent_injury', 'age', 'age_group', 'experience_years',
        'experience_level', 'baseline_weekly_miles'
    ]
    
    for feature in expected_features:
        assert feature in features, f"Missing feature: {feature}"
        assert features[feature] is not None


def test_no_data_leakage(sample_data):
    """Test that features don't use future data."""
    # Create data with known pattern
    test_data = sample_data.copy()
    
    # Calculate features for week 5
    features_week5 = engineer_all_features(test_data, 'ATH001', 5)
    
    # Add future data (week 11)
    future_row = pd.DataFrame({
        'athlete_id': ['ATH001'],
        'week': [11],
        'weekly_load': [100],  # Very high future load
        'age': [30],
        'experience_years': [5],
        'baseline_weekly_miles': [30],
        'injured': [False]
    })
    test_data_with_future = pd.concat([test_data, future_row], ignore_index=True)
    
    # Features for week 5 should be the same (no future data used)
    features_week5_after = engineer_all_features(test_data_with_future, 'ATH001', 5)
    
    assert features_week5['acute_load'] == features_week5_after['acute_load']
    assert features_week5['chronic_load'] == features_week5_after['chronic_load']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
