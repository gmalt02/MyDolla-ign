# Milestone 2 MVP demo guide

**Team:** My Dolla $ign  
**Milestone 2 focus:** One end-to-end browser flow — budget in → Analyze → quiz answer → **`POST /api/grade-quiz`** (AI verdict: correct / partially correct / incorrect) → answer key → grounded explanation and rule-grounded tip, plus a safe fallback path.

---

## How to start the backend

From the repository root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Configure `.env` (see [backend/.env.example](../backend/.env.example)):

- **Same as the terminal demo (`python demo.py`):** set `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com/apikey). The web app calls Gemini through `google-generativeai` first. Optionally set `GEMINI_MODEL` (e.g. `gemini-2.5-flash` to match `demo.py`).
- **Alternative — Vertex AI:** set `GOOGLE_CLOUD_PROJECT` (and GCP auth). The API uses Vertex only if the Studio path is not configured or fails.
- **No key / no project:** you still get a full response from the **deterministic fallback** (UI: “Deterministic fallback (no AI call)”).

Start the server:

```bash
python main.py
```

Default URL: `http://127.0.0.1:5001` (or the `PORT` in `.env`). Health check: `GET http://127.0.0.1:5001/api/health`.

---

## How to start the frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server proxies `/api` to the backend (see `frontend/vite.config.js`, default `http://127.0.0.1:5001`).

---

## Which URL to open

Open **http://localhost:3000** in your browser (Vite default port).

---

## Sample budget input (happy path)

Use these values on the form, then click **Analyze**:

| Field | Sample value |
|--------|----------------|
| Monthly income | `3500` |
| Rent / Housing | `1100` |
| Food | `450` |
| Transportation | `180` |
| Utilities | `120` |
| Entertainment | `200` |
| Savings | `400` |
| Other | `150` |
| Goal | Any (e.g. General financial wellness) |

You should see:

1. **Step 1:** Category breakdown and the **quiz**. Enter an answer and click **Submit for grading** (empty answers are not accepted).  
2. **Step 2:** **Verdict and feedback** from the grader, your submitted text, and the **answer key**. Then **Continue to explanation and tip**.  
3. **Step 3:** **Grounded explanation** and **rule-grounded tip**. The header still shows the analyze **output source** (e.g. Google AI Studio); the grader step has its own source line when relevant.  
4. Deterministic fallback still applies if credentials or the model are unavailable (see below).

Calculations (breakdown percentages) are **deterministic** in code. Narrative fields are from the model when Vertex is available; otherwise they come from **rule-based strings** in `backend/app/services/ai_service.py`.

---

## Fallback or failure-case input (demo-ready)

Use any **one** of these during the live demo:

1. **No AI / graceful fallback:** Do not configure Vertex (`GOOGLE_CLOUD_PROJECT` empty or invalid). Submit the sample budget above. The UI still shows explanation, quiz, and tip from **deterministic fallback** — this is intentional and safe to explain.  
2. **Validation refusal:** Submit **negative** monthly income (e.g. `-100`) or a **negative** expense. The API returns `400` with a clear message; the UI shows the error alert.  
3. **Zero income edge case:** Set **Monthly income** to `0` and enter some expenses. Analysis still runs; copy explains that planning needs income data, and the quiz reflects that scenario.

---

## Architecture (MVP path)

- **`POST /api/analyze`** — JSON `{ monthly_income, expenses, goal }` in `backend/app/routes/budget.py`.  
- **`POST /api/grade-quiz`** — JSON `{ quiz_question, quiz_answer_key, user_answer }` for the AI verdict after the learner submits the quiz.  
- **Orchestration:** `backend/app/services/ai_service.py` — `analyze_budget()` for the budget pass, `grade_quiz_answer()` for grading (same Studio-then-Vertex order, with a small fallback if grading cannot run).  
- **Frontend:** `frontend/src/App.jsx` → `BudgetForm` → `BudgetResults` (three steps: quiz, grader output, explanation and tip).

---

## Demo video (3–7 minutes)

**Option A — file in repo:** Record your screen and save as:

- `docs/milestone2_demo.mp4`

**Option B — external link:** Upload to your course drive or YouTube (unlisted), then add the link here:

- **Demo video URL:** https://youtu.be/-24v4-w1RqQ

The recording should show: successful analysis in the browser, where explanation / quiz / tip appear, one fallback or refusal case, and a short verbal note on what is **AI** vs **deterministic code**.
