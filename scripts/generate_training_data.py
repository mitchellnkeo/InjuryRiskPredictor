"""
Synthetic Training Data Generator for Injury Risk Predictor

Generates realistic training logs for 100-200 athletes over 24 weeks,
with injury labels based on ACWR and training load spikes.

Based on research from:
- Gabbett, T.J. (2016) - ACWR injury prediction
- Hulin, B.T. et al. (2014) - Week-over-week spikes
- Soligard, T. et al. (2016) - Load monitoring framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import random
from datetime import datetime, timedelta


class TrainingDataGenerator:
    """Generates synthetic training data with realistic patterns and injury labels."""
    
    def __init__(self, n_athletes: int = 150, n_weeks: int = 24, random_seed: int = 42):
        """
        Initialize the data generator.
        
        Args:
            n_athletes: Number of athletes to simulate (default: 150)
            n_weeks: Number of weeks per athlete (default: 24)
            random_seed: Random seed for reproducibility
        """
        self.n_athletes = n_athletes
        self.n_weeks = n_weeks
        self.random_seed = random_seed
        np.random.seed(random_seed)
        random.seed(random_seed)
        
        # Injury risk parameters from research
        self.injury_risk_params = {
            'acwr_high_threshold': 1.5,
            'acwr_high_weeks': 2,  # Consecutive weeks
            'acwr_high_probability': 0.60,
            'spike_threshold': 0.20,  # 20% week-over-week increase
            'spike_probability': 0.40,
            'both_conditions_probability': 0.80
        }
        
    def generate_athlete_profiles(self) -> pd.DataFrame:
        """
        Generate athlete metadata profiles.
        
        Returns:
            DataFrame with columns: athlete_id, age, experience_years, baseline_weekly_miles
        """
        athlete_ids = [f"ATH{i:03d}" for i in range(1, self.n_athletes + 1)]
        
        # Age distribution: mostly 25-45, some younger/older
        ages = np.random.normal(35, 8, self.n_athletes)
        ages = np.clip(ages, 18, 65).astype(int)
        
        # Experience: 0-20 years, correlated with age
        experience = np.random.normal(8, 5, self.n_athletes)
        experience = np.clip(experience, 0, 25).astype(int)
        # Ensure experience doesn't exceed age - 10 (started training as teenager/adult)
        experience = np.minimum(experience, np.maximum(0, ages - 10))
        
        # Baseline weekly miles: 15-60 miles, correlated with experience
        baseline_miles = 15 + (experience * 1.5) + np.random.normal(0, 8, self.n_athletes)
        baseline_miles = np.clip(baseline_miles, 10, 80).astype(float)
        
        profiles = pd.DataFrame({
            'athlete_id': athlete_ids,
            'age': ages,
            'experience_years': experience,
            'baseline_weekly_miles': baseline_miles
        })
        
        return profiles
    
    def generate_weekly_load_pattern(
        self, 
        baseline: float, 
        experience: int,
        pattern_type: str = 'progressive'
    ) -> List[float]:
        """
        Generate realistic weekly training load pattern.
        
        Args:
            baseline: Baseline weekly mileage
            experience: Years of training experience
            pattern_type: 'safe', 'moderate', or 'aggressive'
        
        Returns:
            List of weekly loads (miles) for n_weeks
        """
        weeks = []
        current_load = baseline * (0.7 + np.random.random() * 0.3)  # Start 70-100% of baseline
        
        for week in range(self.n_weeks):
            # Add some natural variation
            variation = np.random.normal(0, baseline * 0.1)  # ±10% variation
            
            if pattern_type == 'safe':
                # Safe progressive loading: gradual increases, occasional plateaus
                if week % 4 == 0 and week > 0:
                    # Build phase: increase 3-8%
                    increase = baseline * np.random.uniform(0.03, 0.08)
                    current_load = min(current_load + increase, baseline * 1.3)
                elif week % 6 == 0:
                    # Recovery week: decrease 10-20%
                    current_load = max(current_load * 0.8, baseline * 0.7)
                else:
                    # Maintain with small variation
                    current_load = current_load + variation
                    
            elif pattern_type == 'moderate':
                # Moderate spikes: occasional 10-20% increases
                if week % 5 == 0 and week > 0:
                    # Moderate spike
                    spike = baseline * np.random.uniform(0.10, 0.20)
                    current_load = min(current_load + spike, baseline * 1.5)
                elif week % 7 == 0:
                    # Recovery
                    current_load = max(current_load * 0.85, baseline * 0.6)
                else:
                    current_load = current_load + variation
                    
            elif pattern_type == 'aggressive':
                # Aggressive spikes: frequent 15-30% increases
                if week % 3 == 0 and week > 0:
                    # Aggressive spike
                    spike = baseline * np.random.uniform(0.15, 0.30)
                    current_load = min(current_load + spike, baseline * 1.8)
                elif week % 8 == 0:
                    # Occasional recovery
                    current_load = max(current_load * 0.75, baseline * 0.5)
                else:
                    current_load = current_load + variation
            
            # Add realistic noise (missed days, weather, life events)
            noise_factor = np.random.choice([1.0, 0.7, 0.5, 0.0], p=[0.7, 0.15, 0.1, 0.05])
            weekly_load = max(0, current_load * noise_factor + variation)
            
            weeks.append(round(weekly_load, 1))
            current_load = weekly_load  # Update for next week
        
        return weeks
    
    def calculate_features(self, weekly_loads: List[float]) -> pd.DataFrame:
        """
        Calculate ACWR and other features from weekly loads.
        
        Args:
            weekly_loads: List of weekly training loads
        
        Returns:
            DataFrame with calculated features
        """
        # Convert to daily loads (simplified: distribute evenly across 7 days, with rest days)
        daily_loads_list = []
        for weekly_load in weekly_loads:
            # Distribute load across 5-6 days (1-2 rest days)
            training_days = np.random.choice([5, 6], p=[0.6, 0.4])
            daily_dist = np.random.dirichlet([1] * training_days) * weekly_load
            daily_week = list(daily_dist) + [0.0] * (7 - training_days)
            np.random.shuffle(daily_week)  # Shuffle rest days
            # Store as string representation for CSV compatibility
            daily_loads_list.append(','.join([str(round(d, 1)) for d in daily_week]))
        
        # Calculate rolling features
        df = pd.DataFrame({
            'week': range(1, len(weekly_loads) + 1),
            'weekly_load': weekly_loads,
            'daily_loads': daily_loads_list
        })
        
        # For weekly data:
        # Acute load: Current week's load (represents last 7 days)
        df['acute_load'] = df['weekly_load']
        
        # Chronic load: 4-week rolling mean (28 days = 4 weeks)
        # This represents the average weekly load over the last 4 weeks
        df['chronic_load'] = df['weekly_load'].rolling(window=4, min_periods=1).mean()
        
        # ACWR
        df['acwr'] = df.apply(
            lambda row: row['acute_load'] / row['chronic_load'] if row['chronic_load'] > 0 else 0,
            axis=1
        )
        
        # Week-over-week change
        df['week_over_week_change'] = df['weekly_load'].pct_change().fillna(0)
        
        # Monotony: mean / std over last 4 weeks
        df['monotony'] = df['weekly_load'].rolling(window=4, min_periods=1).apply(
            lambda x: x.mean() / x.std() if x.std() > 0 else 1.0
        )
        
        # Strain
        df['strain'] = df['weekly_load'] * df['monotony']
        
        return df
    
    def determine_injury_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Determine injury events based on ACWR and spikes.
        
        Args:
            df: DataFrame with calculated features
        
        Returns:
            DataFrame with injury labels
        """
        df = df.copy()  # Work on a copy to avoid modifying original
        df['injured'] = False
        df['injury_type'] = 'none'  # 'none' for non-injured (avoids missing values)
        df['injury_week'] = 0  # 0 for non-injured (avoids missing values)
        
        for i in range(len(df)):
            if df.iloc[i]['injured']:  # Skip if already injured
                continue
            
            week = df.iloc[i]['week']
            acwr = df.iloc[i]['acwr']
            week_change = df.iloc[i]['week_over_week_change']
            
            # Check conditions
            acwr_high = acwr > self.injury_risk_params['acwr_high_threshold']
            spike_high = week_change > self.injury_risk_params['spike_threshold']
            
            # Check consecutive weeks with high ACWR
            if i >= self.injury_risk_params['acwr_high_weeks'] - 1:
                start_idx = i - self.injury_risk_params['acwr_high_weeks'] + 1
                recent_acwr = df.iloc[start_idx:i + 1]['acwr']
                consecutive_high_acwr = (recent_acwr > self.injury_risk_params['acwr_high_threshold']).all()
            else:
                consecutive_high_acwr = False
            
            # Determine injury probability
            injury_prob = 0.0
            injury_type = None
            
            if consecutive_high_acwr and spike_high:
                injury_prob = self.injury_risk_params['both_conditions_probability']
                injury_type = 'high_acwr_and_spike'
            elif consecutive_high_acwr:
                injury_prob = self.injury_risk_params['acwr_high_probability']
                injury_type = 'high_acwr'
            elif spike_high:
                injury_prob = self.injury_risk_params['spike_probability']
                injury_type = 'spike'
            
            # Random injury event
            if injury_prob > 0 and np.random.random() < injury_prob:
                df.at[i, 'injured'] = True
                df.at[i, 'injury_type'] = injury_type
                df.at[i, 'injury_week'] = week
        
        return df
    
    def generate_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Generate complete dataset for all athletes.
        
        Returns:
            Tuple of (training_logs_df, athlete_metadata_df)
        """
        # Generate athlete profiles
        athlete_profiles = self.generate_athlete_profiles()
        
        # Assign training patterns
        # 30% safe, 40% moderate, 30% aggressive
        n_safe = int(self.n_athletes * 0.3)
        n_moderate = int(self.n_athletes * 0.4)
        n_aggressive = self.n_athletes - n_safe - n_moderate
        
        patterns = ['safe'] * n_safe + ['moderate'] * n_moderate + ['aggressive'] * n_aggressive
        np.random.shuffle(patterns)
        athlete_profiles['training_pattern'] = patterns
        
        # Generate training data for each athlete
        all_training_logs = []
        
        for idx, athlete in athlete_profiles.iterrows():
            athlete_id = athlete['athlete_id']
            baseline = athlete['baseline_weekly_miles']
            experience = athlete['experience_years']
            pattern = athlete['training_pattern']
            
            # Generate weekly loads
            weekly_loads = self.generate_weekly_load_pattern(baseline, experience, pattern)
            
            # Calculate features
            df = self.calculate_features(weekly_loads)
            
            # Add athlete info
            df['athlete_id'] = athlete_id
            df['age'] = athlete['age']
            df['experience_years'] = athlete['experience_years']
            df['baseline_weekly_miles'] = baseline
            
            # Determine injuries
            df = self.determine_injury_risk(df)
            
            all_training_logs.append(df)
        
        # Combine all athletes
        training_logs = pd.concat(all_training_logs, ignore_index=True)
        
        # Reorder columns
        column_order = [
            'athlete_id', 'week', 'age', 'experience_years', 'baseline_weekly_miles',
            'weekly_load', 'daily_loads', 'acute_load', 'chronic_load', 'acwr',
            'monotony', 'strain', 'week_over_week_change',
            'injured', 'injury_type', 'injury_week'
        ]
        training_logs = training_logs[column_order]
        
        return training_logs, athlete_profiles
    
    def save_data(self, training_logs: pd.DataFrame, athlete_profiles: pd.DataFrame, 
                  output_dir: str = 'data'):
        """
        Save generated data to CSV files.
        
        Args:
            training_logs: Training logs DataFrame
            athlete_profiles: Athlete profiles DataFrame
            output_dir: Output directory path
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Ensure no missing values - injury_type and injury_week should already be filled
        # Convert injury_week to int (0 for non-injured)
        training_logs_clean = training_logs.copy()
        training_logs_clean['injury_week'] = training_logs_clean['injury_week'].fillna(0).astype(int)
        training_logs_clean['injury_type'] = training_logs_clean['injury_type'].fillna('none')
        
        # Save training logs (na_rep='' handles any remaining NaN as empty strings)
        training_logs_clean.to_csv(f'{output_dir}/training_logs.csv', index=False, na_rep='')
        
        # Save athlete metadata
        athlete_profiles.to_csv(f'{output_dir}/athlete_metadata.csv', index=False)
        
        print(f"Data saved to {output_dir}/")
        print(f"Training logs: {len(training_logs)} rows")
        print(f"Athlete profiles: {len(athlete_profiles)} athletes")


