# Migrating from Synthetic to Real-World Data

## Overview

This document outlines the feasibility, challenges, and steps required to replace synthetic data with real-world athlete training data.

---

## Feasibility Assessment

### ✅ **Yes, it's feasible, but with significant challenges**

**Difficulty Level:** Medium to High

**Time Estimate:** 2-4 weeks (depending on data source and availability)

---

## Data Sources for Real-World Data

### Option 1: Strava API (Recommended)
- **Pros:**
  - Large user base (millions of athletes)
  - Rich training data (distance, time, pace, heart rate)
  - Well-documented API
  - Can anonymize data
- **Cons:**
  - Requires API access (may need approval)
  - No injury data (would need separate collection)
  - Privacy concerns
  - Rate limits
- **Difficulty:** Medium

### Option 2: Manual Data Collection
- **Pros:**
  - Full control over data collection
  - Can collect injury data directly
  - No API limitations
- **Cons:**
  - Time-consuming
  - Requires athlete participation/consent
  - Small sample size likely
  - IRB approval may be needed
- **Difficulty:** High

### Option 3: Public Datasets
- **Pros:**
  - Already collected and cleaned
  - May include injury data
  - No collection effort
- **Cons:**
  - Limited availability
  - May not match exact use case
  - Data quality varies
- **Difficulty:** Low (if available)

### Option 4: Partnership with Sports Organizations
- **Pros:**
  - High-quality data
  - May include injury tracking
  - Professional athletes
- **Cons:**
  - Requires relationships/partnerships
  - Privacy/NDA concerns
  - May be proprietary
- **Difficulty:** Very High

---

## Required Changes to Codebase

### 1. Data Loading Module (Easy - Low Difficulty)

**Current:** Loads from `data/training_logs.csv` (synthetic)

**Changes Needed:**
```python
# New module: src/data/loaders.py
def load_strava_data(athlete_id, start_date, end_date):
    """Load training data from Strava API"""
    # API calls to Strava
    # Convert to our schema
    pass

def load_manual_data(csv_path):
    """Load manually collected data"""
    # Load from custom CSV format
    # Validate schema
    pass
```

**Difficulty:** ⭐ Easy
- Just need to adapt data loading
- Schema mapping (Strava fields → our schema)
- Date handling

### 2. Data Schema Adaptation (Medium Difficulty)

**Current Schema:**
- `weekly_load` (miles)
- `daily_loads` (array)
- `injured` (boolean)
- `injury_type` (string)

**Real Data Challenges:**
- Strava uses different units (kilometers, time, TSS)
- May not have daily breakdown
- Injury data needs separate collection
- Different date formats

**Changes Needed:**
```python
# src/data/adapters.py
def convert_strava_to_schema(strava_data):
    """Convert Strava API response to our schema"""
    # Convert km to miles (or keep km and update features)
    # Aggregate daily data to weekly
    # Handle missing data
    pass
```

**Difficulty:** ⭐⭐ Medium
- Unit conversions
- Data aggregation
- Missing data handling
- Schema validation

### 3. Feature Engineering (Easy - No Changes Needed!)

**Good News:** Feature engineering functions should work as-is!

**Why:**
- Functions take DataFrame + athlete_id + week
- They don't care where data comes from
- As long as schema matches, they'll work

**Potential Adjustments:**
- May need to handle different units (km vs miles)
- May need to adjust for different time granularity (daily vs weekly)
- Missing data handling might need enhancement

**Difficulty:** ⭐ Easy (mostly no changes)

### 4. Injury Data Collection (High Difficulty)

**Biggest Challenge:** Getting injury labels

**Options:**

**A. Survey/Questionnaire:**
- Ask athletes to report injuries
- Pros: Direct injury data
- Cons: Self-reporting bias, low response rate, recall issues

**B. Medical Records:**
- Partner with sports medicine clinics
- Pros: Accurate injury data
- Cons: Privacy, access, HIPAA concerns

**C. Public Injury Reports:**
- Professional athletes (if public)
- Pros: Available data
- Cons: Limited to professionals, may not be detailed

**D. Infer from Training Gaps:**
- Large drop in training = possible injury
- Pros: No direct collection needed
- Cons: Not accurate (could be vacation, illness, etc.)

**Difficulty:** ⭐⭐⭐⭐ High
- This is the hardest part
- Requires separate data collection effort
- Privacy/consent issues

### 5. Data Validation (Medium Difficulty)

**Current:** Validates against research expectations

