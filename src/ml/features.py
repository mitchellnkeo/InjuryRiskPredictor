"""
Feature Engineering Module for Injury Risk Predictor

This module implements all features needed for injury risk prediction,
including ACWR, monotony, strain, and derived features.

All features are designed to avoid data leakage by only using past data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from sklearn.linear_model import LinearRegression


def calculate_acute_load(df: pd.DataFrame, athlete_id: str, week: int) -> float:
    """
    Calculate acute load (last 7 days of training).
    
    For weekly data, acute load is the current week's load.
    For daily data, it would be the sum of last 7 days.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
    
    Returns:
        Acute load value
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_week = athlete_data[athlete_data['week'] == week]
    
    if len(current_week) == 0:
        return 0.0
    
    return float(current_week['weekly_load'].iloc[0])


def calculate_chronic_load(df: pd.DataFrame, athlete_id: str, week: int, 
                          window: int = 4) -> float:
    """
    Calculate chronic load (average over last 28 days / 4 weeks).
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        window: Number of weeks to average (default: 4 for 28 days)
    
    Returns:
        Chronic load value (average weekly load over window)
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_idx = athlete_data[athlete_data['week'] == week].index
    
    if len(current_idx) == 0:
        return 0.0
    
    # Get data up to and including current week (no future data)
    current_pos = athlete_data.index.get_loc(current_idx[0])
    start_pos = max(0, current_pos - window + 1)
    
    window_data = athlete_data.iloc[start_pos:current_pos + 1]
    
    if len(window_data) == 0:
        return 0.0
    
    return float(window_data['weekly_load'].mean())


def calculate_acwr(df: pd.DataFrame, athlete_id: str, week: int) -> float:
    """
    Calculate Acute:Chronic Workload Ratio (ACWR).
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
    
    Returns:
        ACWR value (acute / chronic)
    """
    acute = calculate_acute_load(df, athlete_id, week)
    chronic = calculate_chronic_load(df, athlete_id, week)
    
    if chronic == 0:
        return 0.0
    
    return acute / chronic


def calculate_monotony(df: pd.DataFrame, athlete_id: str, week: int, 
                      window: int = 4) -> float:
    """
    Calculate training monotony (mean / std dev of weekly loads).
    
    High monotony (>2.0) indicates repetitive training = injury risk.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        window: Number of weeks to consider (default: 4)
    
    Returns:
        Monotony value
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_idx = athlete_data[athlete_data['week'] == week].index
    
    if len(current_idx) == 0:
        return 1.0  # Default value
    
    current_pos = athlete_data.index.get_loc(current_idx[0])
    start_pos = max(0, current_pos - window + 1)
    
    window_data = athlete_data.iloc[start_pos:current_pos + 1]['weekly_load']
    
    if len(window_data) < 2:
        return 1.0
    
    mean_load = window_data.mean()
    std_load = window_data.std()
    
    if std_load == 0:
        return 1.0  # Avoid division by zero
    
    return mean_load / std_load


def calculate_strain(df: pd.DataFrame, athlete_id: str, week: int) -> float:
    """
    Calculate training strain (weekly load × monotony).
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
    
    Returns:
        Strain value
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_week = athlete_data[athlete_data['week'] == week]
    
    if len(current_week) == 0:
        return 0.0
    
    weekly_load = float(current_week['weekly_load'].iloc[0])
    monotony = calculate_monotony(df, athlete_id, week)
    
    return weekly_load * monotony


def calculate_week_over_week_change(df: pd.DataFrame, athlete_id: str, 
                                    week: int) -> float:
    """
    Calculate week-over-week percentage change in training load.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
    
    Returns:
        Percentage change (can be negative or positive)
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_week = athlete_data[athlete_data['week'] == week]
    
    if len(current_week) == 0:
        return 0.0
    
    current_load = float(current_week['weekly_load'].iloc[0])
    
    # Get previous week
    prev_week = week - 1
    prev_week_data = athlete_data[athlete_data['week'] == prev_week]
    
    if len(prev_week_data) == 0:
        return 0.0
    
    prev_load = float(prev_week_data['weekly_load'].iloc[0])
    
    if prev_load == 0:
        return 0.0
    
    return ((current_load - prev_load) / prev_load) * 100


