# Sprint 3 Plan — Venture 5: myDolla$ign

**Sprint Duration:** April 15 – April 21, 2026
**Sprint Goal:** Lock down evaluation evidence, gather real user feedback, refresh documentation, and begin final demo rehearsal so Sprint 4 can be pure polish.
**Final Demo:** April 29, 2026

---

## Context

Sprint 2 landed every P0 item: the pie chart, 50/30/20 comparison, what-if panel, and saving plan timeline are all wired into `BudgetResults.jsx`, and the legacy Milestone 1 backend (`backend/src/`, `backend/templates/`) is gone. Contribution was also much more balanced, with all four students shipping code. The remaining weak spot is evaluation evidence: the grounding accuracy metrics table was never produced, real user testing has not happened, and `fallback_quality_assessment.md` describes a comparison plan rather than showing results. Sprint 3 closes those gaps and begins demo preparation.

---

## Sprint 3 Tasks

### P0 — Evaluation Evidence (Days 1–4)

| Task | Owner | Description |
|---|---|---|
| Quantitative metrics table | Allison | Create a scored table in `docs/evaluation_metrics.md`: (a) grounding accuracy, percent of explanations that reference at least one of the user's actual expense numbers, (b) quiz relevance, percent of quiz questions tied to a submitted category, (c) tip-to-rule mapping, percent of tips traceable to a rule in `financial_rules.md`. Run against at least 10 of the 20 scenarios in `evaluation_test_cases.md`. Include raw JSON samples. |
| Fallback side-by-side results | Rene | Extend `docs/fallback_quality_assessment.md` with actual AI and deterministic outputs for the 5 scenarios already listed. Toggle by unsetting the API key for deterministic runs. Note concrete differences in tone, specificity, and numeric grounding. |
| Real user testing | Gauge + Hugo | Recruit 3 to 5 non-team-member testers (other CSCI students are fine). Each tester inputs their own budget, walks through all three steps, and fills a short feedback form (clarity, trust, usefulness, one bug, one ask). Save notes to `docs/user_testing.md`. |

### P1 — Demo Readiness (Days 2–5)

| Task | Owner | Description |
|---|---|---|
| Final demo script | Hugo | Write `docs/final_demo_script.md`: scenario 1 balanced budget happy path through all 3 steps including the explanation and financial tip (the step that was skipped in the M2 video), scenario 2 expenses exceed income with what-if reduction, scenario 3 fallback path with API key unset. Target 5 to 6 minutes. |
| README refresh | Allison | Add a Sprint 2 features section to `README.md` covering pie chart, 50/30/20 comparison, what-if panel, and saving plan timeline. Update any stale setup steps after the `backend/src/` removal. |
| Check M2 deliverables box | Allison | `docs/Milestone 2 Deliverables.md` line 194 still shows `- [ ]` for the demo video. Flip it to `- [x]` and confirm the link is in `milestone2_demo.md`. |
| Demo rehearsal round 1 | All | Full team walk-through of the demo script on a real machine. Time it, note hiccups, file issues. |

### P2 — UI and Backend Polish (Days 3–6)

| Task | Owner | Description |
|---|---|---|
| BudgetResults refactor | Gauge | `frontend/src/components/BudgetResults.jsx` now hosts pie chart, comparison, what-if, saving plan, and step animations in one file. Split into at least two subcomponents so the final demo code review is readable. |
| Pie chart label alignment | Gauge | Fix the minor label misalignment noted in `edge_case_testing.md` under "Minor Issues Identified". |
| What-if edge cases | Rene | Test the what-if panel under: reducing a category to a negative value, reducing all categories simultaneously, increasing a category beyond income. Add input clamping if needed. |
| Token limit regression check | Hugo | Confirm the AI token limit increase from commit `87d9b78` does not cause truncation on long budgets. Add 1 to 2 test cases to `backend/test_tutor.py`. |

