# Sprint 2 Grade — Venture 5: myDolla$ign

**Graded:** April 15, 2026
**Sprint Window:** April 8 – April 14, 2026
**Student commits in window:** 14 (excluding 1 Zechun Cao commit that seeded the sprint plan)

---

## Overall Grade: 93/100

---

## Summary

A strong sprint. All four P0 UI wiring tasks shipped (pie chart, 50/30/20 comparison, what-if panel, saving plan timeline), the full P1 cleanup pass landed in a single Rene commit (`39bd279`) that deleted the legacy `backend/src/` tree and `backend/templates/index.html`, and two P2 evaluation artifacts were added (`fallback_quality_assessment.md`, `edge_case_testing.md`). Hugo followed through on P3 polish with step animations and mobile responsiveness. Contribution is also much more balanced than Milestone 2: all four students authored at least one non-merge commit this sprint, which directly addresses the biggest concern flagged after M2.

The main gaps are on the evaluation side. The quantitative metrics table (grounding accuracy %, quiz relevance, tip-to-rule mapping) called out in P2 was not produced: `fallback_quality_assessment.md` is a scenario list without numbers, and `edge_case_testing.md` is narrative-only. Real user testing with 3 to 5 non-team members was not documented. The Milestone 2 Deliverables checklist still shows the demo video box unchecked, and the README was not updated for Sprint 2 changes (P3).

---

## Category Breakdown

### 1. Task Completion (38/40)
- **P0 Integrate ExpensePieChart (Gauge):** Done. Wired in `BudgetResults.jsx` line 204, commit `4c456d6`.
- **P0 Integrate BudgetComparison (Hugo):** Done. Wired in `BudgetResults.jsx` line 241, commit `87d9b78` ("Sprint 2: Add 50/30/20 comparison, step animations, and mobile responsiveness").
- **P0 What-if scenario panel (Rene):** Done. New `frontend/src/components/WhatIfPanel.jsx` (152 lines) plus supporting `utils/budgetPayload.js`, wired at `BudgetResults.jsx` line 188 in commit `39bd279`.
- **P0 Saving plan display (Allison):** Done. Saving plan timeline UI added to `BudgetResults.jsx` in commit `e206557` (58 insertions), with fallback support.
- **P1 Remove legacy backend/src/ (Rene):** Done. `ai_tutor.py`, `rule_engine.py`, `prompt_templates.py`, `rules/financial_rules.json`, and `src/__init__.py` all deleted in `39bd279`.
- **P1 Remove legacy Flask template (Rene):** Done. `backend/templates/index.html` deleted in `39bd279`.
- **P1 Clean up demo.py (Gauge):** Done. Commit `38f4af6` ("Clean up demo.py and mark as standalone utility"). Rene's earlier commit also trimmed `demo.py` from 431 lines to a thin utility.
- **P1 Mark demo video complete (Allison):** Not done. `docs/Milestone 2 Deliverables.md` line 194 still shows `- [ ] Demo video is submitted or linked`. Allison did add `docs: add saving plan feature description` (`36ca78e`), so the checklist slip is the only P1 miss.
- **P2 Add quantitative metrics (Allison):** Partially done. No metrics table with numeric pass rates (grounding accuracy %, quiz relevance %, tip-to-rule mapping). The existing `evaluation_test_cases.md` from M2 was not extended with a scored table.
- **P2 Real user testing (All):** Not documented. No evidence of 3 to 5 non-team testers or feedback notes in `docs/`.
- **P2 Edge case expansion (Gauge):** Done. `docs/edge_case_testing.md` covers zero income, expenses greater than income, single category, and extreme values (commit `6a7a970`).
- **P2 Fallback quality assessment (Rene):** Partially done. `docs/fallback_quality_assessment.md` lists 5 scenarios and describes expected differences but does not include side-by-side AI versus fallback outputs or a scored comparison.
- **P3 Loading state animations (Hugo):** Done. Step progress indicator and fade/slide transitions in commit `87d9b78`, new CSS in `frontend/src/index.css` (110 lines).
- **P3 Mobile responsiveness (Hugo):** Done. Same commit, "better touch targets and scaling".
- **P3 Demo rehearsal (All):** Not verifiable from the repo.
- **P3 Update README (Allison):** Not done for Sprint 2. README was touched in Rene's `39bd279` (34 lines changed as part of legacy cleanup), but there is no Sprint 2 feature section documenting the pie chart, 50/30/20 comparison, what-if panel, or saving plan timeline.

**P0: 4/4. P1: 3/4. P2: 2/4 (two partials). P3: 2/4.**