def calculate_acwr_trend(df: pd.DataFrame, athlete_id: str, week: int, 
                        window: int = 2) -> float:
    """
    Calculate ACWR trend (slope over last N weeks).
    
    Positive = increasing (toward danger), negative = decreasing (safer).
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        window: Number of weeks to consider (default: 2)
    
    Returns:
        Slope of ACWR trend
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_idx = athlete_data[athlete_data['week'] == week].index
    
    if len(current_idx) == 0:
        return 0.0
    
    current_pos = athlete_data.index.get_loc(current_idx[0])
    start_pos = max(0, current_pos - window + 1)
    
    window_data = athlete_data.iloc[start_pos:current_pos + 1]
    
    if len(window_data) < 2:
        return 0.0
    
    # Calculate ACWR for each week in window
    acwr_values = []
    for w in window_data['week']:
        acwr = calculate_acwr(df, athlete_id, int(w))
        acwr_values.append(acwr)
    
    if len(acwr_values) < 2:
        return 0.0
    
    # Calculate slope using linear regression
    weeks = np.array(range(len(acwr_values))).reshape(-1, 1)
    acwr_array = np.array(acwr_values)
    
    if len(weeks) < 2:
        return 0.0
    
    model = LinearRegression()
    model.fit(weeks, acwr_array)
    
    return float(model.coef_[0])


def calculate_weeks_above_threshold(df: pd.DataFrame, athlete_id: str, 
                                   week: int, threshold: float = 1.3) -> int:
    """
    Calculate consecutive weeks with ACWR above threshold.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        threshold: ACWR threshold (default: 1.3)
    
    Returns:
        Number of consecutive weeks above threshold
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_idx = athlete_data[athlete_data['week'] == week].index
    
    if len(current_idx) == 0:
        return 0
    
    current_pos = athlete_data.index.get_loc(current_idx[0])
    
    # Count backwards from current week
    count = 0
    for i in range(current_pos, -1, -1):
        w = int(athlete_data.iloc[i]['week'])
        acwr = calculate_acwr(df, athlete_id, w)
        
        if acwr > threshold:
            count += 1
        else:
            break
    
    return count


