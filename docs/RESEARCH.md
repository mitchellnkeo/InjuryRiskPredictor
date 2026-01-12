# Research Foundation - Injury Risk Predictor

## Overview

This document summarizes the sports science research that forms the foundation of the Injury Risk Predictor application. The core concept is the **Acute:Chronic Workload Ratio (ACWR)**, which has been validated in multiple peer-reviewed studies as a predictor of injury risk in athletes.

---

## Key Research Papers

### 1. Gabbett, T.J. (2016)
**Title:** "The training-injury prevention paradox: should athletes be training smarter and harder?"  
**Journal:** *British Journal of Sports Medicine*

#### Key Findings:
- **ACWR as Injury Predictor:** Established ACWR as a reliable predictor of injury risk
- **Sweet Spot:** ACWR between 0.8-1.3 represents the optimal training zone with lowest injury risk
- **Training Paradox:** Athletes who train more overall (higher chronic load) have lower injury rates, BUT sudden spikes in training (high acute load relative to chronic) increase injury risk
- **Risk Zones:**
  - ACWR < 0.8: Undertrained zone (detraining risk, but also injury risk from sudden increases)
  - ACWR 0.8-1.3: **Sweet spot** (optimal training zone, lowest injury risk)
  - ACWR 1.3-1.5: Moderate risk zone
  - ACWR > 1.5: High risk zone (2-4x increased injury likelihood)

#### Practical Implications:
- Gradual progressive overload is key to injury prevention
- Athletes should aim to maintain ACWR in the 0.8-1.3 range
- Sudden increases in training volume are dangerous, even for well-trained athletes

---

### 2. Hulin, B.T. et al. (2014)
**Title:** "Spikes in acute workload are associated with increased injury risk in elite cricket fast bowlers"  
**Journal:** *British Journal of Sports Medicine*

#### Key Findings:
- **Week-over-Week Spikes:** Sudden increases in training load (>10-15% week-over-week) significantly increase injury risk
- **Elite Athletes:** Even highly trained athletes are vulnerable to injury when training load spikes suddenly
- **Sport-Specific:** Study focused on cricket fast bowlers, but principles apply across sports
- **Timeframe:** Injuries often occur 1-2 weeks after a training load spike

#### Practical Implications:
- Monitor week-over-week changes in training load
- Limit increases to <10% per week when possible
- Be especially cautious after periods of reduced training (return from injury, off-season)

---

### 3. Soligard, T. et al. (2016)
**Title:** "How much is too much? (Part 1) International Olympic Committee consensus statement on load in sport and risk of injury"  
**Journal:** *British Journal of Sports Medicine*

#### Key Findings:
- **Comprehensive Framework:** Provides IOC consensus on load monitoring in sport
- **Multi-Factorial:** Injury risk is influenced by multiple factors beyond just volume:
  - Training intensity
  - Training frequency
  - Recovery time
  - Individual athlete factors (age, experience, injury history)
- **Individual Variation:** Different athletes respond differently to the same training load
- **Monitoring Recommendations:** Regular monitoring of training load is essential for injury prevention

#### Practical Implications:
- No one-size-fits-all approach - individualization is important
- Multiple metrics should be considered (not just ACWR)
- Regular monitoring and adjustment is key

---

## Core Metrics Implementation

### 1. Acute:Chronic Workload Ratio (ACWR)

**Definition:**
- **Acute Load:** Sum of training volume over the last 7 days
- **Chronic Load:** Average training volume over the last 28 days (rolling average)
- **ACWR = Acute Load / Chronic Load**

**Calculation Example:**
```
Week 1-4: 30, 32, 28, 35 miles
Chronic Load (28-day avg): (30+32+28+35) / 4 = 31.25 miles

Week 5: 45 miles (acute load)
ACWR = 45 / 31.25 = 1.44 (MODERATE RISK)
```

**Risk Zones:**
| ACWR Range | Risk Level | Interpretation |
|------------|-----------|----------------|
| < 0.8 | Low-Medium | Undertrained, but sudden increases are risky |
| 0.8 - 1.3 | **Low** | **Sweet spot - optimal training zone** |
| 1.3 - 1.5 | Moderate | Increased injury risk |
| > 1.5 | High | 2-4x increased injury likelihood |

**Why It Works:**
- Chronic load represents an athlete's fitness baseline (what they're adapted to)
- Acute load represents recent training stress
- When acute load spikes relative to chronic load, the athlete hasn't had time to adapt
- This mismatch between stress and adaptation leads to injury

