# Injury Risk Predictor - Development Roadmap

## Project Overview

**Goal:** Build a web application that predicts athlete injury risk based on training load patterns using sports science research principles.

**Core Concept:** The acute:chronic workload ratio (ACWR) - when athletes increase training volume too quickly relative to what they're adapted to, injury risk increases significantly.

**Target Users:** Runners, cyclists, CrossFit athletes, any endurance/strength athletes tracking training volume

**Tech Stack:**
- **Backend ML:** Python 3.10+, scikit-learn, pandas, numpy
- **API:** FastAPI
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Deployment:** Vercel (frontend) + Railway/Render (API)
- **Storage:** PostgreSQL (optional) or JSON files for MVP

**Timeline:** 10-14 days for production-ready portfolio piece

---

## Scientific Foundation

### Key Research Papers to Reference:

1. **Gabbett, T.J. (2016).** "The training-injury prevention paradox: should athletes be training smarter and harder?" *British Journal of Sports Medicine*
   - Establishes ACWR as injury predictor
   - Sweet spot: ACWR between 0.8-1.3

2. **Hulin, B.T. et al. (2014).** "Spikes in acute workload are associated with increased injury risk in elite cricket fast bowlers" *British Journal of Sports Medicine*
   - Week-to-week spikes >10% increase injury risk

3. **Soligard, T. et al. (2016).** "How much is too much? (Part 1) International Olympic Committee consensus statement on load in sport and risk of injury" *British Journal of Sports Medicine*
   - Comprehensive framework for load monitoring

### Core Metrics We'll Implement:

**1. Acute:Chronic Workload Ratio (ACWR)**
- Acute Load = Last 7 days of training
- Chronic Load = Last 28 days average (rolling)
- ACWR = Acute / Chronic
- Risk zones:
  - < 0.8: Undertrained (detraining risk)
  - 0.8-1.3: Sweet spot (low risk)
  - 1.3-1.5: Moderate risk
  - > 1.5: High risk (2-4x injury likelihood)

**2. Training Monotony**
- Monotony = Mean weekly load / Standard Deviation
- High monotony (>2.0) = same load every day = injury risk

**3. Training Strain**
- Strain = Total Load × Monotony
- Captures both volume and variation

**4. Week-over-Week Change**
- Sudden spikes (>10-15%) = red flag

---

## Phase 0: Research & Planning

**Objective:** Understand the domain and define exact scope

### Tasks:
- [ ] Read the 3 core research papers (at least abstracts + conclusions)
- [ ] Understand ACWR calculation methodology
- [ ] Define what "training load" means for different sports
  - Running: weekly mileage, time, or TSS (Training Stress Score)
  - Cycling: TSS or hours
  - Strength training: volume load (sets × reps × weight)
- [ ] Decide on units for MVP: **Running miles/week** (simplest, most universal)
- [ ] Sketch out user flow on paper
- [ ] List all features to engineer

**Success Criteria:**
- Can explain ACWR to a non-technical person
- Have clear data requirements documented
- Know exactly what ML problem we're solving (binary classification: high risk vs low risk)

**Deliverables:**
- `docs/RESEARCH.md` - summary of papers and key findings
- `docs/FEATURES.md` - list of features to engineer
- `docs/USER_FLOW.md` - wireframe/flow diagram

---

## Phase 1: Data Strategy & Generation

**Objective:** Create a realistic training dataset with injury labels

### Option A: Synthetic Data (Recommended for MVP)

Generate realistic training logs based on research parameters:

**Tasks:**
- [ ] Create synthetic data generator script
  - `scripts/generate_training_data.py`
  - Simulate 100-200 athletes over 24 weeks
  - Each athlete has: age, experience level, baseline fitness
  - Weekly load follows realistic patterns (builds, plateaus, tapers, spikes)
- [ ] Inject injury risk scenarios
  - 30% of athletes: safe progressive loading (no injury)
  - 40% of athletes: moderate spikes (some injuries)
  - 30% of athletes: aggressive spikes (high injury rate)
- [ ] Label injury events
  - If ACWR > 1.5 for 2+ weeks: 60% chance of injury
  - If week-over-week spike > 20%: 40% chance of injury
  - If both conditions: 80% chance of injury
