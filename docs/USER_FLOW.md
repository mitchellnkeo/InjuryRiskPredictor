# User Flow - Injury Risk Predictor

This document outlines the user journey through the Injury Risk Predictor application.

---

## High-Level User Flow

```
┌─────────────────┐
│   Landing Page   │
│  (Home/Dashboard)│
└────────┬─────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────────┐  ┌──────────────┐
│  Get Started    │  │  Learn More  │
│  (Predict Risk) │  │  (About Page)│
└────────┬────────┘  └──────────────┘
         │
         ▼
┌─────────────────┐
│ Prediction Form │
│  (Multi-step)   │
└────────┬────────┘
         │
         ├── Step 1: Athlete Profile
         │   - Age
         │   - Experience (years)
         │   - Baseline weekly load
         │
         ├── Step 2: Training History
         │   - Last 4-8 weeks of training
         │   - Weekly mileage
         │   - Daily breakdown (optional)
         │
         └── Step 3: Review & Submit
             - Review entered data
             - Submit to API
             - Loading state
         │
         ▼
┌─────────────────┐
│  Results Page   │
│  (Risk Report)  │
└────────┬────────┘
         │
         ├── Risk Gauge (visual indicator)
         ├── Key Metrics Cards
         ├── ACWR Chart (over time)
         ├── Recommendations
         └── "What does this mean?" explanation
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────────┐  ┌──────────────┐
│  Save to History│  │  Export PDF   │
│  (Optional)     │  │  (Optional)   │
└─────────────────┘  └──────────────┘
```

---

## Detailed User Flows

### Flow 1: First-Time User Journey

**Step 1: Landing Page**
- User arrives at homepage
- Sees hero section explaining the app
- Reads: "Predict your injury risk based on training load patterns"
- Clicks "Get Started" or "Predict Your Risk"

**Step 2: Prediction Form - Athlete Profile**
- Form asks for:
  - Age (number input, 18-100)
  - Years of training experience (number input, 0+)
  - Baseline weekly mileage (optional, can be auto-calculated)
- User fills in information
- Clicks "Next" or "Continue"

**Step 3: Prediction Form - Training History**
- Form asks for last 4-8 weeks of training:
  - Week 1: [__] miles
  - Week 2: [__] miles
  - Week 3: [__] miles
  - Week 4: [__] miles
  - (Optional: Expand to 8 weeks)
  - (Optional: Daily breakdown)
- User enters weekly mileage
- Validation: Ensures at least 4 weeks of data
- Clicks "Next" or "Calculate Risk"

**Step 4: Review & Submit**
- Shows summary of entered data
- User can go back to edit
- Clicks "Get My Risk Assessment"
- Loading spinner appears
- API call in progress

**Step 5: Results Page**
- Risk gauge displays prominently (green/yellow/red)
- Key metrics shown in cards:
  - Current ACWR: 1.44
  - Risk Level: MODERATE
  - Risk Score: 58%
- ACWR chart shows trend over time
- Recommendations list:
  - "Reduce training volume by 10-20% this week"
  - "You increased too quickly. Maintain current volume"
- "What does this mean?" expandable section
- Options to:
  - Save to history
  - Export as PDF
  - Start new prediction
  - Learn more about ACWR

---

### Flow 2: Returning User Journey

**Step 1: Landing Page (with history)**
- User sees dashboard with:
  - Recent predictions
  - Quick stats (average ACWR, risk trends)
  - "New Prediction" button
  - "View History" link

**Step 2: View History**
- Table/list of past predictions
- Shows date, risk level, ACWR
- Can click to view details
- Can edit/delete entries
- Can export as CSV

**Step 3: New Prediction**
- Similar to first-time flow
- May pre-fill athlete profile from previous entries
- User updates training history
- Gets new risk assessment

---

### Flow 3: Learning Journey

**Step 1: Landing Page**
- User clicks "Learn More" or "About"

**Step 2: About Page**
- Explains the science behind ACWR
- Links to research papers
- FAQ section
- Model transparency (accuracy, limitations)
- Contact/feedback form

**Step 3: Return to Prediction**
- User understands the concept
- Ready to try prediction

---

## Page Structure

### 1. Landing/Dashboard Page (`/`)

**Components:**
- Hero section with value proposition
- "Get Started" CTA button
- Quick explanation of ACWR (collapsible)
- Recent predictions (if logged in/has history)
- Quick stats cards (if has data)
- Footer with links to About, Contact

**User Actions:**
- Click "Get Started" → Go to prediction form
- Click "Learn More" → Go to about page
- Click "View History" → Go to history page
- Click on past prediction → View details

---

### 2. Prediction Form Page (`/predict`)

**Components:**
- Multi-step form wizard
- Progress indicator (Step 1 of 3)
- Form validation
- Error messages
- "Back" and "Next" buttons

**Steps:**

**Step 1: Athlete Profile**
- Age input (number, required)
- Experience years (number, required)
- Baseline weekly load (number, optional)
- Help text: "Your typical weekly training volume"