---

### 2. Training Monotony

**Definition:**
- Monotony = Mean Weekly Load / Standard Deviation of Weekly Loads
- Measures how consistent/varied training is

**Interpretation:**
- **Low Monotony (< 1.5):** Varied training (good)
- **Moderate Monotony (1.5 - 2.0):** Some variation
- **High Monotony (> 2.0):** Very repetitive training (injury risk)

**Why It Matters:**
- Same load every day = high monotony = increased injury risk
- Variation in training helps prevent overuse injuries
- High monotony combined with high load = especially dangerous

**Example:**
```
Week 1: [7, 7, 7, 7, 7, 7, 0] miles
Mean: 6, Std Dev: 2.8
Monotony = 6 / 2.8 = 2.14 (HIGH - risky!)

Week 2: [10, 5, 8, 0, 12, 6, 0] miles
Mean: 5.9, Std Dev: 4.5
Monotony = 5.9 / 4.5 = 1.31 (LOW - good!)
```

---

### 3. Training Strain

**Definition:**
- Strain = Total Weekly Load × Monotony
- Captures both volume AND variation

**Interpretation:**
- High strain = high volume + high monotony = very high injury risk
- Even moderate volume can be dangerous if monotony is high

**Example:**
```
Week 1: 42 miles total, Monotony = 2.14
Strain = 42 × 2.14 = 89.9 (HIGH STRAIN - very risky!)

Week 2: 41 miles total, Monotony = 1.31
Strain = 41 × 1.31 = 53.7 (MODERATE STRAIN - safer)
```

---

### 4. Week-over-Week Change

**Definition:**
- Percentage change in weekly load from previous week
- Week-over-Week Change = (Current Week - Previous Week) / Previous Week × 100

**Risk Thresholds:**
- **< 10%:** Generally safe
- **10-15%:** Moderate risk
- **> 15%:** High risk (especially if sustained)

**Example:**
```
Week 1: 30 miles
Week 2: 40 miles
Change = (40 - 30) / 30 × 100 = 33.3% (HIGH RISK!)
```

---

## Training Load Units by Sport

For MVP, we'll focus on **running miles/week** as it's:
- Simple and universal
- Easy for users to track
- Well-studied in research

**Future Expansion:**
- **Cycling:** TSS (Training Stress Score) or hours/week
- **Strength Training:** Volume load (sets × reps × weight)
- **Swimming:** Yards/meters per week
- **CrossFit:** Total volume or workout intensity scores

---

## ML Problem Definition

**Problem Type:** Binary Classification
- **Target Variable:** Injury risk (HIGH RISK vs LOW/MODERATE RISK)
- **Features:** ACWR, monotony, strain, week-over-week change, athlete characteristics
- **Goal:** Predict if an athlete is at high risk of injury in the next 1-2 weeks

**Success Metrics:**
- **Recall > 75%:** Catch most actual injury risks (better to over-predict than miss)
- **Precision:** Balance between false alarms and missed injuries
- **ROC-AUC > 0.85:** Good overall discrimination

---

## Key Takeaways for Non-Technical Explanation

**What is ACWR?**
"Think of your body like a bank account. Your chronic load (last 4 weeks average) is like your savings - it shows how much training you're used to. Your acute load (last week) is like a withdrawal. If you suddenly withdraw way more than usual (high ACWR), you're in trouble. The sweet spot is when your weekly training is about 80-130% of what you've been doing on average - that's when you're building fitness safely without risking injury."

**Why does this matter?**
"30-50% of training injuries happen because athletes increase their training too quickly. By monitoring ACWR, athletes can see when they're pushing too hard and adjust before getting hurt."

---

## References

1. Gabbett, T.J. (2016). The training-injury prevention paradox: should athletes be training smarter and harder? *British Journal of Sports Medicine*, 50(5), 273-280.

2. Hulin, B.T., Gabbett, T.J., Lawson, D.W., Caputi, P., & Sampson, J.A. (2014). Spikes in acute workload are associated with increased injury risk in elite cricket fast bowlers. *British Journal of Sports Medicine*, 50(11), 709-714.

3. Soligard, T., Schwellnus, M., Alonso, J.M., Bahr, R., Clarsen, B., Dijkstra, H.P., ... & Engebretsen, L. (2016). How much is too much? (Part 1) International Olympic Committee consensus statement on load in sport and risk of injury. *British Journal of Sports Medicine*, 50(17), 1030-1041.
