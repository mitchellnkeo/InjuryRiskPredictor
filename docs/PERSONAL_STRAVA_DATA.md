# Using Personal Strava Data

## Overview

Using your own personal Strava data is **much easier** than collecting data from multiple athletes. This guide covers how to replace synthetic data with your personal training data.

---

## Difficulty Assessment

### Overall Difficulty: ⭐⭐ **Easy to Medium** (1-2 weeks)

**Why it's easier:**
- ✅ No privacy/consent issues (your own data)
- ✅ No need for surveys or partnerships
- ✅ Strava API access is straightforward for personal data
- ✅ You know your own injury history
- ✅ Can start immediately

**Challenges:**
- ⚠️ Single athlete = limited data (need historical data)
- ⚠️ Need to self-report injuries
- ⚠️ May need to aggregate data over time

---

## Step 1: Get Your Strava Data

### Option A: Strava API (Recommended)

**Steps:**
1. **Create Strava App:**
   - Go to https://www.strava.com/settings/api
   - Click "Create App"
   - Fill in app details (name: "Injury Risk Predictor")
   - Get Client ID and Client Secret

2. **Authenticate:**
   - Use OAuth2 to get access token
   - This gives you access to your own data

3. **Fetch Activities:**
   - Use Strava API to get all your activities
   - Filter by sport type (running)
   - Get date, distance, time, etc.

**API Endpoints:**
- `GET /athlete/activities` - List all activities
- `GET /activities/{id}` - Get activity details
- Can get years of historical data

**Difficulty:** ⭐ Easy (Strava has good documentation)

### Option B: Strava Data Export (Easier, No API)

**Steps:**
1. **Request Data Export:**
   - Go to https://www.strava.com/athlete/delete_your_account
   - Click "Request Your Account Data"
   - Strava will email you a ZIP file with all your data

2. **Extract Data:**
   - Unzip the file
   - Find `activities.csv` file
   - Contains all your activities in CSV format

**Difficulty:** ⭐ Very Easy (no coding needed)

**Pros:**
- No API setup required
- Get all historical data at once
- CSV format is easy to work with

**Cons:**
- One-time export (not live)
- Need to request again for new data

---

## Step 2: Convert Strava Data to Our Schema

### Strava CSV Format (from data export)

Typical columns:
- `Activity Date`
- `Activity Name`
- `Activity Type` (Run, Ride, etc.)
- `Distance` (km)
- `Moving Time` (seconds)
- `Elapsed Time` (seconds)
- `Elevation Gain` (meters)
- etc.

### Our Schema

```python
{
    'athlete_id': 'PERSONAL',
    'week': 1,
    'weekly_load': 35.0,  # miles
    'daily_loads': [7, 8, 0, 6, 7, 7, 0],
    'injured': False,
    'injury_type': 'none',
    'injury_week': 0
}
```

### Conversion Script

```python
# scripts/convert_strava_data.py
import pandas as pd
from datetime import datetime, timedelta

def convert_strava_to_schema(strava_csv_path, start_date=None):
    """
    Convert Strava export CSV to our training log schema.
    
    Args:
        strava_csv_path: Path to Strava activities.csv
        start_date: Start date for analysis (default: earliest activity)
    
    Returns:
        DataFrame matching our training_logs schema
    """
    # Load Strava data
    df = pd.read_csv(strava_csv_path)
    
    # Filter for running activities only
    df = df[df['Activity Type'] == 'Run'].copy()
    
    # Convert date
    df['Activity Date'] = pd.to_datetime(df['Activity Date'])
    
    # Convert distance from km to miles
    df['distance_miles'] = df['Distance'] * 0.621371
    
    # Group by week
    df['week_start'] = df['Activity Date'].dt.to_period('W').dt.start_time
    df['week'] = (df['week_start'] - df['week_start'].min()).dt.days // 7 + 1
    
    # Aggregate to weekly loads
    weekly_loads = df.groupby('week').agg({
        'distance_miles': 'sum',
        'Activity Date': ['min', 'max', 'count']
    }).reset_index()
    
    weekly_loads.columns = ['week', 'weekly_load', 'week_start', 'week_end', 'num_runs']
    
    # Create daily breakdown (simplified - distribute evenly)
    # In reality, you'd use actual daily data from Strava
    daily_loads_list = []
    for _, row in weekly_loads.iterrows():
        # Get daily data for this week
        week_data = df[(df['week'] == row['week'])]
        daily_dist = week_data.groupby(week_data['Activity Date'].dt.date)['distance_miles'].sum()
        
        # Create 7-day array
        week_start = pd.to_datetime(row['week_start']).date()
        daily_array = [0.0] * 7
        for i in range(7):
            day = week_start + timedelta(days=i)
            if day in daily_dist.index:
                daily_array[i] = float(daily_dist[day])
        
        daily_loads_list.append(','.join([str(round(d, 1)) for d in daily_array]))
    
    weekly_loads['daily_loads'] = daily_loads_list
    
    # Add athlete metadata
    weekly_loads['athlete_id'] = 'PERSONAL'
    weekly_loads['age'] = 30  # Your age (update)
    weekly_loads['experience_years'] = 5  # Your experience (update)
    weekly_loads['baseline_weekly_miles'] = weekly_loads['weekly_load'].median()
    
    # Add injury columns (you'll fill these manually)
    weekly_loads['injured'] = False
    weekly_loads['injury_type'] = 'none'
    weekly_loads['injury_week'] = 0
    
    # Reorder columns to match schema
    columns = ['athlete_id', 'week', 'age', 'experience_years', 'baseline_weekly_miles',
               'weekly_load', 'daily_loads', 'injured', 'injury_type', 'injury_week']
    
    return weekly_loads[columns]
```

