# Features to Engineer - Injury Risk Predictor

This document outlines all features that will be engineered from raw training data to predict injury risk.

---

## Core Metrics (Primary Features)

### 1. Acute Load
- **Definition:** Sum of training volume over the last 7 days
- **Calculation:** Rolling 7-day sum
- **Units:** Miles (for running MVP)
- **Purpose:** Represents recent training stress
- **Implementation:** `pandas.rolling(window=7, min_periods=1).sum()`

### 2. Chronic Load
- **Definition:** Average training volume over the last 28 days
- **Calculation:** Rolling 28-day mean
- **Units:** Miles (for running MVP)
- **Purpose:** Represents athlete's fitness baseline/adaptation level
- **Implementation:** `pandas.rolling(window=28, min_periods=1).mean()`

### 3. ACWR (Acute:Chronic Workload Ratio)
- **Definition:** Acute Load / Chronic Load
- **Calculation:** `acute_load / chronic_load` (handle division by zero)
- **Range:** Typically 0.5 - 2.5
- **Purpose:** Primary injury risk indicator
- **Risk Zones:**
  - < 0.8: Undertrained
  - 0.8-1.3: Sweet spot (low risk)
  - 1.3-1.5: Moderate risk
  - > 1.5: High risk

### 4. Training Monotony
- **Definition:** Mean weekly load / Standard deviation of weekly loads
- **Calculation:** `mean(weekly_loads) / std(weekly_loads)` (over last 4-8 weeks)
- **Range:** Typically 1.0 - 3.0+
- **Purpose:** Measures training variation (high = repetitive = risky)
- **Threshold:** > 2.0 indicates high monotony (injury risk)

### 5. Training Strain
- **Definition:** Total weekly load × Monotony
- **Calculation:** `weekly_load × monotony`
- **Purpose:** Captures both volume and variation
- **Interpretation:** High strain = high volume + high monotony = very risky

### 6. Week-over-Week Change
- **Definition:** Percentage change in weekly load from previous week
- **Calculation:** `(current_week - previous_week) / previous_week × 100`
- **Range:** Can be negative (decrease) or positive (increase)
- **Purpose:** Identifies sudden spikes in training
- **Risk Threshold:** > 10-15% increase = moderate risk, > 20% = high risk

---

## Derived Features (Secondary Features)

### 7. ACWR Trend
- **Definition:** 2-week slope of ACWR values
- **Calculation:** Linear regression slope of ACWR over last 2 weeks
- **Values:** Positive (increasing), negative (decreasing), zero (stable)
- **Purpose:** Identifies if athlete is trending toward danger zone

### 8. Weeks Above Threshold
- **Definition:** Consecutive weeks with ACWR > 1.3
- **Calculation:** Count consecutive weeks where ACWR > 1.3
- **Purpose:** Sustained high ACWR is more dangerous than a single spike
- **Risk:** 2+ consecutive weeks = increased risk

