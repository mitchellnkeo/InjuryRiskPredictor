"""Simple test script for the data generator."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from generate_training_data import TrainingDataGenerator

# Test with small dataset
print("Testing data generator with 5 athletes, 4 weeks...")
generator = TrainingDataGenerator(n_athletes=5, n_weeks=4, random_seed=42)

# Generate profiles
profiles = generator.generate_athlete_profiles()
print(f"Generated {len(profiles)} athlete profiles")
print(profiles.head())

# Test weekly load generation
test_loads = generator.generate_weekly_load_pattern(30.0, 5, 'moderate')
print(f"\nGenerated {len(test_loads)} weeks of training data")
print(f"Weekly loads: {test_loads}")

# Test feature calculation
df = generator.calculate_features(test_loads)
print(f"\nCalculated features:")
print(df[['week', 'weekly_load', 'acute_load', 'chronic_load', 'acwr']].head())

print("\nTest completed successfully!")