- [ ] Add realistic noise (missed days, weather, life events)
- [ ] Validate data distributions match research
  - Plot ACWR distributions
  - Check injury rates align with literature (15-30% per season)

**Synthetic Data Schema:**
```python
{
  "athlete_id": "ATH001",
  "week": 12,
  "weekly_load": 35.0,  # miles
  "daily_loads": [7, 8, 0, 6, 7, 7, 0],  # miles per day
  "acute_load": 35.0,
  "chronic_load": 32.5,
  "acwr": 1.08,
  "monotony": 1.5,
  "strain": 52.5,
  "week_over_week_change": 0.15,  # 15% increase
  "injured": false,
  "injury_type": null,
  "athlete_meta": {
    "age": 32,
    "experience_years": 5,
    "baseline_weekly_miles": 30
  }
}
```

### Option B: Real Data (Stretch Goal)

- [ ] Use Strava API to pull anonymized training data
- [ ] Create survey for injury history
- [ ] Match training patterns with injury events

**For MVP: Use synthetic data. It's faster, controllable, and you can cite the parameters from research.**

**Success Criteria:**
- 100+ athlete profiles with 24 weeks each = 2400+ data points
- Injury rate 15-25% (realistic)
- ACWR distribution matches research
- Clear relationship between high ACWR and injuries visible in EDA

**Key Files to Create:**
- `scripts/generate_training_data.py`
- `data/training_logs.csv`
- `data/athlete_metadata.csv`
- `notebooks/01_data_generation.ipynb`

---

## Phase 2: Exploratory Data Analysis

**Objective:** Understand the data and validate synthetic generation

### Tasks:
- [ ] Create Jupyter notebook for EDA
  - `notebooks/02_exploratory_analysis.ipynb`
- [ ] Load and inspect data
  - Check for missing values
  - Verify data types
  - Summary statistics
- [ ] Visualize training load patterns
  - Plot weekly load over time for sample athletes
  - Histogram of ACWR values
  - Distribution of injuries by ACWR zone
- [ ] Correlation analysis
  - ACWR vs injury rate
  - Monotony vs injury rate
  - Week-over-week change vs injury rate
- [ ] Create key visualizations for portfolio
  - ACWR zones with injury rates (bar chart)
  - Time series of athlete who got injured (annotate spike)
  - Correlation heatmap
- [ ] Statistical tests
  - T-test: injured vs non-injured ACWR means
  - Chi-square: injury rate by ACWR zone
- [ ] Document insights
  - What patterns emerge?
  - Which features seem most predictive?

**Success Criteria:**
- Can clearly see that high ACWR correlates with injury
- Have 5-7 publication-quality visualizations
- Documented insights in markdown cells
- Ready to engineer features

**Key Visualizations to Create:**
1. ACWR distribution by injury status
2. Injury rate by ACWR zone (confirm <0.8, 0.8-1.3, 1.3-1.5, >1.5)
3. Weekly load progression for injured vs non-injured athletes
4. Correlation matrix of all features
5. ROC curve preview (if you manually threshold ACWR)

---

## Phase 3: Feature Engineering

**Objective:** Create predictive features from raw training data

### Tasks:
- [ ] Create feature engineering pipeline
  - `src/ml/features.py`
- [ ] Implement time-based features
  ```python
  def calculate_acwr(df, athlete_id, week):
      acute = df.last_7_days_load
      chronic = df.last_28_days_avg_load
      return acute / chronic if chronic > 0 else 0
  ```
- [ ] Rolling window calculations
  - 7-day rolling sum (acute load)
  - 28-day rolling mean (chronic load)
  - 7-day rolling std (for monotony)
- [ ] Derived features
  - Week-over-week percentage change
  - 2-week ACWR trend (increasing/stable/decreasing)
  - Consecutive weeks above threshold
  - Distance from personal baseline
- [ ] Athlete-specific features
  - Age group (binned)
  - Experience level (novice/intermediate/advanced)
  - Baseline fitness (percentile)
- [ ] Lag features
  - Previous week's ACWR
  - 2 weeks ago ACWR
  - Recent injury history (binary: injured in last 8 weeks?)