### 2. Code Quality (19/20)
- Legacy removal is clean: 1,237 lines deleted in one Rene commit with no lingering imports.
- New components follow existing patterns. `WhatIfPanel.jsx` is a self-contained 152-line component with its own helper in `utils/budgetPayload.js`.
- Hugo's CSS for step transitions is isolated in `frontend/src/index.css`, does not touch Tailwind utility flow.
- AI token limit bump in `backend/app/services/ai_service.py` addresses a real truncation issue.
- Minor: multiple features landed in one `BudgetResults.jsx` file (now 240+ lines), which is getting wide. Consider splitting into subcomponents in Sprint 3 if it grows further.

### 3. Documentation (12/15)
- Two new docs added: `fallback_quality_assessment.md`, `edge_case_testing.md`.
- `docs/Milestone 2 Deliverables.md` still has the unchecked demo video box.
- README not refreshed for Sprint 2 features.
- No Sprint 2 retrospective or changelog entry.
- `fallback_quality_assessment.md` is thin (17 lines). It describes the comparison plan rather than results.

### 4. Testing / Evaluation (11/15)
- Edge case testing document is present and covers the four scenarios Sprint 2 asked for, but it is descriptive prose rather than a numeric table.
- No quantitative metrics table produced. The "grounding accuracy (% of explanations referencing user's actual numbers)" metric, which was the single most valuable item on the P2 list for the final demo narrative, is still not in the repo.
- No real user testing notes.
- `backend/test_tutor.py` was trimmed (121 → fewer lines) as part of legacy cleanup; no new unit tests were added.

### 5. Team Contribution (13/10)

Bonus given because the post-M2 biggest risk (Hugo doing 70% of the work alone) was meaningfully addressed this sprint. All four students show up in the commit log on substantive work, not just merges.

| Member (login) | Commits | Work |
|---|---|---|
| hpadi02 (Hugo) | 5 non-merge + merges | 50/30/20 wiring, step animations, mobile responsiveness, token limit fix, code-workspace file |
| gmalt02 (Gauge) | 4 | Pie chart integration, edge case testing doc, demo.py cleanup |
| allirose140 (Allison) | 2 | Saving plan timeline UI (feature), saving plan feature doc |
| Rene2x (Rene) | 1 | Large "sprint 2" commit: what-if panel, legacy backend removal, fallback quality doc |

Rene only has one commit, but that commit carries three separate Sprint 2 line items (P0 what-if, P1 legacy removal, P2 fallback assessment) and is the largest diff of the sprint. Allison's two commits are both real and include shipped UI code.

---

## Per-Task Completion Matrix

| Priority | Task | Owner | Status |
|---|---|---|---|
| P0 | Integrate ExpensePieChart | Gauge | Complete |
| P0 | Integrate BudgetComparison | Hugo | Complete |
| P0 | What-if scenario panel | Rene | Complete |
| P0 | Saving plan display | Allison | Complete |
| P1 | Remove legacy backend/src/ | Rene | Complete |
| P1 | Remove legacy Flask template | Rene | Complete |
| P1 | Clean up demo.py | Gauge | Complete |
| P1 | Mark demo video checklist | Allison | Missed (box still unchecked) |
| P2 | Quantitative metrics table | Allison | Missed |
| P2 | Real user testing (3 to 5) | All | Missed / not documented |
| P2 | Edge case expansion | Gauge | Complete |
| P2 | Fallback quality assessment | Rene | Partial (plan only, no results) |
| P3 | Loading animations | Hugo | Complete |
| P3 | Mobile responsiveness | Hugo | Complete |
| P3 | Demo rehearsal | All | Not verifiable |
| P3 | Update README for Sprint 2 | Allison | Missed |

---

## Individual Grade Indicator (Red Flag Only)

Reminder: per course policy, all team members receive the venture grade of **93** unless a contribution issue is formally raised. The table below is a red flag indicator, nothing more.

| Member | Sprint 2 commits (non-merge) | Indicator |
|---|---|---|
| hpadi02 (Hugo) | 5 | Green |
| gmalt02 (Gauge) | 4 | Green |
| Rene2x (Rene) | 1 (large, multi-feature) | Green |
| allirose140 (Allison) | 2 | Green |

No red flags this sprint. The contribution distribution improved significantly from Milestone 2.

---

## Top Items Carrying into Sprint 3

1. Quantitative evaluation metrics table (grounding accuracy, quiz relevance, tip-to-rule mapping) with real numbers.
2. Real user testing with 3 to 5 non-team members, with feedback notes in `docs/`.
3. Expand `fallback_quality_assessment.md` with actual side-by-side AI versus deterministic outputs for the 5 scenarios.
4. README refresh documenting Sprint 2 features (pie chart, 50/30/20 comparison, what-if panel, saving plan timeline).
5. Check the demo video box in `Milestone 2 Deliverables.md`.
