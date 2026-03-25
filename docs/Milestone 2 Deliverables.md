# Milestone 2 Deliverables
## Team: My Dolla $ign
## Due: April 5, 2026
## Focus: MVP Demo Readiness

---

## Context

Milestone 1 was focused on proving that the project had a grounded AI tutoring direction:

- documented financial rules
- a structured prompt design
- an AI tutor backend
- evaluation cases

Sprint 1 then asked for a minimal UI with:

- budget input
- an Analyze action
- a grounded explanation
- one quiz question
- one financial tip

Milestone 2 is different. By April 1, 2026, you must demonstrate a working MVP, not just documentation or isolated backend pieces.

---

# Milestone 2 Objective

By Milestone 2, your team must demonstrate one stable, end-to-end MVP flow:

- user enters budget information in the UI
- system analyzes that budget through your chosen backend path
- UI shows grounded explanation, one quiz question, and one financial tip
- system handles at least one edge case safely
- team can explain what is real AI output versus deterministic logic

The MVP should favor reliability and clarity over extra features.

---

# 1. Required MVP User Flow

Your live demo must show this exact flow:

1. User enters monthly income and categorized expenses.
2. User clicks `Analyze`.
3. The system returns:
   - one grounded explanation referencing the user's numbers
   - one quiz question tied to that budget
   - one grounded financial tip
4. The UI clearly displays the result.
5. The team demonstrates one failure or refusal case safely.

If the browser path does not work end-to-end, Milestone 2 is incomplete.

---

# 2. MVP Functional Requirements

## A. Single Integrated Backend Path

You must choose one production path for the MVP.

That path must:

- accept the same request shape the frontend sends
- return the same response shape the frontend renders
- use one consistent AI orchestration path
- avoid duplicated logic across multiple incompatible endpoints

## B. Grounded Tutor Output

The MVP output must include:

- explanation referencing real user values
- quiz question derived from that user budget
- tip grounded in at least one documented rule

Generic advice without evidence from the budget or rules does not count.

## C. Safe Fallback Behavior

If the LLM is unavailable, invalid, or missing credentials, the MVP must:

- fail gracefully, or
- return a deterministic fallback that still keeps the demo functional

You must be able to explain this fallback during demo.

## D. UI Completeness

The UI may stay simple, but it must clearly show:

- input form
- loading state
- explanation
- quiz question
- financial tip
- any disclaimer needed for educational use

---

# 3. Required Evidence In The Repository

Your repository must include:

- updated README with correct setup and run instructions
- working frontend and backend code paths for the MVP
- any updated prompt or rule documents if the implementation changed
- `.env.example` with the required environment variable names only
- a short MVP demo guide in `/docs/milestone2_demo.md`

The demo guide must include:

- how to start backend
- how to start frontend
- which URL to open
- one sample budget input
- one fallback or failure-case input

---

# 4. Required Demo Video

Submit a 4 to 7 minute demo video showing:

1. the MVP running in the browser
2. one successful end-to-end analysis
3. where the grounded explanation, quiz, and tip appear
4. one edge case or fallback behavior
5. a brief explanation of your final architecture choice

Store as:

- `/docs/milestone2_demo.mp4`

or link externally from:

- `/docs/milestone2_demo.md`

---

# 5. Acceptance Criteria

Milestone 2 will be evaluated against these criteria:

- The browser flow works end-to-end on demo day.
- The explanation references real values from the user budget.
- The quiz question is tied to the submitted budget.
- The tip is grounded in a documented financial rule.
- The team can explain how grounding is enforced.
- The team can show one safe failure or fallback path.
- README instructions are accurate enough for another team member to run.

---

# 6. What To Cut If Necessary

Do not miss MVP because of optional scope.

If time is tight, cut or defer:

- extra tabs and advanced UI polish
- nonessential visualizations
- extra quiz generation beyond one required question
- optional what-if features
- additional glossary or chatbot features not required for core MVP

---

# 7. Live Review Questions You Should Be Ready To Answer

Be ready to answer:

1. Which backend path is the real MVP path?
2. How does the frontend request match the backend parser?
3. Where is the quiz rendered in the UI?
4. What happens if the AI model fails?
5. How do you know the output is grounded and not generic?

---

# 8. Submission Checklist

- [ ] Browser MVP works end-to-end
- [ ] Explanation, quiz, and tip are visible in the UI
- [ ] Grounding and disclaimer behavior are preserved
- [ ] One fallback or refusal case is demo-ready
- [ ] README is updated and accurate
- [ ] `.env.example` is present
- [ ] `/docs/milestone2_demo.md` is present
- [ ] Demo video is submitted or linked