- [ ] Interaction features (advanced)
  - ACWR × Age
  - ACWR × Experience
  - Strain × Experience

**Feature List (Final):**
1. `acute_load` - Last 7 days total
2. `chronic_load` - Last 28 days average
3. `acwr` - Acute / Chronic ratio
4. `monotony` - Mean / Std Dev of weekly loads
5. `strain` - Load × Monotony
6. `week_over_week_change` - % change from previous week
7. `acwr_trend` - 2-week slope of ACWR
8. `weeks_above_threshold` - Consecutive weeks ACWR > 1.3
9. `distance_from_baseline` - Current vs typical load
10. `age_group` - Binned age
11. `experience_level` - Years of training
12. `previous_week_acwr` - Lag feature
13. `recent_injury` - Binary: injured in last 8 weeks

**Success Criteria:**
- All features calculated correctly (unit tests)
- No data leakage (only use past data to predict future)
- Features normalized/scaled appropriately
- Missing values handled (forward fill for rolling windows)

**Key Files to Create:**
- `src/ml/features.py`
- `src/ml/preprocessing.py`
- `tests/test_features.py`
- `notebooks/03_feature_engineering.ipynb`

---

## Phase 4: Model Development

**Objective:** Train and evaluate injury risk prediction models

### Tasks:

#### 4.1: Data Splitting
- [ ] Create train/validation/test split
  - Train: 60% (weeks 1-14)
  - Validation: 20% (weeks 15-19)
  - Test: 20% (weeks 20-24)
  - **Important:** Split by time, not randomly (avoid data leakage)
- [ ] Ensure class balance
  - Check injury rate in each split
  - If imbalanced, use stratification

#### 4.2: Baseline Model
- [ ] Rule-based baseline (no ML)
  ```python
  def predict_injury_risk(acwr):
      if acwr > 1.5:
          return "HIGH_RISK"
      elif acwr > 1.3:
          return "MODERATE_RISK"
      else:
          return "LOW_RISK"
  ```
- [ ] Evaluate baseline accuracy
  - Establish lower bound to beat

#### 4.3: Model Training Pipeline
- [ ] Set up ML pipeline
  - `src/ml/train.py`
  - Preprocessing → Model → Evaluation
- [ ] Train Logistic Regression (simple, interpretable)
  ```python
  from sklearn.linear_model import LogisticRegression
  
  model = LogisticRegression(
      class_weight='balanced',  # handle imbalance
      max_iter=1000
  )
  ```
- [ ] Train Random Forest
  ```python
  from sklearn.ensemble import RandomForestClassifier
  
  model = RandomForestClassifier(
      n_estimators=100,
      max_depth=10,
      min_samples_split=20,
      class_weight='balanced',
      random_state=42
  )
  ```
- [ ] Train XGBoost
  ```python
  from xgboost import XGBClassifier
  
  model = XGBClassifier(
      n_estimators=100,
      max_depth=6,
      learning_rate=0.1,
      scale_pos_weight=3,  # handle imbalance
      random_state=42
  )
  ```

#### 4.4: Hyperparameter Tuning
- [ ] Use GridSearchCV or RandomizedSearchCV
- [ ] Tune on validation set
- [ ] Parameters to tune:
  - Random Forest: `n_estimators`, `max_depth`, `min_samples_split`
  - XGBoost: `learning_rate`, `max_depth`, `n_estimators`

#### 4.5: Model Evaluation
- [ ] Metrics to calculate:
  - Accuracy (baseline metric)
  - Precision (avoid false alarms)
  - Recall (catch actual injuries)
  - F1-Score (balance)
  - ROC-AUC (overall discrimination)
  - Confusion Matrix
- [ ] **Important:** Optimize for recall (better to over-predict injury risk than miss one)
- [ ] Feature importance analysis
  - Which features matter most?
  - Validate they align with research (ACWR should be top)
- [ ] Learning curves
  - Check for overfitting/underfitting

#### 4.6: Model Comparison
- [ ] Create comparison table
  ```
  Model               Accuracy  Precision  Recall  F1    ROC-AUC
  Baseline (Rules)    0.72      0.68       0.45    0.54  0.65
  Logistic Regression 0.78      0.74       0.71    0.72  0.81
  Random Forest       0.83      0.79       0.82    0.80  0.87
  XGBoost             0.85      0.81       0.84    0.82  0.89
  ```
