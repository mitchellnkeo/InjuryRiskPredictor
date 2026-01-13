"""
Convert Personal Strava Data Export to Training Logs Schema

This script converts Strava's activities.csv export to our training_logs.csv format.

Usage:
1. Request your Strava data export from https://www.strava.com/athlete/delete_your_account
2. Download and unzip the export
3. Run: python scripts/convert_strava_data.py path/to/activities.csv
4. Manually add injury labels to the output CSV
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


def convert_strava_to_schema(strava_csv_path, output_path='data/personal_training_logs.csv',
                             athlete_id='PERSONAL', age=30, experience_years=5):
    """
    Convert Strava activities.csv to our training logs schema.
    
    Args:
        strava_csv_path: Path to Strava activities.csv file
        output_path: Where to save the converted data
        athlete_id: ID for the athlete (default: 'PERSONAL')
        age: Your age
        experience_years: Your years of training experience
    
    Returns:
        DataFrame in our training logs schema
    """
    print(f"Loading Strava data from {strava_csv_path}...")
    
    # Load Strava data
    try:
        df = pd.read_csv(strava_csv_path)
    except FileNotFoundError:
        print(f"Error: File not found: {strava_csv_path}")
        print("\nTo get your Strava data:")
        print("1. Go to https://www.strava.com/athlete/delete_your_account")
        print("2. Click 'Request Your Account Data'")
        print("3. Wait for email with download link")
        print("4. Unzip and find activities.csv")
        return None
    
    print(f"Loaded {len(df)} activities")
    
    # Filter for running activities only
    # Strava uses different column names - try common ones
    activity_type_col = None
    for col in ['Activity Type', 'ActivityType', 'type', 'Type']:
        if col in df.columns:
            activity_type_col = col
            break
    
    if activity_type_col:
        df = df[df[activity_type_col].str.contains('Run', case=False, na=False)].copy()
        print(f"Filtered to {len(df)} running activities")
    else:
        print("Warning: Could not find activity type column. Using all activities.")
    
    # Find date column
    date_col = None
    for col in ['Activity Date', 'ActivityDate', 'date', 'Date', 'start_date', 'Start Date']:
        if col in df.columns:
            date_col = col
            break
    
    if not date_col:
        print("Error: Could not find date column in CSV")
        print(f"Available columns: {list(df.columns)}")
        return None
    
    # Convert date
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # Find distance column
    distance_col = None
    for col in ['Distance', 'distance', 'Distance (km)', 'distance_km']:
        if col in df.columns:
            distance_col = col
            break
    
    if not distance_col:
        print("Error: Could not find distance column")
        print(f"Available columns: {list(df.columns)}")
        return None
    
    # Convert distance from km to miles (if needed)
    # Check if already in miles (unlikely but possible)
    if df[distance_col].max() > 100:  # Likely in km if max > 100
        df['distance_miles'] = df[distance_col] * 0.621371
        print("Converted distance from km to miles")
    else:
        df['distance_miles'] = df[distance_col]
        print("Distance appears to be in miles already")
    
    # Group by week
    df['week_start'] = df[date_col].dt.to_period('W').dt.start_time
    df['week'] = ((df['week_start'] - df['week_start'].min()).dt.days // 7) + 1
    
    # Aggregate to weekly loads
    print("Aggregating to weekly loads...")
    weekly_data = []
    
    for week_num in sorted(df['week'].unique()):
        week_df = df[df['week'] == week_num]
        weekly_load = week_df['distance_miles'].sum()
        
        # Create daily breakdown
        week_start_date = week_df['week_start'].iloc[0]
        daily_loads = [0.0] * 7
        
        for i in range(7):
            day_date = week_start_date + timedelta(days=i)
            day_activities = week_df[week_df[date_col].dt.date == day_date.date()]
            if len(day_activities) > 0:
                daily_loads[i] = float(day_activities['distance_miles'].sum())
        
        # Calculate baseline (median of all weeks)
        baseline = df['distance_miles'].sum() / len(df['week'].unique()) if len(df['week'].unique()) > 0 else weekly_load
        
        weekly_data.append({
            'athlete_id': athlete_id,
            'week': int(week_num),
            'age': age,
            'experience_years': experience_years,
            'baseline_weekly_miles': float(baseline),
            'weekly_load': round(weekly_load, 1),
            'daily_loads': ','.join([str(round(d, 1)) for d in daily_loads]),
            'injured': False,  # You'll fill this manually
            'injury_type': 'none',
            'injury_week': 0
        })
    
    result_df = pd.DataFrame(weekly_data)
    
    # Calculate baseline as median of weekly loads
    result_df['baseline_weekly_miles'] = result_df['weekly_load'].median()
    
    # Reorder columns to match schema
    column_order = [
        'athlete_id', 'week', 'age', 'experience_years', 'baseline_weekly_miles',
        'weekly_load', 'daily_loads', 'injured', 'injury_type', 'injury_week'
    ]
    result_df = result_df[column_order]
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Conversion complete!")
    print(f"  Output: {output_path}")
    print(f"  Total weeks: {len(result_df)}")
    print(f"  Date range: {df[date_col].min().date()} to {df[date_col].max().date()}")
    print(f"  Average weekly load: {result_df['weekly_load'].mean():.1f} miles")
    print(f"\n⚠️  Next step: Manually add injury labels to {output_path}")
    print("   Edit the CSV and mark 'injured' = True for weeks you were injured")
    
    return result_df


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python convert_strava_data.py <path_to_activities.csv> [age] [experience_years]")
        print("\nExample:")
        print("  python convert_strava_data.py ~/Downloads/strava_export/activities.csv 30 5")
        print("\nTo get your Strava data:")
        print("  1. Go to https://www.strava.com/athlete/delete_your_account")
        print("  2. Click 'Request Your Account Data'")
        print("  3. Wait for email, download and unzip")
        print("  4. Find activities.csv in the export")
        sys.exit(1)
    
    strava_path = sys.argv[1]
    age = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    experience = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    convert_strava_to_schema(strava_path, age=age, experience_years=experience)


if __name__ == '__main__':
    main()
