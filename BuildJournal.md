# Build Journal - Documentation Guidelines

## Overview

This Build Journal serves as a daily log of development progress, capturing key technical decisions, implementations, and learnings from each day's work on the Injury Risk Predictor project.

## File Structure

### Daily Files

- **Format:** Create a new markdown file for each day using the format: `DDMMMYY.md` (e.g., `12JAN26.md`)
- **Location:** All daily journal files should be stored in the `journal/` directory
- **Naming Convention:** Use uppercase 3-letter month abbreviation (JAN, FEB, MAR, etc.) and 2-digit year

### Example Structure
```
journal/
├── 12JAN26.md
├── 13JAN26.md
├── 14JAN26.md
└── ...
```

## Daily Journal Entry Format

Each daily file should follow this structure:

```markdown
# Build Journal - [Date]

## Date
[Full date, e.g., January 12, 2026]

## Summary
[Brief 2-3 sentence overview of what was accomplished today]

---

## Commits & Pushes

### Commit #[Number]: [Short Descriptive Title]
**Time:** [HH:MM AM/PM PST]
**Hash:** [Git commit hash]

#### What Was Done
- [Brief bullet points of changes made]

#### Key Takeaways
- [Technical insight or learning from this commit]

#### Interview Explanation
**Question:** "Can you explain [feature/implementation] from your Injury Risk Predictor project?"

**Answer:** 
[Write a clear, concise explanation suitable for a technical interview. Include:
- What problem it solves
- How it works (high-level)
- Why this approach was chosen
- Any trade-offs or considerations]

---

### Commit #[Number]: [Next Commit Title]
[Repeat structure for each commit/push]
```

## Guidelines for Writing Entries

### 1. Commit Documentation
- Document **each commit and push** separately
- Keep commits small and focused (as per project guidelines)
- Include the commit hash for reference
- Note the time of each push

### 2. Key Takeaways
- Focus on **technical insights** and **learnings**
- What did you discover or learn during this implementation?
- What challenges did you overcome?
- What would you do differently next time?

### 3. Interview Explanations
- Write explanations as if answering a **technical interview question**
- Be concise but complete (aim for 2-3 minutes of speaking time)
- Include:
  - **Context:** What problem were you solving?
  - **Approach:** How did you solve it?
  - **Rationale:** Why this approach?
  - **Outcomes:** What were the results?
  - **Trade-offs:** What were the limitations or alternatives considered?

### 4. Technical Depth
- Balance between high-level concepts and specific implementation details
- Assume the interviewer has technical knowledge but may not know your specific domain
- Use code snippets or diagrams when helpful (but keep them brief)

## Example Entry

```markdown
# Build Journal - January 12, 2026

## Date
January 12, 2026

## Summary
Set up the project structure, initialized the FastAPI backend, and implemented the core ACWR calculation feature. Created synthetic data generation script to produce realistic training datasets.

---

## Commits & Pushes

### Commit #1: Initialize FastAPI Backend Structure
**Time:** 10:30 AM PST
**Hash:** a1b2c3d4e5f6

#### What Was Done
- Created `backend/` directory structure
- Set up FastAPI application with basic health check endpoint
- Configured CORS middleware for frontend integration
- Added requirements.txt with initial dependencies

#### Key Takeaways
- FastAPI's automatic OpenAPI documentation is incredibly useful for API development
- Setting up CORS early prevents integration headaches later
- Using Pydantic models for request validation catches errors before they reach business logic

#### Interview Explanation
**Question:** "How did you structure your FastAPI backend and why?"

**Answer:** 
"I structured the backend using a modular approach with separate directories for routes, ML logic, and models. I used FastAPI because it provides automatic API documentation, type validation through Pydantic, and excellent async support. The main application file sets up CORS middleware early to enable frontend communication, and I organized routes into separate modules to keep the codebase maintainable. I also used Pydantic models for request validation, which catches invalid data before it reaches the prediction logic, improving both security and user experience."

---

### Commit #2: Implement ACWR Calculation Feature
**Time:** 2:15 PM PST
**Hash:** f6e5d4c3b2a1

#### What Was Done
- Implemented `calculate_acwr()` function in `src/ml/features.py`
- Added rolling window calculations for acute (7-day) and chronic (28-day) loads
- Created unit tests to validate ACWR calculations match research thresholds
- Handled edge cases (division by zero, insufficient data)

#### Key Takeaways
- Rolling window calculations require careful handling of data boundaries
- The ACWR formula is simple but requires at least 28 days of data for accurate chronic load
- Testing against known research values (e.g., ACWR > 1.5 = high risk) validates correctness

#### Interview Explanation
**Question:** "Can you explain how you calculate the Acute:Chronic Workload Ratio?"

**Answer:**
"The ACWR is a key metric from sports science research that predicts injury risk. I calculate it by dividing the acute load (sum of training volume over the last 7 days) by the chronic load (average training volume over the last 28 days). The chronic load represents an athlete's fitness baseline, while acute load shows recent training stress. When acute load spikes relative to chronic load, injury risk increases. I implemented this using pandas rolling windows - a 7-day rolling sum for acute and a 28-day rolling mean for chronic. I also added validation to ensure we have sufficient data (at least 28 days) and handle edge cases like division by zero. The implementation matches research thresholds where ACWR > 1.5 indicates high injury risk."
```

## Best Practices

1. **Write entries immediately after each push** - Don't wait until the end of the day
2. **Be honest about challenges** - Document what was difficult and how you solved it
3. **Connect to the bigger picture** - Explain how each commit fits into the overall project
4. **Use consistent terminology** - Match the language used in DEVELOPMENT.md
5. **Keep it concise** - Aim for 3-5 sentences per section, but be thorough
6. **Update regularly** - Don't let entries pile up; document as you go

## Review & Reflection

At the end of each week, consider adding a brief reflection:
- What was the biggest technical challenge this week?
- What would you do differently if starting over?
- What are you most proud of accomplishing?

---

## Notes

- All times should be in **PST (Pacific Standard Time)**
- Use **24-hour format** or **12-hour format with AM/PM** (be consistent)
- Include **commit hashes** for easy reference back to code
- Keep explanations **interview-ready** - practice explaining them out loud