- [ ] Select best model (likely Random Forest or XGBoost)
- [ ] Document why you chose it

**Success Criteria:**
- Beat baseline by 10%+ accuracy
- Recall > 0.75 (catch most injuries)
- ROC-AUC > 0.85
- Feature importance makes domain sense
- No overfitting (train vs val performance similar)

**Key Files to Create:**
- `src/ml/train.py`
- `src/ml/evaluate.py`
- `src/ml/models.py`
- `notebooks/04_model_training.ipynb`
- `models/injury_risk_model.pkl` (saved model)
- `models/scaler.pkl` (saved preprocessing)

---

## Phase 5: Model Interpretation & Validation

**Objective:** Understand what the model learned and validate against research

### Tasks:
- [ ] Feature importance visualization
  - Plot top 10 features
  - Verify ACWR, strain, week-over-week change are top features
- [ ] SHAP values (advanced explainability)
  ```python
  import shap
  explainer = shap.TreeExplainer(model)
  shap_values = explainer.shap_values(X_test)
  shap.summary_plot(shap_values, X_test)
  ```
- [ ] Partial dependence plots
  - How does injury risk change with ACWR?
  - Should match research: risk increases above 1.3
- [ ] Error analysis
  - Which cases does model get wrong?
  - Are there patterns in false negatives/positives?
- [ ] Validate against research
  - Does model predict higher risk at ACWR > 1.3? ✓
  - Does model penalize rapid load increases? ✓
  - Are experienced athletes more resilient? ✓
- [ ] Cross-validation
  - 5-fold time series cross-validation
  - Ensure model generalizes

**Success Criteria:**
- ACWR is #1 or #2 most important feature
- Model predictions align with sports science
- Can explain model decisions to non-technical users
- Feature importance matches domain expertise

**Key Files to Create:**
- `notebooks/05_model_interpretation.ipynb`
- `outputs/feature_importance.png`
- `outputs/shap_summary.png`
- `outputs/partial_dependence_plots.png`

---

## Phase 6: API Development

**Objective:** Create FastAPI backend to serve predictions

### Tasks:

#### 6.1: Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py (Pydantic schemas)
│   ├── ml/
│   │   ├── predictor.py
│   │   └── features.py
│   └── routers/
│       └── predictions.py
├── models/
│   ├── injury_risk_model.pkl
│   └── scaler.pkl
├── requirements.txt
└── Dockerfile
```

#### 6.2: Pydantic Models
- [ ] Create request/response schemas
  ```python
  # app/models.py
  from pydantic import BaseModel, Field
  from typing import List
  
  class TrainingWeek(BaseModel):
      week: int
      weekly_load: float = Field(..., gt=0)
      daily_loads: List[float]
  
  class AthleteProfile(BaseModel):
      age: int = Field(..., ge=18, le=100)
      experience_years: int = Field(..., ge=0)
      baseline_weekly_load: float
  
  class PredictionRequest(BaseModel):
      athlete: AthleteProfile
      training_history: List[TrainingWeek]
  
  class PredictionResponse(BaseModel):
      risk_level: str  # "LOW", "MODERATE", "HIGH"
      risk_score: float  # 0-1 probability
      acwr: float
      recommendations: List[str]
      feature_importance: dict
  ```

#### 6.3: Prediction Service
- [ ] Load saved model
  ```python
  # app/ml/predictor.py
  import pickle
  import pandas as pd
  from .features import calculate_features
  
  class InjuryPredictor:
      def __init__(self):
          with open('models/injury_risk_model.pkl', 'rb') as f:
              self.model = pickle.load(f)
          with open('models/scaler.pkl', 'rb') as f:
              self.scaler = pickle.load(f)
      
      def predict(self, training_data: dict) -> dict:
          # Calculate features
          features = calculate_features(training_data)
          
          # Scale features
          features_scaled = self.scaler.transform([features])
          
          # Predict
          risk_prob = self.model.predict_proba(features_scaled)[0][1]
          risk_level = self._get_risk_level(risk_prob)
          
          # Generate recommendations
          recommendations = self._generate_recommendations(
              features, risk_prob
          )
          
          return {
              "risk_level": risk_level,
              "risk_score": float(risk_prob),
              "acwr": features['acwr'],
              "recommendations": recommendations
          }
      
      def _get_risk_level(self, prob):
          if prob < 0.3:
              return "LOW"
          elif prob < 0.6:
              return "MODERATE"
          else:
              return "HIGH"
      
      def _generate_recommendations(self, features, risk_prob):
          recs = []
          
          if features['acwr'] > 1.3:
              recs.append("Reduce training volume by 10-20% this week")
          
          if features['monotony'] > 2.0:
              recs.append("Add more variety to your training")
          
          if features['week_over_week_change'] > 0.15:
              recs.append("You increased too quickly. Maintain current volume")
          
          if risk_prob < 0.3:
              recs.append("You're in the sweet spot! Keep up the good work")
          
          return recs
  ```

#### 6.4: API Endpoints
- [ ] Health check endpoint
  ```python
  @app.get("/health")
  def health_check():
      return {"status": "healthy"}
  ```
- [ ] Prediction endpoint
  ```python
  @app.post("/predict", response_model=PredictionResponse)
  def predict_injury_risk(request: PredictionRequest):
      predictor = InjuryPredictor()
      result = predictor.predict(request.dict())
      return result
  ```
- [ ] Batch prediction endpoint (optional)
- [ ] Model info endpoint
  ```python
  @app.get("/model/info")
  def model_info():
      return {
          "model_type": "Random Forest",
          "accuracy": 0.83,
          "features": ["acwr", "strain", "monotony", ...],
          "last_trained": "2024-01-15"
      }
  ```

#### 6.5: CORS & Middleware
- [ ] Enable CORS for frontend
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Restrict in production
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

#### 6.6: Testing
- [ ] Unit tests for feature calculation
- [ ] Integration tests for API endpoints
- [ ] Test with sample data

**Success Criteria:**
- API returns predictions in <100ms
- Handles edge cases (missing data, invalid input)
- Clear error messages
- Documentation with OpenAPI/Swagger

**Key Files to Create:**
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/ml/predictor.py`
- `backend/requirements.txt`
- `backend/tests/test_api.py`

---

## Phase 6.5: Early Backend Deployment

**Objective:** Deploy minimal API early to catch deployment issues before full integration

**Rationale:** Deploying early allows us to identify and fix deployment configuration issues (Docker, environment variables, platform-specific quirks) when the codebase is smaller and easier to debug.

### Tasks:

#### 6.5.1: Minimal Backend Setup
- [ ] Create `Dockerfile` for backend
  ```dockerfile
  FROM python:3.10-slim
  
  WORKDIR /app
  
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  COPY . .
  
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Create `.dockerignore` to exclude unnecessary files
- [ ] Test Docker build locally
  ```bash
  docker build -t injury-api .
  docker run -p 8000:8000 injury-api
  ```

#### 6.5.2: Deploy to Railway/Render
- [ ] Create account on Railway or Render
- [ ] Create new project/service
- [ ] Connect GitHub repository
- [ ] Configure build settings:
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Set environment variables (if needed)
  - `ENVIRONMENT=development`
- [ ] Deploy backend
- [ ] Verify deployment:
  - Health check endpoint works: `https://your-api.railway.app/health`
  - OpenAPI docs accessible: `https://your-api.railway.app/docs`
  - API responds correctly

#### 6.5.3: Fix Deployment Issues
- [ ] Document any platform-specific issues encountered
- [ ] Fix port configuration (Railway/Render may use `$PORT` env var)
- [ ] Fix file path issues (absolute vs relative paths)
- [ ] Fix dependency installation issues
- [ ] Test with sample API calls (use curl or Postman)

#### 6.5.4: Document Deployment Process
- [ ] Create `docs/DEPLOYMENT.md` with step-by-step instructions
- [ ] Document environment variables needed
- [ ] Note any gotchas or platform quirks
- [ ] Save API URL for later use