**Difficulty:** ⭐⭐ Medium (2-3 days)
- Need to handle date grouping
- Unit conversions
- Daily aggregation
- Schema mapping

---

## Step 3: Add Injury Labels

### Manual Injury Tracking

**Option A: CSV File**
Create `data/personal_injuries.csv`:
```csv
week,injured,injury_type,notes
15,True,high_acwr,"Knee pain after high mileage week"
23,True,spike,"Shin splints after 30% increase"
```

**Option B: Add to Training Logs**
Manually edit the converted CSV to add injury flags:
- Mark weeks where you were injured
- Add injury type
- Add notes if helpful

**Option C: Simple Script**
```python
# Mark injuries based on your memory/records
injuries = {
    15: {'injured': True, 'injury_type': 'high_acwr'},
    23: {'injured': True, 'injury_type': 'spike'},
    # Add more as needed
}

for week, injury_data in injuries.items():
    df.loc[df['week'] == week, 'injured'] = injury_data['injured']
    df.loc[df['week'] == week, 'injury_type'] = injury_data['injury_type']
```

**Difficulty:** ⭐ Easy (just need to remember/report injuries)

---

## Step 4: Update Data Loading

### Modify Existing Code

**Option A: Keep Both (Recommended)**

```python
# scripts/load_data.py
def load_training_data(data_source='synthetic'):
    """
    Load training data from specified source.
    
    Args:
        data_source: 'synthetic' or 'personal_strava'
    """
    if data_source == 'synthetic':
        return pd.read_csv('data/training_logs.csv')
    elif data_source == 'personal_strava':
        return pd.read_csv('data/personal_training_logs.csv')
    else:
        raise ValueError(f"Unknown data source: {data_source}")
```

**Option B: Replace Synthetic**

Just update notebooks to load from `data/personal_training_logs.csv` instead of `data/training_logs.csv`

**Difficulty:** ⭐ Very Easy (just change file path)

---

## Complete Implementation Plan

### Week 1: Data Collection & Conversion

**Day 1-2: Get Strava Data**
- [ ] Request Strava data export OR set up API
- [ ] Download activities.csv
- [ ] Review data structure

**Day 3-4: Create Conversion Script**
- [ ] Write `scripts/convert_strava_data.py`
- [ ] Handle unit conversions (km → miles)
- [ ] Aggregate daily → weekly
- [ ] Map to our schema
- [ ] Test conversion

**Day 5: Add Injury Labels**
- [ ] Review training history
- [ ] Mark injury weeks
- [ ] Add injury types
- [ ] Validate injury data

**Day 6-7: Integration**
- [ ] Update data loading
- [ ] Test feature engineering
- [ ] Run EDA on personal data
- [ ] Compare to synthetic data

### Week 2: Validation & Model Training

**Day 1-2: Data Validation**
- [ ] Check data quality
- [ ] Validate ACWR calculations
- [ ] Check injury rates
- [ ] Compare distributions

**Day 3-5: Model Training**
- [ ] Engineer features on personal data
- [ ] Train models
- [ ] Compare performance
- [ ] Validate predictions

---

## Challenges with Personal Data

### 1. Single Athlete = Limited Data

**Challenge:**
- Only one athlete = less diversity
- May not have enough data points
- Can't generalize to other athletes

**Solutions:**
- Use historical data (years of training)
- Aggregate into multiple "seasons" if you have enough data
- Use for personal predictions (not general model)
- Can still demonstrate the pipeline works

### 2. Injury Data Quality

**Challenge:**
- Self-reported injuries
- May forget minor injuries
- Recall bias

**Solutions:**
- Use training logs/notes if you kept them
- Mark obvious injuries (large training gaps)
- Be conservative (only mark clear injuries)
- Document uncertainty

### 3. Data Volume

**Challenge:**
- May not have 24+ weeks of consistent data
- May have gaps (off-seasons, breaks)

