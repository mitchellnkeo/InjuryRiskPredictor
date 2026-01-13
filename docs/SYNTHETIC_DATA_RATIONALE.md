# Synthetic Data Generation Rationale

## Why Synthetic Data?

**Question:** "Why did you generate synthetic data instead of using real athlete training data?"

**Answer:**
"I chose synthetic data generation for several strategic reasons:

1. **Speed & Control:** Collecting real athlete data would require months of data collection, IRB approval, athlete consent, and data cleaning. For an MVP portfolio project, synthetic data allows me to build and validate the model quickly while still being grounded in research.

2. **Research Grounding:** I can directly cite and implement parameters from peer-reviewed sports science research (Gabbett 2016, Hulin 2014, Soligard 2016). This ensures the data reflects real-world patterns that sports scientists have identified.

3. **Controllable Scenarios:** I can create specific injury scenarios (high ACWR, spikes, etc.) to ensure the model has sufficient examples of both injured and non-injured cases. Real data might be imbalanced or lack certain patterns.

4. **Reproducibility:** Synthetic data with a fixed random seed ensures anyone can reproduce the exact dataset, which is important for portfolio projects and interviews.

5. **Ethical Considerations:** No privacy concerns, no need for athlete consent, and I can be transparent about the data source.

The trade-off is that I need to validate the synthetic data matches research expectations, which I did through comprehensive EDA and statistical tests."

---

## Data Generation Parameters

### Why 150 Athletes × 24 Weeks?

**Question:** "How did you decide on 150 athletes and 24 weeks?"

**Answer:**
"These parameters were chosen to balance statistical power with computational efficiency:

1. **150 Athletes:**
   - Provides 3,600 data points (150 × 24 weeks), which is sufficient for machine learning
   - Allows for diverse athlete profiles (age, experience, training patterns)
   - Large enough to see statistical patterns, small enough to generate quickly
   - Research studies often use 50-200 athletes, so 150 is in the realistic range

2. **24 Weeks:**
   - Represents approximately half a year of training (6 months)
   - Long enough to see training progression, plateaus, and injury patterns
   - Allows for multiple training cycles (build, peak, recovery)
   - Typical training seasons are 20-30 weeks, so 24 is representative

3. **Total Data Points:**
   - 3,600 data points is sufficient for training ML models
   - With 15-25% injury rate, we get 540-900 injury cases, enough for the model to learn patterns
   - More data would be better, but this strikes a balance for MVP"

---

## Training Pattern Distribution (30/40/30)

**Question:** "Why did you split athletes into 30% safe, 40% moderate, and 30% aggressive training patterns?"

**Answer:**
"This distribution was designed to create a realistic mix of training behaviors that would produce a realistic injury rate:

1. **30% Safe Progressive Loading:**
   - Represents athletes who follow best practices (gradual 3-8% increases)
   - These athletes should have very low injury rates
   - Models real-world athletes who are injury-conscious or working with coaches

2. **40% Moderate Spikes:**
   - Represents typical athletes who occasionally push too hard
   - Occasional 10-20% week-over-week increases
   - This is probably the most common real-world scenario
   - Should produce moderate injury rates

3. **30% Aggressive Spikes:**
   - Represents athletes who frequently push too hard (15-30% spikes)
   - Could be competitive athletes, overzealous beginners, or those returning from injury
   - Should produce higher injury rates
   - Models the 'high-risk' population

**Why this split?**
- Creates a realistic distribution of injury risk levels
- Ensures we have enough examples of both safe and risky training patterns
- The 40% moderate group provides the bulk of 'normal' training data
- The 30/30 split on extremes ensures we have sufficient examples of both very safe and very risky patterns
- This distribution, combined with the injury probabilities, produces an overall injury rate of 15-25%, which matches research"

---

## Injury Risk Parameters

### ACWR Threshold: 1.5

**Question:** "Why did you use ACWR > 1.5 as the high-risk threshold?"

**Answer:**
"This comes directly from Gabbett's 2016 research, which established that ACWR > 1.5 indicates 2-4x increased injury likelihood. This is a well-established threshold in sports science literature. The research shows:
- ACWR 0.8-1.3: Sweet spot (lowest risk)
- ACWR 1.3-1.5: Moderate risk
- ACWR > 1.5: High risk (2-4x injury likelihood)