def calculate_distance_from_baseline(df: pd.DataFrame, athlete_id: str, 
                                     week: int, baseline_window: int = 12) -> float:
    """
    Calculate distance from athlete's personal baseline.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        baseline_window: Weeks to use for baseline calculation (default: 12)
    
    Returns:
        Percentage difference from baseline
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_week = athlete_data[athlete_data['week'] == week]
    
    if len(current_week) == 0:
        return 0.0
    
    current_load = float(current_week['weekly_load'].iloc[0])
    
    # Calculate baseline (median of historical data, excluding current week)
    current_idx = athlete_data[athlete_data['week'] == week].index
    current_pos = athlete_data.index.get_loc(current_idx[0])
    start_pos = max(0, current_pos - baseline_window)
    
    baseline_data = athlete_data.iloc[start_pos:current_pos]['weekly_load']
    
    if len(baseline_data) == 0:
        return 0.0
    
    baseline_load = float(baseline_data.median())
    
    if baseline_load == 0:
        return 0.0
    
    return ((current_load - baseline_load) / baseline_load) * 100


def calculate_lag_features(df: pd.DataFrame, athlete_id: str, week: int, 
                          lag_weeks: int = 1) -> float:
    """
    Calculate lag features (previous week's ACWR).
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        lag_weeks: Number of weeks to lag (default: 1)
    
    Returns:
        ACWR value from lag_weeks ago
    """
    lag_week = week - lag_weeks
    
    if lag_week < 1:
        return 0.0
    
    return calculate_acwr(df, athlete_id, lag_week)


def calculate_recent_injury(df: pd.DataFrame, athlete_id: str, week: int, 
                           window: int = 8) -> int:
    """
    Calculate binary indicator if athlete was injured in last N weeks.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
        window: Number of weeks to look back (default: 8)
    
    Returns:
        1 if injured in last window weeks, 0 otherwise
    """
    athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
    current_idx = athlete_data[athlete_data['week'] == week].index
    
    if len(current_idx) == 0:
        return 0
    
    current_pos = athlete_data.index.get_loc(current_idx[0])
    start_pos = max(0, current_pos - window)
    
    # Look at previous weeks (not including current week)
    window_data = athlete_data.iloc[start_pos:current_pos]
    
    if len(window_data) == 0:
        return 0
    
    # Check if any injury occurred in this window
    if 'injured' in window_data.columns:
        return 1 if window_data['injured'].any() else 0
    
    return 0


def bin_age(age: int) -> str:
    """
    Bin age into categories.
    
    Args:
        age: Age in years
    
    Returns:
        Age group category
    """
    if age < 26:
        return 'young_adult'
    elif age < 36:
        return 'adult'
    elif age < 46:
        return 'masters'
    else:
        return 'senior'


def bin_experience(experience_years: int) -> str:
    """
    Bin experience into categories.
    
    Args:
        experience_years: Years of training experience
    
    Returns:
        Experience level category
    """
    if experience_years < 3:
        return 'novice'
    elif experience_years < 6:
        return 'intermediate'
    elif experience_years < 10:
        return 'advanced'
    else:
        return 'expert'


def engineer_all_features(df: pd.DataFrame, athlete_id: str, week: int) -> Dict[str, float]:
    """
    Engineer all features for a given athlete and week.
    
    This is the main function to call for feature engineering.
    Ensures no data leakage by only using past data.
    
    Args:
        df: DataFrame with training data
        athlete_id: ID of the athlete
        week: Current week number
    
    Returns:
        Dictionary of feature names and values
    """
    features = {}
    
    # Core metrics
    features['acute_load'] = calculate_acute_load(df, athlete_id, week)
    features['chronic_load'] = calculate_chronic_load(df, athlete_id, week)
    features['acwr'] = calculate_acwr(df, athlete_id, week)
    features['monotony'] = calculate_monotony(df, athlete_id, week)
    features['strain'] = calculate_strain(df, athlete_id, week)
    features['week_over_week_change'] = calculate_week_over_week_change(df, athlete_id, week)
    
    # Derived features
    features['acwr_trend'] = calculate_acwr_trend(df, athlete_id, week)
    features['weeks_above_threshold'] = calculate_weeks_above_threshold(df, athlete_id, week)
    features['distance_from_baseline'] = calculate_distance_from_baseline(df, athlete_id, week)
    
    # Lag features
    features['previous_week_acwr'] = calculate_lag_features(df, athlete_id, week, lag_weeks=1)
    features['two_weeks_ago_acwr'] = calculate_lag_features(df, athlete_id, week, lag_weeks=2)
    features['recent_injury'] = calculate_recent_injury(df, athlete_id, week)
    
    # Athlete-specific features (from metadata)
    athlete_data = df[df['athlete_id'] == athlete_id]
    if len(athlete_data) > 0:
        age = int(athlete_data['age'].iloc[0])
        experience = int(athlete_data['experience_years'].iloc[0])
        baseline = float(athlete_data['baseline_weekly_miles'].iloc[0])
        
        features['age'] = age
        features['age_group'] = bin_age(age)
        features['experience_years'] = experience
        features['experience_level'] = bin_experience(experience)
        features['baseline_weekly_miles'] = baseline
    else:
        features['age'] = 0
        features['age_group'] = 'unknown'
        features['experience_years'] = 0
        features['experience_level'] = 'unknown'
        features['baseline_weekly_miles'] = 0.0
    
    # Interaction features (optional, can be added later)
    # features['acwr_x_age'] = features['acwr'] * features['age']
    # features['acwr_x_experience'] = features['acwr'] * features['experience_years']
    # features['strain_x_experience'] = features['strain'] * features['experience_years']
    
    return features


def engineer_features_for_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer all features for entire dataset.
    
    This function applies feature engineering to all athlete-week combinations
    in the dataset, creating a feature matrix ready for ML.
    
    Args:
        df: DataFrame with training data (must have athlete_id, week columns)
    
    Returns:
        DataFrame with engineered features
    """
    feature_rows = []
    
    for athlete_id in df['athlete_id'].unique():
        athlete_data = df[df['athlete_id'] == athlete_id].sort_values('week')
        
        for _, row in athlete_data.iterrows():
            week = int(row['week'])
            features = engineer_all_features(df, athlete_id, week)
            features['athlete_id'] = athlete_id
            features['week'] = week
            
            # Preserve target variable if it exists
            if 'injured' in row:
                features['injured'] = row['injured']
            
            feature_rows.append(features)
    
    return pd.DataFrame(feature_rows)