**Solutions:**
- Use all available data
- Handle gaps gracefully
- May need to adjust time windows
- Can still demonstrate the approach

### 4. Generalization

**Challenge:**
- Model trained on one person won't generalize
- Personal model vs general model

**Solutions:**
- This is fine for personal use case
- Can demonstrate the pipeline works
- Can combine with synthetic data for general model
- Personal model might be more accurate for you!

---

## Code Changes Required

### New Files Needed:

1. **`scripts/convert_strava_data.py`** - Convert Strava CSV to our schema
2. **`scripts/add_personal_injuries.py`** - Helper to add injury labels
3. **`data/personal_training_logs.csv`** - Your converted data

### Files to Update:

1. **Notebooks** - Change data source path
2. **Data loading** - Add option for personal data

### Files That DON'T Need Changes:

- ✅ `src/ml/features.py` - Works as-is
- ✅ `src/ml/preprocessing.py` - Works as-is
- ✅ Model training code - Works as-is

**Total Code Changes:** Minimal (~200-300 lines)

---

## Example: Complete Workflow

### 1. Get Strava Data Export

```bash
# Request export from Strava website
# Download activities.csv
```

### 2. Convert Data

```python
# scripts/convert_strava_data.py
from convert_strava_data import convert_strava_to_schema

df = convert_strava_to_schema('strava_export/activities.csv')
df.to_csv('data/personal_training_logs.csv', index=False)
```

### 3. Add Injuries

```python
# Manually edit CSV or use script
# Mark weeks where you were injured
```

### 4. Use in Pipeline

```python
# notebooks/02_exploratory_analysis.ipynb
# Change this line:
training_logs = pd.read_csv('../data/personal_training_logs.csv')
# Instead of:
# training_logs = pd.read_csv('../data/training_logs.csv')
```

### 5. Everything Else Works!

- Feature engineering: ✅ Works as-is
- EDA: ✅ Works as-is
- Model training: ✅ Works as-is

---

## Interview Answer

**Question:** "Could you use your own Strava data instead of synthetic data?"

**Answer:**
"Absolutely, and it would actually be much easier than collecting data from multiple athletes. Here's how:

1. **Data Collection:** Strava allows you to export all your historical data as a CSV file - no API needed. This gives me years of training data in one file.

2. **Conversion:** I'd create a simple script to convert Strava's format (activities with dates, distances in km) to our schema (weekly loads in miles). This is straightforward - just group activities by week and aggregate distances.

3. **Injury Labels:** I'd manually mark weeks where I was injured based on my training history and memory. This is the easiest part since I know my own injury history.

4. **Integration:** The feature engineering and model training code would work as-is - they're data-agnostic. I'd just change the data loading path in the notebooks.

**Difficulty: Easy to Medium (1-2 weeks)**

The main limitation is that it's only one athlete, so the model would be personalized to me rather than generalizable. But it would:
- Demonstrate the pipeline works with real data
- Show I can adapt to different data sources
- Create a personal injury prediction tool
- Validate the approach with real-world data

For a portfolio project, this is actually a great approach - it shows I can work with real data sources and adapt the system accordingly."

---

## Benefits of Personal Data

1. **Real Data:** Actual training patterns, not simulated
2. **No Privacy Issues:** Your own data
3. **Personalized Model:** Might be more accurate for you
4. **Demonstrates Adaptability:** Shows you can work with different data sources
5. **Quick to Implement:** Much faster than multi-athlete collection

---

## Recommended Approach

### Phase 1: Quick Proof of Concept (3-5 days)

1. Export your Strava data
2. Create simple conversion script
3. Add a few injury labels (even if just 2-3 injuries)
4. Run the pipeline end-to-end
5. Validate it works

### Phase 2: Full Implementation (1-2 weeks)

1. Refine conversion script
2. Add all injury history
3. Validate data quality
4. Retrain models
5. Compare to synthetic data

### Phase 3: Hybrid Approach (Optional)

1. Use personal data for validation
2. Keep synthetic data for general model
3. Show both approaches work
4. Demonstrate adaptability

---

## Summary

**Feasibility:** ✅ Very Feasible

**Difficulty:** ⭐⭐ Easy to Medium (1-2 weeks)

**Main Steps:**
1. Export Strava data (very easy)
2. Convert to our schema (medium - 2-3 days)
3. Add injury labels (easy - manual)
4. Update data loading (very easy - change path)

**Code Changes:** Minimal (~200-300 lines)

**Benefits:**
- Real data
- No privacy issues
- Quick to implement
- Demonstrates adaptability
- Personal model

**Limitations:**
- Single athlete (less generalizable)
- Self-reported injuries
- May have limited data volume

**Recommendation:** This is a great approach! Start with a quick proof of concept (3-5 days) to validate it works, then do full implementation if you want a personal model.
