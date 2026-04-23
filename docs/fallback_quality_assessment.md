# Fallback quality — AI vs deterministic (Sprint 3, Rene)

**Code:** `backend/app/services/ai_service.py` — `analyze_budget()` uses Gemini when `google-generativeai` (or Vertex) is configured and `GEMINI_API_KEY` / project env is set; otherwise `generate_fallback_response()` with `output_source: fallback_deterministic`.

**Deterministic runs:** Unset `GEMINI_API_KEY` (or leave it blank), clear `GOOGLE_CLOUD_PROJECT`, or run without the Gemini SDK — responses stay rule-based and reproducible.

**AI runs:** Set `GEMINI_API_KEY` in `backend/.env`, install `google-generativeai`, then run:

```bash
cd backend
python scripts/sprint3_capture_ai_column.py
```

Paste each printed JSON block into the matching **Google AI Studio** fence below (replace the placeholder). The script labels `output_source`; only captures with `google_ai_studio` count as the live model path.

**Reading the script output:** If every block shows `output_source: fallback_deterministic` and the terminal said **No Gemini SDK installed**, Python is not using the `google-generativeai` package in *this* environment (`pip install google-generativeai` inside your venv, then re-run). If the SDK is installed but the key is missing, you get the same fallback. In both cases the printed JSON **duplicates the deterministic column** in this doc — **do not** paste it into the AI side.

The **Deterministic** JSON below was produced with no Studio key (same inputs as the five-row plan).

---

## Five scenarios — side by side

### 1 — Balanced budget, positive remaining

**Inputs:** `monthly_income` 5000; expenses rent 1200, food 400, transportation 200, utilities 150, entertainment 200, savings 800, other 100 (total 3050, remaining 1950).

| Aspect | Deterministic | Google AI Studio |
|--------|---------------|------------------|
| **Tone** | Short, fixed template; generic closing line. | *(Paste capture — usually longer, more conversational.)* |
| **Specificity** | Same dollar figures in every narrative field. | *(Should still mirror calculated summary numbers from the prompt.)* |
| **Numeric grounding** | Strong: income, remaining, savings %, total expenses in tip. | *(Check FINANCIAL ADVICE / GROUNDED TIP cite summary values.)* |

**Deterministic (captured):**

```json
{
  "output_source": "fallback_deterministic",
  "financial_advice": "Based on your income of $5000.00 and expenses of $3050.00, you have $1950.00 left. You're saving 16.0%; building toward 20% can help long-term. Small steps add up—focus on one category to improve first.",
  "quiz_question": "Your documented savings line is $800.00 per month, which is 16.0% of your $5000.00 income. Per Savings Benchmarks in financial_rules.md, what is the recommended range for savings as a percentage of income?",
  "quiz_answer_key": "Strong answers note that you save 16.0% ($800.00 of $5000.00). Savings Benchmarks in financial_rules.md describe about 10% as a common minimum floor, roughly 15–20% as a healthy target, and 20%+ as strong.",
  "grounded_tip": "Per the Emergency Fund Guideline (financial_rules.md), aim for 3–6 months of essential expenses in accessible savings; your total expenses are $3050.00/month in this budget.",
  "grounded_rule_citation": "Emergency Fund Guideline"
}
```

**Google AI Studio (paste from `sprint3_capture_ai_column.py`):**

```json
{
  "output_source": "google_ai_studio",
  "_instructions": "Replace this object with script output when GEMINI_API_KEY is set."
}
```

---

### 2 — Expenses exceed income

**Inputs:** `monthly_income` 3000; expenses total 4200 (remaining −1200); rent 50% of income.

| Aspect | Deterministic | Google AI Studio |
|--------|---------------|------------------|
| **Tone** | Warning emoji + explicit deficit; housing called out. | |
| **Specificity** | Exact overspend amount; $0 savings line in quiz. | |
| **Numeric grounding** | Deficit, housing %, savings $ all explicit. | |

**Deterministic (captured):**

```json
{
  "output_source": "fallback_deterministic",
  "financial_advice": "Based on your income of $3000.00 and expenses of $4200.00, you have $-1200.00 left. ⚠️ Your expenses exceed income by $1200.00. Focus on reducing spending or increasing income before saving. Small steps add up—focus on one category to improve first.",
  "quiz_question": "Your documented savings line is $0.00 per month, which is 0.0% of your $3000.00 income. Per Savings Benchmarks in financial_rules.md, what is the recommended range for savings as a percentage of income?",
  "quiz_answer_key": "Strong answers note that you save 0.0% ($0.00 of $3000.00). Savings Benchmarks in financial_rules.md describe about 10% as a common minimum floor, roughly 15–20% as a healthy target, and 20%+ as strong.",
  "grounded_tip": "Housing is 50.0% of income; our financial_rules.md housing guideline suggests keeping housing near or below ~30% when possible—so this is a key area to revisit.",
  "grounded_rule_citation": "Housing ~30% guideline"
}
```

**Google AI Studio (paste from script):**

