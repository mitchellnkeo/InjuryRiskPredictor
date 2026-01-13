"""
Preprocessing Module for Injury Risk Predictor

Handles data preprocessing, scaling, encoding, and feature selection
for the injury risk prediction model.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, List, Optional


def handle_missing_values(df: pd.DataFrame, method: str = 'forward_fill') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: DataFrame with potential missing values
        method: Method to use ('forward_fill', 'backward_fill', 'mean', 'median', 'drop')
    
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    if method == 'forward_fill':
        df = df.fillna(method='ffill').fillna(method='bfill')
    elif method == 'backward_fill':
        df = df.fillna(method='bfill').fillna(method='ffill')
    elif method == 'mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif method == 'median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif method == 'drop':
        df = df.dropna()
    
    return df


def encode_categorical_features(df: pd.DataFrame, 
                                categorical_cols: Optional[List[str]] = None) -> Tuple[pd.DataFrame, dict]:
    """
    Encode categorical features using label encoding.
    
    Args:
        df: DataFrame with categorical features
        categorical_cols: List of categorical column names (auto-detected if None)
    
    Returns:
        Tuple of (encoded DataFrame, label encoders dictionary)
    """
    df = df.copy()
    encoders = {}
    
    if categorical_cols is None:
        # Auto-detect categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        # Exclude target variable and ID columns
        categorical_cols = [col for col in categorical_cols 
                          if col not in ['athlete_id', 'injured', 'injury_type']]
    
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    
    return df, encoders


def scale_features(df: pd.DataFrame, 
                   feature_cols: Optional[List[str]] = None,
                   scaler_type: str = 'standard',
                   fit: bool = True,
                   scaler: Optional[object] = None) -> Tuple[pd.DataFrame, object]:
    """
    Scale numerical features.
    
    Args:
        df: DataFrame with features to scale
        feature_cols: List of feature column names (auto-detected if None)
        scaler_type: Type of scaler ('standard' or 'minmax')
        fit: Whether to fit the scaler (True for training, False for inference)
        scaler: Pre-fitted scaler (used when fit=False)
    
    Returns:
        Tuple of (scaled DataFrame, fitted scaler)
    """
    df = df.copy()
    
    if feature_cols is None:
        # Auto-detect numerical features (exclude IDs and target)
        exclude_cols = ['athlete_id', 'week', 'injured', 'injury_type', 'injury_week']
        feature_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                       if col not in exclude_cols]
    
    if scaler is None:
        if scaler_type == 'standard':
            scaler = StandardScaler()
        elif scaler_type == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler_type: {scaler_type}")
    
    if fit:
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
    else:
        df[feature_cols] = scaler.transform(df[feature_cols])
    
    return df, scaler


def prepare_features_for_training(df: pd.DataFrame,
                                  target_col: str = 'injured',
                                  exclude_cols: Optional[List[str]] = None) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features and target for model training.
    
    Args:
        df: DataFrame with features and target
        target_col: Name of target column
        exclude_cols: Columns to exclude from features
    
    Returns:
        Tuple of (feature DataFrame, target Series)
    """
    if exclude_cols is None:
        exclude_cols = ['athlete_id', 'week', 'injured', 'injury_type', 'injury_week']
    
    feature_cols = [col for col in df.columns if col not in exclude_cols + [target_col]]
    X = df[feature_cols].copy()
    y = df[target_col].copy() if target_col in df.columns else None
    
    return X, y


def split_data_by_time(df: pd.DataFrame,
                       train_weeks: Tuple[int, int] = (1, 14),
                       val_weeks: Tuple[int, int] = (15, 19),
                       test_weeks: Tuple[int, int] = (20, 24),
                       target_col: str = 'injured') -> Tuple[pd.DataFrame, pd.Series, 
                                                              pd.DataFrame, pd.Series,
                                                              pd.DataFrame, pd.Series]:
    """
    Split data by time (weeks) to avoid data leakage.
    
    Important: Split by time, not randomly, to simulate real-world prediction.
    
    Args:
        df: DataFrame with training data
        train_weeks: (start, end) weeks for training set
        val_weeks: (start, end) weeks for validation set
        test_weeks: (start, end) weeks for test set
        target_col: Name of target column
    
    Returns:
        Tuple of (X_train, y_train, X_val, y_val, X_test, y_test)
    """
    # Training set
    train_mask = (df['week'] >= train_weeks[0]) & (df['week'] <= train_weeks[1])
    train_df = df[train_mask].copy()
    
    # Validation set
    val_mask = (df['week'] >= val_weeks[0]) & (df['week'] <= val_weeks[1])
    val_df = df[val_mask].copy()
    
    # Test set
    test_mask = (df['week'] >= test_weeks[0]) & (df['week'] <= test_weeks[1])
    test_df = df[test_mask].copy()
    
    # Prepare features and targets
    X_train, y_train = prepare_features_for_training(train_df, target_col)
    X_val, y_val = prepare_features_for_training(val_df, target_col)
    X_test, y_test = prepare_features_for_training(test_df, target_col)
    
    return X_train, y_train, X_val, y_val, X_test, y_test


def create_feature_pipeline(df: pd.DataFrame,
                           target_col: str = 'injured',
                           scale_features_flag: bool = True,
                           scaler_type: str = 'standard') -> Tuple[pd.DataFrame, pd.Series, object]:
    """
    Complete preprocessing pipeline.
    
    Args:
        df: Raw DataFrame with features
        target_col: Name of target column
        scale_features_flag: Whether to scale features
        scaler_type: Type of scaler to use
    
    Returns:
        Tuple of (processed DataFrame, target Series, fitted scaler)
    """
    # Handle missing values
    df = handle_missing_values(df, method='forward_fill')
    
    # Encode categorical features
    df, encoders = encode_categorical_features(df)
    
    # Scale features
    scaler = None
    if scale_features_flag:
        df, scaler = scale_features(df, scaler_type=scaler_type, fit=True)
    
    # Prepare features and target
    X, y = prepare_features_for_training(df, target_col)
    
    return X, y, scaler