**Real Data Challenges:**
- May not match research distributions
- Different injury rates
- Different ACWR patterns
- Need to validate data quality

**Changes Needed:**
```python
# Enhanced validation
def validate_real_data(df):
    """Validate real-world data quality"""
    # Check for outliers
    # Validate distributions
    # Check for data quality issues
    # Compare to research (may differ)
    pass
```

**Difficulty:** ⭐⭐ Medium
- More complex validation
- May need to adjust expectations
- Data cleaning required

---

## Step-by-Step Migration Plan

### Phase 1: Data Collection Setup (1-2 weeks)

1. **Choose data source**
   - Strava API (recommended)
   - Set up API access
   - Test data retrieval

2. **Set up data collection**
   - Create data collection scripts
   - Handle authentication
   - Implement rate limiting
   - Store data securely

3. **Injury data collection**
   - Design survey/questionnaire
   - Set up collection system
   - Get IRB approval (if needed)
   - Recruit participants

### Phase 2: Data Adaptation (1 week)

1. **Create data adapters**
   - Convert Strava format to our schema
   - Handle unit conversions
   - Aggregate daily → weekly if needed
   - Map fields correctly

2. **Data cleaning**
   - Handle missing values
   - Remove outliers
   - Validate data quality
   - Check for anomalies

3. **Schema validation**
   - Ensure data matches expected schema
   - Validate required fields
   - Check data types

### Phase 3: Integration (1 week)

1. **Update data loading**
   - Replace synthetic data loader
   - Add real data loader
   - Make it configurable (synthetic vs real)

2. **Test feature engineering**
   - Run features on real data
   - Validate calculations
   - Check for edge cases
   - Compare distributions

3. **Re-run EDA**
   - Validate real data matches expectations
   - Check injury rates
   - Validate ACWR distributions
   - Statistical tests

### Phase 4: Model Retraining (1 week)

1. **Retrain models**
   - Use real data instead of synthetic
   - Compare performance
   - May need hyperparameter tuning
   - Validate feature importance

2. **Evaluate differences**
   - Compare synthetic vs real model performance
   - Check if features still work
   - Validate predictions make sense

---

## Code Changes Required

### Minimal Changes (If Schema Matches)

**Files that need updates:**
1. `scripts/generate_training_data.py` → `scripts/load_real_data.py` (or keep both)
2. `notebooks/01_data_generation.ipynb` → Update or create new loader notebook
3. `src/data/loaders.py` (new file) - Data loading abstraction
4. `src/data/adapters.py` (new file) - Schema conversion

**Files that DON'T need changes:**
- ✅ `src/ml/features.py` - Should work as-is
- ✅ `src/ml/preprocessing.py` - Should work as-is
- ✅ `notebooks/02_exploratory_analysis.ipynb` - Just change data source
- ✅ `notebooks/03_feature_engineering.ipynb` - Just change data source
- ✅ Model training code - Should work with any data

### Code Structure for Real Data

```python
# src/data/loaders.py
class DataLoader:
    """Abstract base class for data loading"""
    def load_training_data(self):
        raise NotImplementedError

class SyntheticDataLoader(DataLoader):
    """Load synthetic data"""
    def load_training_data(self):
        # Current implementation
        pass

class StravaDataLoader(DataLoader):
    """Load data from Strava API"""
    def load_training_data(self):
        # New implementation
        pass

class ManualDataLoader(DataLoader):
    """Load manually collected data"""
    def load_training_data(self):
        # Load from CSV
        pass
```

---

## Challenges & Considerations

### 1. Data Quality Issues