**Success Criteria:**
- Backend API is live and accessible
- Health check endpoint returns 200 OK
- OpenAPI documentation is accessible
- Can make test API calls successfully
- No deployment errors or crashes
- Docker build works locally

**Key Files to Create:**
- `backend/Dockerfile`
- `backend/.dockerignore`
- `docs/DEPLOYMENT.md` (backend section)

**Note:** At this stage, the API may not have the full ML model yet - that's okay. We're primarily testing that the deployment infrastructure works.

---

## Phase 7: Frontend Development

**Objective:** Build a beautiful, intuitive web interface

### Tasks:

#### 7.1: Project Setup
- [ ] Initialize Next.js project
  ```bash
  npx create-next-app@latest injury-risk-predictor --typescript --tailwind --app
  ```
- [ ] Install dependencies
  ```bash
  npm install recharts date-fns axios zod
  ```

#### 7.2: Page Structure
```
app/
├── page.tsx (landing/dashboard)
├── predict/
│   └── page.tsx (prediction form)
├── results/
│   └── page.tsx (prediction results)
├── history/
│   └── page.tsx (training log history)
└── about/
    └── page.tsx (explain the science)

components/
├── TrainingLogForm.tsx
├── RiskGauge.tsx
├── ACWRChart.tsx
├── RecommendationCard.tsx
└── MetricsOverview.tsx
```

#### 7.3: Key Components

**TrainingLogForm.tsx**
- [ ] Input weekly mileage for last 4-8 weeks
- [ ] Daily breakdown (optional)
- [ ] Athlete profile (age, experience)
- [ ] Validation with Zod
- [ ] Submit to API

**RiskGauge.tsx**
- [ ] Visual risk indicator (green/yellow/red)
- [ ] Animated needle/gauge
- [ ] Display risk percentage
- [ ] Color-coded zones

**ACWRChart.tsx**
- [ ] Line chart showing ACWR over time
- [ ] Horizontal lines for risk thresholds (0.8, 1.3, 1.5)
- [ ] Color-coded zones
- [ ] Annotations for injury risk periods
- [ ] Use Recharts

**RecommendationCard.tsx**
- [ ] Display actionable recommendations
- [ ] Icons for each recommendation type
- [ ] Severity indicators
- [ ] Expandable details

**MetricsOverview.tsx**
- [ ] Display key metrics in cards
  - Current ACWR
  - Training Strain
  - Monotony
  - Week-over-week change
- [ ] Trend indicators (↑↓→)

#### 7.4: Pages

**Landing/Dashboard (`app/page.tsx`)**
- [ ] Hero section explaining the app
- [ ] "Get Started" CTA button
- [ ] Quick stats (if user has data)
- [ ] Recent predictions
- [ ] Educational content ("What is ACWR?")

**Prediction Form (`app/predict/page.tsx`)**
- [ ] Multi-step form or single page
- [ ] Step 1: Athlete profile
- [ ] Step 2: Training history (last 4-8 weeks)
- [ ] Step 3: Review & submit
- [ ] Loading state during API call
- [ ] Error handling

**Results Page (`app/results/page.tsx`)**
- [ ] Risk gauge (prominent)
- [ ] Key metrics cards
- [ ] ACWR chart over time
- [ ] Recommendations list
- [ ] "What does this mean?" explanation
- [ ] Export report button (PDF)
- [ ] Share link

**Training History (`app/history/page.tsx`)**
- [ ] Table of logged training weeks
- [ ] Charts showing load progression
- [ ] Edit past entries
- [ ] Delete entries
- [ ] Export CSV

**About Page (`app/about/page.tsx`)**
- [ ] Explain the science
- [ ] Link to research papers
- [ ] FAQ section
- [ ] Model transparency (accuracy, limitations)
- [ ] Contact/feedback