def main():
    """Main function to generate and save data."""
    print("Generating synthetic training data...")
    print("=" * 50)
    
    generator = TrainingDataGenerator(n_athletes=150, n_weeks=24, random_seed=42)
    training_logs, athlete_profiles = generator.generate_all_data()
    
    # Print summary statistics
    print("\nDataset Summary:")
    print(f"Total athletes: {len(athlete_profiles)}")
    print(f"Total weeks: {len(training_logs)}")
    print(f"Total data points: {len(training_logs)}")
    print(f"\nInjury Statistics:")
    print(f"Total injuries: {training_logs['injured'].sum()}")
    print(f"Injury rate: {training_logs['injured'].mean() * 100:.1f}%")
    print(f"\nACWR Statistics:")
    print(f"Mean ACWR: {training_logs['acwr'].mean():.2f}")
    print(f"ACWR range: {training_logs['acwr'].min():.2f} - {training_logs['acwr'].max():.2f}")
    print(f"High ACWR (>1.5): {(training_logs['acwr'] > 1.5).sum()} weeks ({((training_logs['acwr'] > 1.5).sum() / len(training_logs) * 100):.1f}%)")
    
    # Save data
    generator.save_data(training_logs, athlete_profiles)
    
    print("\nData generation complete!")


if __name__ == '__main__':
    main()