**Step 2: Training History**
- Week inputs (4-8 weeks)
- Add/remove week buttons
- Daily breakdown toggle (optional)
- Validation: At least 4 weeks required
- Help text: "Enter your weekly mileage for the last 4-8 weeks"

**Step 3: Review**
- Summary of entered data
- Edit buttons for each section
- Submit button: "Get My Risk Assessment"
- Loading state on submit

---

### 3. Results Page (`/results`)

**Components:**
- **Risk Gauge** (large, prominent)
  - Visual indicator (gauge/chart)
  - Color-coded (green/yellow/red)
  - Risk percentage displayed
  
- **Key Metrics Cards** (grid layout)
  - Current ACWR
  - Risk Level (LOW/MODERATE/HIGH)
  - Risk Score (0-100%)
  - Training Strain
  - Monotony
  - Week-over-week change

- **ACWR Chart** (line chart)
  - Shows ACWR over time
  - Horizontal lines for thresholds (0.8, 1.3, 1.5)
  - Color-coded zones
  - Annotations for risk periods

- **Recommendations Section**
  - List of actionable recommendations
  - Icons for each recommendation type
  - Severity indicators
  - Expandable details

- **Explanation Section** (collapsible)
  - "What does this mean?"
  - Explains ACWR in simple terms
  - Links to research

- **Action Buttons**
  - "Save to History"
  - "Export PDF"
  - "New Prediction"
  - "Learn More"

---

### 4. History Page (`/history`)

**Components:**
- Table/list of past predictions
- Columns: Date, ACWR, Risk Level, Actions
- Filter/search functionality
- Sort by date, risk level
- Charts showing trends over time
- Export CSV button

**User Actions:**
- View details (click row)
- Edit entry
- Delete entry
- Export all data

---

### 5. About Page (`/about`)

**Components:**
- Hero section: "The Science Behind Injury Risk Prediction"
- Explanation of ACWR
- Research papers section
- FAQ accordion
- Model transparency section:
  - Model accuracy
  - Limitations
  - Data privacy
- Contact/feedback form

---

## Error Handling Flows

### Error 1: Insufficient Data
- **Scenario:** User enters < 4 weeks of data
- **Flow:** 
  - Show validation error
  - Highlight missing weeks
  - Prevent form submission
  - Show help text: "At least 4 weeks of data required"

### Error 2: API Error
- **Scenario:** API call fails
- **Flow:**
  - Show error message
  - "Please try again" button
  - Option to go back and edit data
  - Contact support link

### Error 3: Invalid Input
- **Scenario:** User enters negative numbers or invalid data
- **Flow:**
  - Real-time validation
  - Show inline error messages
  - Prevent submission until fixed

---

## Mobile User Flow

**Adaptations for mobile:**
- Single column layout
- Larger touch targets
- Simplified navigation (hamburger menu)
- Stacked form inputs
- Full-screen modals for results
- Swipe gestures for multi-step forms

---

## User Personas

### Persona 1: Casual Runner
- **Goal:** Check if current training is safe
- **Flow:** Quick prediction → View results → Adjust training
- **Needs:** Simple interface, clear recommendations

### Persona 2: Serious Athlete
- **Goal:** Track ACWR over time, optimize training
- **Flow:** Regular predictions → History tracking → Trend analysis
- **Needs:** Detailed metrics, historical data, export functionality

### Persona 3: Coach/Trainer
- **Goal:** Monitor multiple athletes
- **Flow:** (Future feature) Dashboard for multiple athletes
- **Needs:** Bulk predictions, athlete management

---

## Success Metrics

**User Engagement:**
- % of users who complete prediction form
- % of users who view results
- % of users who return for new predictions

**User Satisfaction:**
- Time to complete prediction (< 2 minutes)
- Clarity of results (user understands risk level)
- Actionability of recommendations

**Technical:**
- Form submission success rate (> 95%)
- API response time (< 2 seconds)
- Error rate (< 5%)

---

## Wireframe Notes

**Key Design Principles:**
- **Clarity:** Risk level should be immediately obvious
- **Simplicity:** Minimal steps to get results
- **Education:** Help users understand ACWR without overwhelming
- **Actionability:** Clear recommendations, not just data

**Visual Hierarchy:**
1. Risk Gauge (most prominent)
2. Risk Level text
3. Key metrics
4. Chart
5. Recommendations
6. Additional info (collapsible)

**Color Coding:**
- Green (#10B981): Low risk (ACWR 0.8-1.3)
- Yellow (#F59E0B): Moderate risk (ACWR 1.3-1.5)
- Red (#EF4444): High risk (ACWR > 1.5)
- Gray: Undertrained (ACWR < 0.8)

---

## Future Enhancements

- **User Accounts:** Save history, track over time
- **Notifications:** Alert when ACWR is high
- **Training Plans:** Suggest optimal training progression
- **Social Sharing:** Share results (anonymized)
- **Mobile App:** Native iOS/Android app
- **Coach Dashboard:** Monitor multiple athletes