### P3 — Nice to Have (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| Error toast component | Hugo | Replace any raw error text with a dismissible toast so failed API calls look clean during the live demo. |
| Accessibility pass | Allison | Check color contrast on the pie chart and step indicator, add alt text where relevant, keyboard navigation through the form. |
| Record backup demo video | Rene | Record a 5 minute screen capture of the full flow as a fallback if the live demo fails on April 29. |

---

## Definition of Done (Sprint 3)

- [ ] `docs/evaluation_metrics.md` exists with at least 3 quantitative metrics scored against 10+ scenarios
- [ ] `docs/fallback_quality_assessment.md` contains real AI and deterministic outputs side by side
- [ ] `docs/user_testing.md` documents feedback from 3+ non-team testers
- [ ] `docs/final_demo_script.md` exists with scenario walkthroughs and target timing
- [ ] README has a Sprint 2 features section
- [ ] Demo video checkbox in `Milestone 2 Deliverables.md` is checked
- [ ] At least one full team rehearsal completed
- [ ] Each team member has code or documentation commits this sprint

---

## Contribution Expectations

Sprint 2 was the most balanced sprint of the semester for this team. Keep that going. Specifically:

- **Allison** owns evaluation metrics and the README refresh. These are the two most visible gaps from Sprint 2 and the highest leverage items for the final demo narrative.
- **Rene** owns the fallback side-by-side document and what-if edge cases. Rene's Sprint 2 contribution was one large commit; Sprint 3 should break into 2 to 3 smaller commits.
- **Gauge** owns user testing recruitment (along with Hugo) and the `BudgetResults.jsx` refactor.
- **Hugo** owns the final demo script and token limit regression check. Hugo has led the UI throughout, which makes Hugo the right person to drive the demo narrative.

---

## Carry-forward from Sprint 2

| Item | Sprint 2 status | New owner |
|---|---|---|
| Quantitative metrics table | Missed | Allison (P0) |
| Real user testing 3 to 5 | Missed | Gauge + Hugo (P0) |
| Fallback quality assessment with results | Partial (plan only) | Rene (P0) |
| README refresh for Sprint 2 features | Missed | Allison (P1) |
| Check demo video box | Missed | Allison (P1) |

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 3 (this sprint) | Apr 15–21 | Evaluation evidence, user testing, demo script, rehearsal 1 |
| Sprint 4 | Apr 22–28 | Final polish, rehearsal 2, backup recording, final deliverables pass |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |

---

## Final Demo Day Heads-Up (April 29)

Two weeks out. Rehearse toward this format during Sprint 3 and Sprint 4.

**12 minutes per team, hard cap.** I will cut you off at 12:00 to keep all 8 teams on schedule, so rehearse to 10:30 or 11:00 to leave margin. Suggested split:

1. **About 3 min: overall design.** What the product does, the core pipeline, and the architectural decisions that matter (retrieval strategy, validator or grounding approach, refusal policy). No code walkthroughs.
2. **About 4 min: individual contributions.** Every team member speaks briefly about what they personally owned this semester. Plan what you will say, roughly 45 to 60 seconds each.
3. **About 4 min: live demo of the highlights.** Pick 2 or 3 scenarios from your existing demo script. Required: at least one refusal or failure case and at least one end-to-end grounded answer. Do not spend this time on UI polish.
4. **About 1 min: Q&A**, included in the 12 minutes.

**Running order** is Venture 1 through Venture 8 in order, so myDolla$ign presents fifth.

**Backup plan:** have a prerecorded screen capture of the working path ready in case the live demo fails. Internet or API hiccups are not an excuse on demo day.

**Slides and runbook:** not due before the presentation, but both are required artifacts in the final deliverables package due May 3. Save them under `docs/Final_Demo/` in your repo.

**Avoid:** narrating code, reading slides verbatim, skipping the refusal case, opening with missing features. Present the version you are proud of.

Rehearse the full 12 minutes end to end at least twice, at least once with a timer.