### 9. Distance from Baseline
- **Definition:** Current weekly load vs athlete's typical/baseline load
- **Calculation:** `(current_load - baseline_load) / baseline_load × 100`
- **Baseline:** Median or mean of athlete's historical loads (e.g., last 12 weeks)
- **Purpose:** Personalizes risk assessment (what's risky for one athlete may be normal for another)

### 10. Previous Week ACWR (Lag Feature)
- **Definition:** ACWR value from 1 week ago
- **Calculation:** `acwr.shift(1)` (lag by 1 week)
- **Purpose:** Captures temporal patterns and momentum
- **Use Case:** Recent high ACWR may indicate ongoing risk

### 11. 2-Week Ago ACWR (Lag Feature)
- **Definition:** ACWR value from 2 weeks ago
- **Calculation:** `acwr.shift(2)` (lag by 2 weeks)
- **Purpose:** Captures longer-term patterns

### 12. Recent Injury History
- **Definition:** Binary indicator if athlete was injured in last 8 weeks
- **Calculation:** `1 if injured_in_last_8_weeks else 0`
- **Purpose:** Recent injury increases risk of re-injury
- **Implementation:** Check injury flags in last 8 weeks of data

---

## Athlete-Specific Features

### 13. Age Group
- **Definition:** Binned age categories
- **Categories:**
  - 18-25: Young adult
  - 26-35: Adult
  - 36-45: Masters
  - 46+: Senior
- **Purpose:** Age affects injury risk and recovery
- **Calculation:** `pd.cut(age, bins=[18, 26, 36, 46, 100], labels=['young', 'adult', 'masters', 'senior'])`

### 14. Experience Level
- **Definition:** Years of training experience
- **Categories:**
  - 0-2 years: Novice
  - 3-5 years: Intermediate
  - 6-10 years: Advanced
  - 10+ years: Expert
- **Purpose:** More experienced athletes may handle load spikes better
- **Calculation:** `pd.cut(experience_years, bins=[0, 3, 6, 10, 100], labels=['novice', 'intermediate', 'advanced', 'expert'])`

### 15. Baseline Weekly Load
- **Definition:** Athlete's typical weekly training volume
- **Calculation:** Median or mean of historical weekly loads (e.g., last 12 weeks)
- **Purpose:** Normalizes features relative to athlete's capacity
- **Use:** Helps identify what's "high" for this specific athlete

---

## Interaction Features (Advanced)

### 16. ACWR × Age
- **Definition:** Interaction between ACWR and age
- **Calculation:** `acwr × age`
- **Purpose:** Older athletes may be more sensitive to high ACWR

### 17. ACWR × Experience
- **Definition:** Interaction between ACWR and experience level
- **Calculation:** `acwr × experience_years`
- **Purpose:** Experienced athletes may tolerate higher ACWR

### 18. Strain × Experience
- **Definition:** Interaction between strain and experience
- **Calculation:** `strain × experience_years`
- **Purpose:** Experienced athletes may handle high strain better

---

## Feature Engineering Pipeline

### Input Data Requirements:
- **Minimum:** 28 days of training history (for chronic load calculation)
- **Ideal:** 8+ weeks of weekly training data
- **Daily Data:** Optional but helpful for more accurate acute load

### Data Preprocessing:
1. **Handle Missing Values:**
   - Forward fill for rolling windows
   - Interpolate missing days
   - Flag weeks with insufficient data

2. **Normalization:**
   - Scale numerical features (StandardScaler or MinMaxScaler)
   - Encode categorical features (one-hot encoding)

3. **Temporal Validation:**
   - Ensure no data leakage (only use past data to predict future)
   - Validate rolling window calculations

### Feature Calculation Order:
1. Calculate rolling windows (acute, chronic)
2. Calculate ACWR
3. Calculate monotony (requires multiple weeks)
4. Calculate strain
5. Calculate week-over-week change
6. Calculate derived features (trends, lags)
7. Add athlete-specific features
8. Create interaction features (if using)

---

## Feature Importance Expectations

Based on research, expected feature importance (from highest to lowest):
1. **ACWR** - Primary predictor
2. **Week-over-Week Change** - Identifies spikes
3. **Training Strain** - Volume + variation
4. **Monotony** - Training variation
5. **Weeks Above Threshold** - Sustained risk
6. **Recent Injury History** - Re-injury risk
7. **Experience Level** - Individual resilience
8. **Age Group** - Recovery capacity
9. **ACWR Trend** - Direction of risk
10. **Distance from Baseline** - Personalized risk

---

## Feature Validation

### Unit Tests Required:
- [ ] ACWR calculation matches research thresholds
- [ ] Monotony calculation handles edge cases (zero std dev)
- [ ] Week-over-week change handles first week (no previous week)
- [ ] Rolling windows handle insufficient data (< 28 days)
- [ ] No data leakage (features only use past data)
- [ ] Feature ranges are reasonable (ACWR 0.5-2.5, etc.)

### Validation Checks:
- [ ] ACWR distribution matches research (most values 0.8-1.3)
- [ ] High ACWR correlates with injuries in dataset
- [ ] Features are not highly correlated (avoid multicollinearity)
- [ ] Missing values handled appropriately

---

## Future Feature Ideas (Post-MVP)

- **Training Intensity:** Incorporate heart rate zones, pace zones
- **Recovery Metrics:** Sleep, stress, HRV (heart rate variability)
- **Sport-Specific:** Running pace, cycling power, strength training volume
- **Environmental:** Weather, altitude, terrain
- **Biomechanical:** Gait analysis, movement patterns
- **Nutrition:** Caloric intake, hydration
- **Time-Based:** Time of day, day of week patterns

---

## Summary

**Total Features for MVP: 13-15 core features**
- 6 core metrics (ACWR, monotony, strain, etc.)
- 5-7 derived features (trends, lags, athlete-specific)
- 2-3 interaction features (optional, for advanced models)

**Minimum Features for Baseline: 5**
- ACWR (primary)
- Week-over-week change
- Monotony
- Strain
- Recent injury history