#### 7.5: Styling & UX
- [ ] Consistent color scheme
  - Green: Low risk (#10B981)
  - Yellow: Moderate risk (#F59E0B)
  - Red: High risk (#EF4444)
- [ ] Responsive design (mobile-first)
- [ ] Loading skeletons
- [ ] Toast notifications for actions
- [ ] Dark mode (optional)
- [ ] Smooth animations (framer-motion)

#### 7.6: State Management
- [ ] Use React Context or Zustand for global state
- [ ] Store:
  - User profile
  - Training history
  - Past predictions
- [ ] LocalStorage persistence (optional)

**Success Criteria:**
- Clean, professional design
- Mobile responsive
- Fast page loads (<2s)
- Intuitive user flow
- Accessible (WCAG AA)
- No runtime errors

**Key Files to Create:**
- `app/page.tsx`
- `app/predict/page.tsx`
- `app/results/page.tsx`
- `components/TrainingLogForm.tsx`
- `components/RiskGauge.tsx`
- `components/ACWRChart.tsx`
- `lib/api.ts` (API client)

---

## Phase 7.5: Early Frontend Deployment

**Objective:** Deploy frontend early to catch Vercel/deployment issues before full integration

**Rationale:** Frontend deployment can have its own set of issues (build errors, environment variables, routing, static assets). Deploying early ensures we catch these when the codebase is manageable.

### Tasks:

#### 7.5.1: Frontend Build Configuration
- [ ] Verify Next.js build works locally
  ```bash
  npm run build
  npm run start
  ```
- [ ] Check for build warnings/errors
- [ ] Ensure all environment variables are prefixed with `NEXT_PUBLIC_` if needed client-side
- [ ] Create `.env.local` for local development (if needed)
- [ ] Add `.env.local` to `.gitignore`

#### 7.5.2: Deploy to Vercel
- [ ] Create Vercel account (if not already created)
- [ ] Install Vercel CLI (optional, can use web interface)
  ```bash
  npm i -g vercel
  ```
- [ ] Connect GitHub repository to Vercel
- [ ] Configure project settings:
  - Framework Preset: Next.js (auto-detected)
  - Root Directory: `frontend/` or `.` (depending on structure)
  - Build Command: `npm run build` (default)
  - Output Directory: `.next` (default)
- [ ] Set environment variables in Vercel dashboard:
  - `NEXT_PUBLIC_API_URL=https://your-api.railway.app` (from Phase 6.5)
- [ ] Deploy frontend
- [ ] Verify deployment:
  - Site is accessible
  - Pages load correctly
  - No runtime errors in browser console
  - Static assets load properly

#### 7.5.3: Fix Frontend Deployment Issues
- [ ] Fix any build errors (missing dependencies, TypeScript errors)
- [ ] Fix environment variable issues
- [ ] Fix routing issues (if using custom routes)
- [ ] Fix static asset paths (images, fonts, etc.)
- [ ] Test on different devices/browsers
- [ ] Check Vercel build logs for warnings

#### 7.5.4: Test Frontend-Backend Connection
- [ ] Update API client to use deployed backend URL
- [ ] Test API calls from deployed frontend
- [ ] Verify CORS is working correctly
- [ ] Test error handling (network errors, API errors)
- [ ] Document any CORS or connection issues

#### 7.5.5: Document Frontend Deployment
- [ ] Update `docs/DEPLOYMENT.md` with frontend deployment steps
- [ ] Document environment variables needed
- [ ] Note Vercel-specific configurations
- [ ] Save frontend URL for later use

**Success Criteria:**
- Frontend is live and accessible
- All pages load without errors
- Build completes successfully
- Environment variables are set correctly
- Frontend can connect to deployed backend API
- No console errors in browser
- Mobile responsive (basic check)

**Key Files to Create/Update:**
- `.env.local` (local development, gitignored)
- `.env.example` (template for environment variables)
- `docs/DEPLOYMENT.md` (frontend section)

**Note:** At this stage, the frontend may use mock data or a simplified API connection. The goal is to ensure the deployment pipeline works.

---

## Phase 8: Integration & Testing

**Objective:** Connect frontend to backend and test end-to-end

### Tasks:
- [ ] Create API client in frontend
  ```typescript
  // lib/api.ts
  import axios from 'axios';
  
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  export async function predictInjuryRisk(data: PredictionRequest) {
      const response = await axios.post(`${API_BASE_URL}/predict`, data);
      return response.data;
  }
  ```
- [ ] Handle API errors gracefully
  - Network errors
  - Validation errors
  - Server errors
- [ ] Loading states for async operations
- [ ] Test full user journey
  1. Enter training data
  2. Submit form
  3. View results
  4. See recommendations
  5. View history
- [ ] Test edge cases
  - No training history
  - Very high risk scenario
  - Very low risk scenario
  - Invalid inputs
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile testing (iOS, Android)
- [ ] Performance testing
  - Lighthouse score > 90
  - Fast API responses
- [ ] Accessibility testing
  - Screen reader compatibility
  - Keyboard navigation
  - Color contrast

**Success Criteria:**
- Complete user flow works without errors
- Error messages are helpful
- Loading states prevent confusion
- Works on all major browsers
- Mobile experience is smooth

---

## Phase 9: Full Integration Deployment

**Objective:** Deploy complete integrated application to production and verify end-to-end functionality

**Note:** Backend and frontend have already been deployed separately in Phases 6.5 and 7.5. This phase focuses on ensuring the full integrated application works correctly in production, updating configurations, and finalizing production settings.

### Tasks:

#### 9.1: Update Backend for Production
- [ ] Update `Dockerfile` if needed (should already exist from Phase 6.5)
- [ ] Update environment variables to production values
  - `ENVIRONMENT=production`
  - Any API keys or secrets
- [ ] Ensure model files are included in deployment
  - Verify `models/injury_risk_model.pkl` is in repository or deployment
  - Verify `models/scaler.pkl` is included
- [ ] Test full prediction endpoint with real model
  - Test `/predict` endpoint with sample data
  - Verify predictions are returned correctly
- [ ] Update CORS settings if needed (restrict origins in production)
- [ ] Verify backend is stable and handling requests correctly

#### 9.2: Update Frontend for Production
- [ ] Update environment variables in Vercel
  - `NEXT_PUBLIC_API_URL` should point to production backend
  - Set `NODE_ENV=production`
- [ ] Verify all API endpoints are correctly configured
- [ ] Test full user flow in production:
  - Submit prediction form
  - Receive results
  - View recommendations
- [ ] Check that all components render correctly
- [ ] Verify charts and visualizations work
- [ ] Test error handling in production environment

#### 9.3: Domain & SSL (Optional)
- [ ] Purchase domain (Namecheap, Google Domains)
- [ ] Point domain to Vercel
- [ ] SSL auto-configured by Vercel

#### 9.4: Monitoring
- [ ] Set up basic error tracking
  - Sentry (optional)
  - Vercel Analytics
- [ ] Monitor API performance
  - Railway/Render metrics
  - Response times
- [ ] Set up uptime monitoring (UptimeRobot)

**Success Criteria:**
- Full application is live and integrated
- Frontend successfully communicates with backend API
- All features work end-to-end in production
- API responses are fast (<200ms)
- No CORS issues between frontend and backend
- HTTPS enabled on both frontend and backend
- Mobile experience works correctly
- Error handling works in production
- Model predictions are accurate and returned correctly

**URLs to Document:**
- Production site: `https://injury-risk-predictor.vercel.app`
- API endpoint: `https://injury-api.railway.app`

---

## Phase 10: Portfolio Documentation

**Objective:** Create materials to showcase this project

### Tasks:

#### 10.1: GitHub README
- [ ] Create comprehensive README
  ```markdown
  # Injury Risk Predictor
  
  ## Overview
  AI-powered tool to predict athlete injury risk based on training load patterns, 
  built on sports science research.
  
  ## The Problem
  30-50% of training injuries are caused by rapid increases in training volume.
  
  ## The Solution
  Monitor acute:chronic workload ratio (ACWR) and predict injury risk before it happens.
  
  ## Key Features
  - Real-time injury risk prediction
  - Based on peer-reviewed sports science research
  - Actionable recommendations
  - Training load visualization
  
  ## Tech Stack
  - ML: Python, scikit-learn, XGBoost
  - Backend: FastAPI
  - Frontend: Next.js, TypeScript, Tailwind, Recharts
  - Deployment: Vercel + Railway
  
  ## Model Performance
  - Accuracy: 83%
  - Recall: 82% (catches most injury risks)
  - ROC-AUC: 0.87
  
  ## Research Foundation
  Based on:
  - Gabbett, T