```json
{
  "output_source": "google_ai_studio",
  "_instructions": "Replace with script output."
}
```

---

### 3 — Zero income

**Inputs:** `monthly_income` 0; rent 800, food 200.

| Aspect | Deterministic | Google AI Studio |
|--------|---------------|------------------|
| **Tone** | Quiz explains why income is required for percentages. | |
| **Specificity** | No savings-rate quiz; pivot to data requirement. | |
| **Numeric grounding** | Grounded tip still uses total expenses ($1000/mo). | |

**Deterministic (captured):**

```json
{
  "output_source": "fallback_deterministic",
  "financial_advice": "Based on your income of $0.00 and expenses of $1000.00, you have $-1000.00 left. ⚠️ Your expenses exceed income by $1000.00. Focus on reducing spending or increasing income before saving. Small steps add up—focus on one category to improve first.",
  "quiz_question": "Why is entering a positive monthly income required before the tool can compute percentages like savings rate or housing share of income?",
  "quiz_answer_key": "Income is needed so the tool can divide savings (and other categories) by income to get percentages. Add your monthly take-home pay, then re-run Analyze.",
  "grounded_tip": "Per the Emergency Fund Guideline (financial_rules.md), aim for 3–6 months of essential expenses in accessible savings; your total expenses are $1000.00/month in this budget.",
  "grounded_rule_citation": "Emergency Fund Guideline"
}
```

**Google AI Studio (paste from script):**

```json
{
  "output_source": "google_ai_studio",
  "_instructions": "Replace with script output."
}
```

---

### 4 — Housing above ~30% of income

**Inputs:** `monthly_income` 4000; rent 1800 (45%); other lines sum to 3200 total.

| Aspect | Deterministic | Google AI Studio |
|--------|---------------|------------------|
| **Tone** | Housing paragraph + savings “toward 20%” nudge. | |
| **Specificity** | Grounded tip always housing rule when rent &gt; 30%. | |
| **Numeric grounding** | 45%, $4000, $400 savings in quiz. | |

**Deterministic (captured):**

```json
{
  "output_source": "fallback_deterministic",
  "financial_advice": "Based on your income of $4000.00 and expenses of $3200.00, you have $800.00 left. Housing is 45.0% of your income (often recommended under 30%). You're saving 10.0%; building toward 20% can help long-term. Small steps add up—focus on one category to improve first.",
  "quiz_question": "Your documented savings line is $400.00 per month, which is 10.0% of your $4000.00 income. Per Savings Benchmarks in financial_rules.md, what is the recommended range for savings as a percentage of income?",
  "quiz_answer_key": "Strong answers note that you save 10.0% ($400.00 of $4000.00). Savings Benchmarks in financial_rules.md describe about 10% as a common minimum floor, roughly 15–20% as a healthy target, and 20%+ as strong.",
  "grounded_tip": "Housing is 45.0% of income; our financial_rules.md housing guideline suggests keeping housing near or below ~30% when possible—so this is a key area to revisit.",
  "grounded_rule_citation": "Housing ~30% guideline"
}
```

**Google AI Studio (paste from script):**

```json
{
  "output_source": "google_ai_studio",
  "_instructions": "Replace with script output."
}
```

---

### 5 — One category dominates (savings line)

**Inputs:** `monthly_income` 6000; savings 3500 (58.3%); other lines smaller.

| Aspect | Deterministic | Google AI Studio |
|--------|---------------|------------------|
| **Tone** | Advice block is shorter (no “increase savings” line); quiz stresses high savings %. | |
| **Specificity** | 58.3% and $3500 called out in quiz and answer key. | |
| **Numeric grounding** | `breakdown` from code always matches payload (not repeated in this slim JSON). | |

**Deterministic (captured):**

```json
{
  "output_source": "fallback_deterministic",
  "financial_advice": "Based on your income of $6000.00 and expenses of $5200.00, you have $800.00 left. Small steps add up—focus on one category to improve first.",
  "quiz_question": "Your documented savings line is $3500.00 per month, which is 58.3% of your $6000.00 income. Per Savings Benchmarks in financial_rules.md, what is the recommended range for savings as a percentage of income?",
  "quiz_answer_key": "Strong answers note that you save 58.3% ($3500.00 of $6000.00). Savings Benchmarks in financial_rules.md describe about 10% as a common minimum floor, roughly 15–20% as a healthy target, and 20%+ as strong.",
  "grounded_tip": "Per the Emergency Fund Guideline (financial_rules.md), aim for 3–6 months of essential expenses in accessible savings; your total expenses are $5200.00/month in this budget.",
  "grounded_rule_citation": "Emergency Fund Guideline"
}
```

**Google AI Studio (paste from script):**

```json
{
  "output_source": "google_ai_studio",
  "_instructions": "Replace with script output."
}
```

---

## Guarantee

Category percentages and `breakdown` are always computed in Python (`parse_ai_response` / `generate_fallback_response`), not invented by the model.

Use `POST /api/analyze` and the `output_source` field in the JSON to tell which path ran.