I used 1.5 as the threshold because it's the research-backed cutoff for 'high risk' that has been validated across multiple studies."

### Consecutive Weeks: 2+

**Question:** "Why require 2+ consecutive weeks of high ACWR for injury risk?"

**Answer:**
"This reflects the research finding that sustained high ACWR is more dangerous than a single spike. Gabbett's research shows that:
- A single week of high ACWR might not cause injury
- Sustained high ACWR (multiple weeks) significantly increases risk
- The body needs time to adapt, and repeated stress without adaptation leads to injury

I chose 2+ weeks because:
1. It matches the research emphasis on sustained high load
2. It's more realistic - one bad week might not cause injury, but 2+ weeks of high load is dangerous
3. It creates a more nuanced injury pattern (not just 'any spike = injury')"

### Week-over-Week Spike: 20%

**Question:** "Why 20% as the spike threshold?"

**Answer:**
"Hulin's 2014 research found that week-over-week spikes >10-15% increase injury risk. I used 20% as the threshold because:
1. It's above the research threshold (10-15%), making it a clear 'high spike'
2. It's a round number that's easy to explain
3. It represents a significant increase that would be noticeable and concerning
4. Combined with the 40% injury probability, it creates realistic injury patterns

The research shows that even 10-15% increases are risky, so 20% represents a more extreme spike that definitely increases injury risk."

### Injury Probabilities: 60%, 40%, 80%

**Question:** "How did you determine the injury probabilities (60% for high ACWR, 40% for spikes, 80% for both)?"

**Answer:**
"These probabilities were calibrated to produce a realistic overall injury rate (15-25%) while reflecting the relative risk levels:

