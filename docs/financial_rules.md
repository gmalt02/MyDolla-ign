# Financial Rule Base

---

## 1. 50/30/20 Budget Rule

### Description
A budgeting heuristic that allocates:
- 50% of income → Needs
- 30% of income → Wants
- 20% of income → Savings or debt repayment

### Formula / Logic
- Needs % = (Needs / Income) × 100
- Wants % = (Wants / Income) × 100
- Savings % = (Savings / Income) × 100

**Flag Conditions:**
- Needs > 50%
- Wants > 30%
- Savings < 20%

### Example Application
Income: $4,000  
Needs: $2,400 → 60% (Above target)  
Savings: $400 → 10% (Below recommended)

Triggered Rules:
- Needs overspending
- Savings below benchmark

---

## 2. Savings Benchmarks

### Description
Savings health indicators:
- Minimum: 10%
- Recommended: 15–20%
- Strong: 20%+

### Formula
- Savings % = (Savings / Income) × 100

### Example
Income: $5,000  
Savings: $500 → 10% → Minimum level only

---

## 3. Emergency Fund Guideline

### Description
An emergency fund should cover 3–6 months of essential expenses.

### Logic
- Minimum Fund = Monthly Essential Expenses × 3
- Ideal Fund = Monthly Essential Expenses × 6

### Example
Essential expenses: $2,000  
Minimum target: $6,000  
Ideal target: $12,000

---

## 4. Overspending Threshold Detection

### Description
Spending imbalance detection rule.

### Logic
- Category % = (Category Spending / Income) × 100

**Flag If:**
- Housing > 35% of income
- Any non-housing category > 30% of income

### Example
Rent: $2,000  
Income: $4,000  
→ 50% → Overspending alert

---

## 5. Debt-to-Income Ratio (DTI)

### Description
Debt payments should not exceed 36% of income.

### Formula
- DTI = (Monthly Debt Payments / Income) × 100

**Flag If:**
- DTI > 36%

### Example
Debt: $1,800  
Income: $4,000  
DTI = 45% → High risk
