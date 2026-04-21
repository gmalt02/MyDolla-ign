# Final demo script — myDolla$ign

**Audience:** Course final presentation (Venture 5).  
**Target runtime:** About 5–6 minutes for the live product portion (overall slot is ~12 minutes with design + contributions + Q&A — see Sprint 3 plan).  
**Prep:** Stable network, `.env` with `GEMINI_API_KEY` for AI path; duplicate browser profile or terminal tab with API key unset for Scenario 3.

---

## Scenario 1 — Balanced budget, happy path (full 3-step flow)

**Purpose:** Show quiz-first tutoring, grounded explanation, **financial tip**, pie chart, 50/30/20 comparison, what-if, and saving plan timeline.

**Numbers to enter (example):**

- Monthly income: **4,000**
- Expenses (adjust to taste but keep totals ≤ income): e.g. rent **1,200**, food **500**, transportation **200**, utilities **150**, entertainment **200**, savings **400**, other **150**
- Goal: **General financial wellness**

**Steps:**

1. Submit the budget form and wait for analysis.
2. **Step 1 — Quiz:** Read the quiz aloud in one sentence, then submit a short good-faith answer (does not need to be perfect).
3. **Step 2 — Grading:** Point out verdict + feedback + answer key.
4. **Step 3 — Results:** Scroll slowly through:
   - Grounded explanation (mention it uses **their** numbers).
   - **Financial tip (rule-grounded)** — call out naming a rule from `financial_rules.md` (this is what Milestone 2 video skipped).
   - Expense pie chart + category list.
   - **50/30/20 comparison.**
   - **What-if** (reduce one discretionary line slightly) → re-run and show updated view.
   - **Saving plan** timeline (months 1–3 / 4–6).
5. Close with one sentence: output source shows **Google AI Studio** (or Vertex) when the key is set.

**One-liner if pressed for time:** “We force a quiz before the tutor explanation and tip so the learner engages before seeing the grounded answer.”

---

## Scenario 2 — Expenses exceed income + what-if

**Purpose:** Show defensive tone, overspending messaging, and the what-if panel under stress.

**Numbers:**

- Monthly income: **3,000**
- Expenses: inflate **food** + **entertainment** (or add categories) so **total expenses > 3,000** (e.g. rent 1,200, food 900, transportation 300, utilities 200, entertainment 500, savings 0, other 600 → total 3,700).

**Steps:**

1. Analyze and complete quiz / grading briefly (short answers OK).
2. On results, highlight negative “remaining” / insights.
3. Open **what-if**: reduce entertainment and food until remaining is **non-negative** (or closer), re-analyze, show the UI update.

**Talking point:** Advice stays educational; the UI still grounds numbers from user input.

---

## Scenario 3 — Deterministic fallback (no API key)

**Purpose:** Show the product works when Gemini is unavailable — aligns with “failure path” expectations for the final demo format.

**Prep:**

- Stop the dev server, **unset** `GEMINI_API_KEY` in `backend/.env` (or export empty in the shell that starts the backend), restart backend + frontend.

**Numbers:** Same as Scenario 1 (or any consistent set).

**Steps:**

1. Submit budget; note **Output source: Deterministic fallback (no AI call)** on results.
2. Walk quickly through quiz → grading → explanation + tip (tone will be template-driven).
3. Optionally flip the key back for Q&A.

**Talking point:** “Calculations and structure always come from our code; the LLM adds narrative when available.”

---

## Timing cheat sheet

| Block                         | Target   |
|------------------------------|----------|
| Scenario 1 (full highlights) | ~3 min   |
| Scenario 2 (overspend + what-if) | ~1.5 min |
| Scenario 3 (fallback)       | ~1 min   |
| Buffer / transitions        | ~0.5 min |

**Total:** ~5–6 minutes for scenarios; rehearse with a timer.

---

## Backup if live fails

Use the prerecorded walkthrough (see Sprint 3 / Sprint 4 tasks) or Scenario 3-only path if only the API fails.