**Challenges:**
- Missing data (athletes don't log every day)
- Inaccurate data (GPS errors, manual entry mistakes)
- Inconsistent units (some in km, some in miles)
- Different sports (running, cycling, swimming)

**Solutions:**
- Robust data cleaning pipeline
- Unit standardization
- Handle missing data gracefully
- Filter by sport type

### 2. Injury Data Collection

**Challenges:**
- Self-reporting bias
- Low response rates
- Recall issues (athletes forget injuries)
- Privacy concerns

**Solutions:**
- Clear survey design
- Incentivize participation
- Partner with sports organizations
- Use medical records (if possible)

### 3. Data Volume

**Challenges:**
- May have fewer athletes than synthetic (150)
- May have shorter time periods
- Missing weeks/months

**Solutions:**
- Collect over longer period
- Recruit more participants
- Use data augmentation (carefully)
- Accept smaller dataset if validated

### 4. Distribution Differences

**Challenges:**
- Real data may not match research distributions
- Different injury rates
- Different ACWR patterns
- May need to adjust model

**Solutions:**
- Validate against research (may differ)
- Adjust model expectations
- Document differences
- May need more data

### 5. Privacy & Ethics

**Challenges:**
- Athlete privacy
- Data anonymization
- Consent requirements
- IRB approval (if research)

**Solutions:**
- Anonymize data
- Get proper consent
- Follow privacy regulations
- Consider IRB if needed

---

## Difficulty Assessment by Component

| Component | Difficulty | Time | Notes |
|-----------|-----------|------|-------|
| **Data Collection** | ⭐⭐⭐ High | 1-2 weeks | API setup, surveys, consent |
| **Data Loading** | ⭐ Easy | 2-3 days | Schema mapping, API calls |
| **Schema Adaptation** | ⭐⭐ Medium | 3-5 days | Unit conversion, aggregation |
| **Feature Engineering** | ⭐ Easy | 1-2 days | Mostly works as-is |
| **Injury Labels** | ⭐⭐⭐⭐ Very High | 2-4 weeks | Biggest challenge |
| **Data Validation** | ⭐⭐ Medium | 3-5 days | Quality checks, cleaning |
| **Model Retraining** | ⭐⭐ Medium | 3-5 days | May need tuning |
| **Testing** | ⭐⭐ Medium | 3-5 days | Validate everything works |

**Total Estimated Time:** 4-8 weeks (depending on data source and injury collection method)

---

## Recommended Approach

### Option A: Hybrid Approach (Easiest)

**Keep synthetic data, add real data gradually:**

1. Start with synthetic data (current state)
2. Collect small amount of real data (10-20 athletes)
3. Validate real data works with existing pipeline
4. Gradually increase real data
5. Eventually replace synthetic entirely

**Benefits:**
- Lower risk
- Can validate approach works
- Gradual transition
- Can compare synthetic vs real

### Option B: Strava API + Survey (Recommended)

**Use Strava for training data, survey for injuries:**

1. Set up Strava API access
2. Collect training data from volunteers
3. Send survey for injury history
4. Match training data with injury data
5. Use existing pipeline

**Benefits:**
- Good quality training data
- Can get injury data
- Scalable
- Realistic

### Option C: Public Dataset (If Available)

**Use existing public dataset:**

1. Find public sports/injury dataset
2. Adapt to our schema
3. Use existing pipeline
4. Minimal changes needed

**Benefits:**
- Fastest option
- Already collected
- May include injuries
- No collection effort

---

## Interview Answer

**Question:** "Could you replace the synthetic data with real-world data? How difficult would that be?"

**Answer:**
"Yes, absolutely. The architecture is designed to make this transition feasible. Here's the difficulty breakdown:

**Easy parts (1-2 weeks):**
- Data loading: Just need to create adapters to convert real data (e.g., from Strava API) to our schema
- Feature engineering: The functions are data-agnostic - they'll work with any data that matches the schema
- Model training: The pipeline doesn't care where data comes from

**Medium difficulty (1-2 weeks):**
- Schema adaptation: Need to handle unit conversions (km vs miles), different time granularities, missing data
- Data validation: Real data may have quality issues, outliers, different distributions than synthetic

**Hard part (2-4 weeks):**
- Injury data collection: This is the biggest challenge. Training data is available (Strava API), but injury labels require separate collection through surveys, medical records, or partnerships. This involves privacy, consent, and data collection logistics.

**Overall difficulty: Medium to High, estimated 4-8 weeks**

The good news is that the codebase is modular - the feature engineering and model training code should work with minimal changes. The main effort would be:
1. Setting up data collection (Strava API + injury survey)
2. Creating data adapters to convert to our schema
3. Data cleaning and validation
4. Retraining models on real data

I designed the system with this transition in mind - the feature engineering functions are data-agnostic, so as long as the input schema matches, they'll work with real data too."

---

## Summary

**Feasibility:** ✅ Yes, definitely feasible

**Overall Difficulty:** ⭐⭐⭐ Medium to High (4-8 weeks)

**Main Challenges:**
1. Injury data collection (hardest part)
2. Data quality and cleaning
3. Schema adaptation
4. Privacy/consent requirements

**Easy Parts:**
1. Feature engineering (works as-is)
2. Model training (minimal changes)
3. Data loading (straightforward adaptation)

**Recommendation:** Start with a hybrid approach - keep synthetic data while gradually collecting real data to validate the approach works, then transition fully once you have sufficient real data.
