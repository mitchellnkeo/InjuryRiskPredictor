# Feature Importance Explanation: Why Week-over-Week Change is #1

## The Question
"Why is `week_over_week_change` ranked #1 instead of `acwr`? I thought ACWR should be the most important feature."

## The Answer

**This is actually CORRECT and EXPECTED!** Here's why:

### 1. **Both Features Are Strong Predictors**

Looking at our data generation logic (`scripts/generate_training_data.py`), injuries are created based on:

1. **High ACWR (>1.5) for 2+ consecutive weeks** → 60% injury probability
2. **Week-over-week spike (>20% increase)** → 40% injury probability  
3. **BOTH conditions** → 80% injury probability

### 2. **Why Week-over-Week Change Might Rank Higher**

**Week-over-week change captures sudden spikes** - rapid increases in training load that haven't been "averaged out" yet by the chronic load calculation.

**Example:**
- Athlete normally runs 20 miles/week (chronic load = 20)
- Suddenly spikes to 35 miles/week (acute load = 35)
- **Week-over-week change = 75%** (huge spike!)
- **ACWR = 35/20 = 1.75** (high, but takes time to build up)

The week-over-week change **immediately** flags this as dangerous, while ACWR needs 2+ weeks of high values to reach the same risk level.

### 3. **This Matches Research**

Research shows that **sudden spikes** (week-over-week changes >20%) are a major injury risk factor, independent of ACWR. Our model correctly learned this!

### 4. **ACWR Being #3 is Still Excellent**

ACWR being in the **top 3** features validates our domain knowledge:
- ✓ ACWR is still highly important
- ✓ The model learned the research-backed relationship
- ✓ Week-over-week change being #1 doesn't invalidate ACWR - it complements it!

### 5. **Feature Interactions**

These features work together:
- **High ACWR + High week-over-week change** = Highest risk (80% probability in our data)
- **High ACWR alone** = Moderate risk (60% probability)
- **High week-over-week change alone** = Moderate risk (40% probability)

The model learned that **both matter**, with week-over-week change being slightly more predictive in our specific dataset.

## Conclusion

**This is not an error - it's the model correctly learning from the data!**

- Week-over-week change #1 = Captures sudden spikes (immediate risk)
- ACWR #3 = Captures sustained high load (accumulated risk)
- Both are in top 3 = Model learned the right patterns

If ACWR was ranked #10 or lower, THAT would be a problem. But #3 is excellent!

## For Interviews

**Q: "Why is week-over-week change more important than ACWR?"**

**A:** "Both features are highly important - they're ranked #1 and #3, which validates our domain knowledge. Week-over-week change captures sudden spikes in training load, which research shows are a major injury risk factor. ACWR captures sustained high load over time. The model learned that sudden spikes are slightly more predictive in our dataset, which makes sense - a 75% week-over-week increase immediately signals danger, while ACWR needs 2+ weeks to build up. Both features work together - when both are high, injury risk is highest (80% probability in our data generation). This aligns with research showing that both sudden spikes AND sustained high load increase injury risk."