1. **60% for ACWR > 1.5 for 2+ weeks:**
   - High ACWR is the primary risk factor (from Gabbett's research)
   - 60% reflects that sustained high ACWR is very dangerous, but not guaranteed to cause injury
   - Some athletes might be more resilient or lucky
   - This probability, combined with the frequency of high ACWR events, produces realistic injury rates

2. **40% for week-over-week spike > 20%:**
   - Spikes are a secondary risk factor (from Hulin's research)
   - 40% reflects that spikes are dangerous but less certain than sustained high ACWR
   - A single spike might not cause injury, but increases risk

3. **80% for both conditions:**
   - When both high ACWR AND a spike occur, the risk is very high
   - 80% reflects the compounding effect of multiple risk factors
   - Not 100% because some athletes might still avoid injury (resilience, luck, early intervention)

**Calibration Process:**
- I started with research-based relative risk levels (ACWR is primary, spikes are secondary)
- I tuned the probabilities through iteration to achieve 15-25% overall injury rate
- I validated that injured athletes have higher ACWR values than non-injured ones
- The final probabilities produce injury rates that match research literature"

---

## Athlete Profile Parameters

### Age Distribution: Mean 35, Std 8

**Question:** "Why this age distribution?"

**Answer:**
"Most recreational and competitive athletes are in their 20s-40s, with a peak around 30-35. The normal distribution centered at 35 with standard deviation of 8 creates:
- Most athletes between 27-43 (realistic range)
- Some younger athletes (18-26)
- Some masters athletes (44-65)
- This matches real-world athlete demographics"

### Experience: 0-25 years, correlated with age

**Question:** "Why correlate experience with age?"

**Answer:**
"This reflects reality - older athletes typically have more years of training experience. However, I added constraints:
- Experience can't exceed (age - 10), assuming athletes start training as teenagers/adults
- This prevents unrealistic combinations (e.g., 20-year-old with 25 years experience)
- Creates realistic athlete profiles"

### Baseline Weekly Miles: 15-60, correlated with experience

**Question:** "Why this baseline range?"

**Answer:**
"15-60 miles per week represents a realistic range for recreational to serious runners:
- Beginners: 15-25 miles/week
- Intermediate: 25-40 miles/week
- Advanced: 40-60+ miles/week

Correlating with experience makes sense - more experienced athletes typically train more. The formula `15 + (experience × 1.5)` creates this correlation while allowing for individual variation."

---

## Training Pattern Details

### Safe Pattern: 3-8% increases

**Question:** "Why 3-8% for safe progressive loading?"

**Answer:**
"Research recommends gradual increases of 5-10% per week for safe progression. I used 3-8% to be conservative:
- Below the 10% threshold that research identifies as risky
- Allows for natural variation
- Represents athletes following best practices
- Includes recovery weeks (10-20% decreases) to model periodization"

### Moderate Pattern: 10-20% spikes

**Question:** "Why 10-20% for moderate spikes?"

**Answer:**
"This range sits right at the research threshold (10-15% is risky):
- 10% is at the edge of what research says is safe
- 20% is clearly in the risky zone
- Represents athletes who occasionally push too hard
- More common than aggressive spikes (40% of athletes)"

### Aggressive Pattern: 15-30% spikes

**Question:** "Why 15-30% for aggressive spikes?"

**Answer:**
"This represents clearly dangerous training increases:
- Well above the 10-15% research threshold
- Models athletes who frequently push too hard
- Could represent competitive athletes, overzealous beginners, or those returning from injury
- Should produce higher injury rates"

---

## Validation & Calibration

**Question:** "How did you validate that the synthetic data is realistic?"

**Answer:**
"I validated the data through multiple checks:

1. **Injury Rate Validation:**
   - Target: 15-30% (from research literature)
   - Actual: 16.9% ✓
   - This confirms the probabilities are calibrated correctly

2. **ACWR Distribution Validation:**
   - Mean ACWR: 1.01 (within sweet spot 0.8-1.3) ✓
   - Injured athletes: Mean ACWR 1.60 (high risk zone) ✓
   - Non-injured athletes: Mean ACWR 0.88 (sweet spot) ✓
   - This confirms the relationship between ACWR and injury matches research

3. **Statistical Tests:**
   - T-test: Confirmed injured athletes have significantly higher ACWR (p < 0.05) ✓
   - Chi-square: Confirmed injury rates differ significantly across ACWR zones ✓
   - This provides quantitative validation, not just visual inspection

4. **Feature Relationships:**
   - High ACWR correlates with injuries ✓
   - Week-over-week spikes correlate with injuries ✓
   - Training patterns produce expected injury rates ✓

5. **Data Quality:**
   - No missing values ✓
   - Realistic distributions (age, experience, baseline load) ✓
   - Training patterns include realistic variation and noise ✓

This multi-faceted validation ensures the synthetic data captures the real-world patterns identified in sports science research."

---

## Key Design Decisions Summary

1. **Synthetic over Real:** Speed, control, research grounding, reproducibility
2. **150 athletes × 24 weeks:** Balance of statistical power and efficiency
3. **30/40/30 pattern split:** Realistic distribution of training behaviors
4. **ACWR > 1.5 threshold:** Directly from Gabbett's research
5. **2+ consecutive weeks:** Reflects research on sustained high load
6. **20% spike threshold:** Above research threshold (10-15%), clearly risky
7. **60/40/80 probabilities:** Calibrated to produce 15-25% injury rate
8. **Realistic athlete profiles:** Age, experience, baseline correlated realistically
9. **Validation:** Multiple checks ensure data matches research expectations

---

## Interview Answer (Concise Version)

**Question:** "Why did you generate synthetic data in this specific way?"

**Answer:**
"I designed the synthetic data generator to directly implement parameters from peer-reviewed sports science research. The key decisions were:

1. **Research-based thresholds:** ACWR > 1.5 (from Gabbett 2016), 20% week-over-week spikes (from Hulin 2014), 2+ consecutive weeks of high ACWR (sustained risk from research)

2. **Calibrated probabilities:** I set injury probabilities (60% for high ACWR, 40% for spikes, 80% for both) to produce an overall injury rate of 15-25%, which matches research literature. I validated this through EDA and statistical tests.

3. **Realistic distributions:** 150 athletes × 24 weeks provides sufficient data (3,600 points) while being computationally efficient. The 30/40/30 split of training patterns (safe/moderate/aggressive) creates a realistic mix that produces expected injury rates.

4. **Validation:** I confirmed the data matches research by checking injury rates (16.9%, within 15-30% range), ACWR distributions (injured athletes have mean ACWR 1.60 vs 0.88 for non-injured), and statistical significance (t-test, chi-square).

The synthetic approach allows me to cite research parameters directly, ensures sufficient examples of injury scenarios, and produces data that validates against research expectations. This is more transparent and reproducible than using real data, while still being grounded in peer-reviewed science."
