"""
AI Service - Handles Gemini for budget analysis.

Two ways to get real model output (same idea as the terminal demo):

1. **Google AI Studio (recommended for local dev)** — set `GEMINI_API_KEY` in `backend/.env`.
   This is what `demo.py` uses (`google.generativeai`).

2. **Vertex AI** — set `GOOGLE_CLOUD_PROJECT` (and auth). Used when no API key path runs or you
   prefer GCP billing.

If neither works, responses use deterministic fallback (`output_source`: fallback_deterministic).
Calculations (breakdown, etc.) are always done in code.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

from dotenv import load_dotenv

# Ensure backend/.env is loaded even if this module is imported before main.py runs
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from app.models.budget import BudgetInput

# Google AI Studio SDK (API key) — matches backend/demo.py
try:
    import google.generativeai as genai
    GENAI_STUDIO_AVAILABLE = True
except ImportError:
    GENAI_STUDIO_AVAILABLE = False
    genai = None  # type: ignore

# Google Cloud Vertex AI SDK
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel as VertexGenerativeModel
    from vertexai.generative_models import GenerationConfig as VertexGenerationConfig
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False
    vertexai = None  # type: ignore
    VertexGenerativeModel = None  # type: ignore
    VertexGenerationConfig = None  # type: ignore

# True if any Gemini client library is importable (used by glossary/chat guards)
GEMINI_AVAILABLE = GENAI_STUDIO_AVAILABLE or VERTEX_AVAILABLE


def init_vertex_ai():
    """Initialize Vertex AI with project and location from environment."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set")
    
    vertexai.init(project=project_id, location=location)


def _studio_generation_config():
    """Build GenerationConfig for google.generativeai (varies slightly by package version)."""
    if not GENAI_STUDIO_AVAILABLE or genai is None:
        return None
    try:
        return genai.GenerationConfig(max_output_tokens=2500, temperature=0.6)
    except Exception:
        return {"max_output_tokens": 2500, "temperature": 0.6}


def _extract_google_generativeai_text(response) -> str:
    """
    google.generativeai sometimes raises on `.text` when the response is blocked or has no candidates.
    """
    try:
        t = getattr(response, "text", None)
        if t:
            return str(t).strip()
    except ValueError as e:
        print(f"Gemini .text unavailable ({e})")
    feedback = getattr(response, "prompt_feedback", None)
    if feedback is not None:
        print(f"Gemini prompt_feedback: {feedback}")
    candidates = getattr(response, "candidates", None) or []
    if candidates:
        parts = getattr(candidates[0].content, "parts", None) or []
        chunks = [getattr(p, "text", "") for p in parts]
        return "".join(chunks).strip()
    return ""


class GeminiStudioClient:
    """
    Adapts google.generativeai to the `client.models.generate_content(model=..., contents=..., config=...)`
    shape used by glossary/chat routes.
    """

    def __init__(self) -> None:
        self.models = self

    def generate_content(
        self,
        model: str,
        contents: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        if not GENAI_STUDIO_AVAILABLE or genai is None:
            raise RuntimeError("google.generativeai is not installed")
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model)
        cfg = config or {}
        gen_cfg = None
        if cfg:
            try:
                gen_cfg = genai.GenerationConfig(
                    max_output_tokens=int(cfg.get("max_output_tokens", 400)),
                    temperature=float(cfg.get("temperature", 0.6)),
                )
            except Exception:
                gen_cfg = {
                    "max_output_tokens": int(cfg.get("max_output_tokens", 400)),
                    "temperature": float(cfg.get("temperature", 0.6)),
                }
        resp = m.generate_content(contents, generation_config=gen_cfg)
        text = getattr(resp, "text", None) or ""
        return type("Resp", (), {"text": text})()


def get_gemini_client():
    """Client for routes that expect `client.models.generate_content(...)`. Uses AI Studio API key."""
    return GeminiStudioClient()


def build_budget_prompt(budget: BudgetInput) -> str:
    """Build the user prompt for Gemini with budget data and calculated summary."""
    expenses_text = "\n".join([
        f"- {category.replace('_', ' ').title()}: ${amount:.2f}"
        for category, amount in budget.expenses.items()
    ])
    
    # Calculate all metrics in code (for accuracy)
    savings = budget.expenses.get("savings", 0)
    savings_pct = (savings / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
    housing = budget.expenses.get("rent", 0)
    housing_pct = (housing / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
    
    # Find top 3 expense categories
    sorted_expenses = sorted(budget.expenses.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_expenses[:3]
    top_categories_text = ", ".join([
        f"{cat.replace('_', ' ').title()} (${amt:.2f}, {(amt/budget.monthly_income*100):.1f}%)"
        for cat, amt in top_categories
        if budget.monthly_income > 0
    ])
    
    # Determine financial situation
    is_overspending = budget.remaining < 0
    is_low_income = budget.monthly_income < 2000
    is_high_saver = savings_pct >= 20
    is_low_saver = savings_pct < 10 and savings_pct >= 0
    
    # Goal mapping
    goal_descriptions = {
        "general": "general financial wellness",
        "emergency_fund": "building an emergency fund (3-6 months of expenses)",
        "debt_payoff": "paying down debt",
        "big_purchase": "saving for a big purchase (e.g. laptop, car, down payment)"
    }
    goal_text = goal_descriptions.get(budget.goal, "general financial wellness")
    
    # Build calculated summary for AI (so it uses exact numbers)
    calculated_summary = f"""
CALCULATED SUMMARY (use these exact numbers; do not recalculate):
- Monthly income: ${budget.monthly_income:.2f}
- Total expenses: ${budget.total_expenses:.2f}
- Remaining after expenses: ${budget.remaining:.2f}
- Current savings: ${savings:.2f} ({savings_pct:.1f}% of income)
- Housing cost: ${housing:.2f} ({housing_pct:.1f}% of income)
- Top 3 expenses: {top_categories_text if top_categories_text else "N/A"}
- Financial situation: {"⚠️ Overspending" if is_overspending else "✅ Within budget"}
- Savings status: {"✅ Excellent" if is_high_saver else "⚠️ Needs improvement" if is_low_saver else "🟡 Good"}
"""

    # Edge case instructions
    edge_case_instructions = ""
    if is_overspending:
        edge_case_instructions += "\n⚠️ IMPORTANT: Expenses exceed income. Focus advice on reducing spending or increasing income. Do NOT suggest investing until budget is balanced."
    if budget.monthly_income == 0:
        edge_case_instructions += "\n⚠️ IMPORTANT: Income is zero. Explain that a budget plan requires income data."
    if is_low_income:
        edge_case_instructions += "\n⚠️ IMPORTANT: Income is relatively low. Be realistic and encouraging; acknowledge some recommendations may be challenging."
    if is_high_saver:
        edge_case_instructions += "\n✅ IMPORTANT: User is already saving 20%+. Praise this and focus on fine-tuning or next steps."

    documented_rules = """
DOCUMENTED RULES (you MUST tie the grounded tip to exactly one of these by name):
- 50/30/20 Budget Rule (docs/financial_rules.md): 50% needs, 30% wants, 20% savings/debt
- Savings Benchmarks: minimum ~10%, recommended 15–20%, strong 20%+
- Emergency Fund Guideline: 3–6 months of essential expenses
- Housing / needs: housing often recommended at or below ~30% of income (see financial_rules.md)
"""

    return f"""You are a financial educator helping a young adult understand their budget. Use ONLY the calculated numbers I provide below. Do NOT recalculate percentages or totals.

{calculated_summary}

USER'S GOAL: {goal_text}

DETAILED EXPENSES:
{expenses_text}

{documented_rules}

{edge_case_instructions}

Respond with exactly SEVEN sections using these exact headers (order matters):

## FINANCIAL ADVICE
[One short paragraph (3-4 sentences). MUST cite at least two numeric values from the calculated summary (e.g. income, savings $, housing %, remaining $). Tailor to goal: {goal_text}.]

## QUIZ QUESTION
[Exactly ONE question, tied to THIS user's numbers (reference at least one value from the summary). It can be multiple choice or short answer. No trick questions.]

## QUIZ ANSWER KEY
[2-4 sentences: the main ideas a learner should express (not only a single word). Reference the same numbers as the question. The app shows this ONLY after the user tries the question.]

## GROUNDED TIP
[Exactly ONE sentence or short paragraph. MUST name one rule from the DOCUMENTED RULES list above AND reference at least one number from the calculated summary. No specific investment products.]

## SAVING TIPS
[2 to 3 bullet points only; each must use their exact numbers.]

## SAVING PLAN (3-6 MONTHS)
[Two phases — Months 1-3 and Months 4-6 — with bullet actions using their current savings rate ({savings_pct:.1f}%).]

## WHERE SAVINGS COULD GO
[One short paragraph: general vehicles only (e.g. emergency savings, retirement accounts in general terms). End with: Talk to a licensed financial advisor for your situation.]

End with: "Disclaimer: This is for education only and is not financial advice."
"""


def parse_ai_response(response_text: str, budget: BudgetInput) -> Dict[str, Any]:
    """Parse Gemini response into structured sections; keep calculations in code."""
    def find_section(name: str) -> str:
        # Match ## SECTION NAME then take text until next ## or end
        pattern = rf"##\s*{re.escape(name)}\s*\n(.*?)(?=\n##\s|\nDisclaimer:|$)"
        m = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else ""

    financial_advice = find_section("FINANCIAL ADVICE")
    quiz_question = find_section("QUIZ QUESTION")
    quiz_answer_key = find_section("QUIZ ANSWER KEY")
    grounded_tip = find_section("GROUNDED TIP")
    saving_tips_raw = find_section("SAVING TIPS")
    saving_plan_raw = find_section("SAVING PLAN (3-6 MONTHS)") or find_section("SAVING PLAN")
    where_savings_could_go = find_section("WHERE SAVINGS COULD GO")

    # Turn saving tips into list (split by newline, strip bullets/dashes)
    saving_tips = []
    for line in saving_tips_raw.split("\n"):
        line = re.sub(r"^[\s\-*•]+\s*", "", line).strip()
        if line:
            saving_tips.append(line)

    # Parse saving plan (extract Months 1-3 and Months 4-6)
    saving_plan = {}
    if saving_plan_raw:
        # Try to extract Months 1-3 and Months 4-6 sections
        months_1_3_match = re.search(r"Months?\s*1-3[:\-]?\s*(.*?)(?=Months?\s*4-6|$)", saving_plan_raw, re.IGNORECASE | re.DOTALL)
        months_4_6_match = re.search(r"Months?\s*4-6[:\-]?\s*(.*?)$", saving_plan_raw, re.IGNORECASE | re.DOTALL)
        
        if months_1_3_match:
            plan_1_3 = months_1_3_match.group(1).strip()
            # Extract bullets
            bullets_1_3 = []
            for line in plan_1_3.split("\n"):
                line = re.sub(r"^[\s\-*•]+\s*", "", line).strip()
                if line:
                    bullets_1_3.append(line)
            saving_plan["months_1_3"] = bullets_1_3
        
        if months_4_6_match:
            plan_4_6 = months_4_6_match.group(1).strip()
            bullets_4_6 = []
            for line in plan_4_6.split("\n"):
                line = re.sub(r"^[\s\-*•]+\s*", "", line).strip()
                if line:
                    bullets_4_6.append(line)
            saving_plan["months_4_6"] = bullets_4_6

    # Expense breakdown (calculated in code)
    breakdown = []
    for category, amount in sorted(
        budget.expenses.items(), key=lambda x: x[1], reverse=True
    ):
        pct = (amount / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
        breakdown.append({
            "category": category.replace("_", " ").title(),
            "amount": amount,
            "percentage": round(pct, 1),
        })

    # Insights (code-generated for consistency)
    insights = []
    if budget.monthly_income > 0:
        total_pct = (budget.total_expenses / budget.monthly_income * 100)
        insights.append(
            f"Total expenses: ${budget.total_expenses:.2f} ({total_pct:.1f}% of income)"
        )
    if budget.remaining > 0:
        insights.append(f"Remaining: ${budget.remaining:.2f} — consider adding to savings")
    elif budget.remaining < 0:
        insights.append(f"⚠️ Expenses exceed income by ${abs(budget.remaining):.2f}")
    
    savings_pct = (budget.expenses.get("savings", 0) / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
    if savings_pct >= 20:
        insights.append("✅ Excellent savings rate (20%+)")
    elif savings_pct < 10:
        insights.append("💡 Aim to increase savings to 10-20%")
    else:
        insights.append("50/30/20 guideline: 50% needs, 30% wants, 20% savings")

    cited = []
    if grounded_tip:
        for label in (
            "50/30/20",
            "Savings Benchmarks",
            "Emergency Fund",
            "housing",
            "30%",
        ):
            if label.lower() in grounded_tip.lower():
                cited.append(label)
    grounded_rule_citation = ", ".join(cited) if cited else ""

    return {
        "analysis": response_text,
        "financial_advice": financial_advice or response_text[:500],
        "quiz_question": quiz_question or (
            f"With monthly income ${budget.monthly_income:.2f} and savings of "
            f"${budget.expenses.get('savings', 0):.2f}, what percentage of income are you saving, "
            "and how does that compare to the documented 15–20% recommendation?"
        ),
        "quiz_answer_key": quiz_answer_key or (
            f"You are saving {(budget.expenses.get('savings', 0) / budget.monthly_income * 100):.1f}% of "
            f"${budget.monthly_income:.2f} income. Savings Benchmarks (financial_rules.md) suggest working "
            "toward about 15–20% over time."
            if budget.monthly_income > 0
            else "Enter a positive income to compute savings rate and compare it to the 15–20% guideline."
        ),
        "grounded_tip": grounded_tip or (
            "Per Savings Benchmarks (financial_rules.md), aim to grow savings toward 15–20% of income; "
            f"your current savings line is ${budget.expenses.get('savings', 0):.2f} per month."
        ),
        "grounded_rule_citation": grounded_rule_citation or "Savings Benchmarks",
        "saving_tips": saving_tips,
        "saving_plan": saving_plan if saving_plan else None,
        "where_savings_could_go": where_savings_could_go,
        "breakdown": breakdown,
        "insights": insights,
        "goal": budget.goal,
    }


def analyze_budget(budget: BudgetInput) -> Dict[str, Any]:
    """
    Narrative from Gemini: prefers Google AI Studio (`GEMINI_API_KEY`, same as demo.py), else Vertex AI.
    """
    if not GEMINI_AVAILABLE:
        print("No Gemini SDK installed (google-generativeai or vertexai), using fallback")
        out = generate_fallback_response(budget)
        out["output_source"] = "fallback_deterministic"
        return out

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    prompt = build_budget_prompt(budget)

    # 1) Google AI Studio — same path as `python demo.py`
    if api_key and GENAI_STUDIO_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=api_key)
            # Default matches backend/demo.py; override with GEMINI_MODEL in .env if needed
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            model = genai.GenerativeModel(model_name)
            gen_cfg = _studio_generation_config()
            response = model.generate_content(prompt, generation_config=gen_cfg)
            text = _extract_google_generativeai_text(response)
            if not text:
                raise ValueError(
                    "Empty Gemini response (blocked, unsupported model name, or API error — see logs above)"
                )
            parsed = parse_ai_response(text, budget)
            parsed["output_source"] = "google_ai_studio"
            return parsed
        except Exception as e:
            print(f"AI Service Error (Google AI Studio): {type(e).__name__}: {e}")

    # 2) Vertex AI
    if project_id and VERTEX_AVAILABLE and vertexai is not None and VertexGenerativeModel is not None and VertexGenerationConfig is not None:
        try:
            init_vertex_ai()
            model = VertexGenerativeModel("gemini-1.5-flash")
            generation_config = VertexGenerationConfig(
                max_output_tokens=1500,
                temperature=0.6,
            )
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
            )
            text = response.text or ""
            parsed = parse_ai_response(text, budget)
            parsed["output_source"] = "vertex_ai"
            return parsed
        except ValueError as e:
            print(f"AI Service Error (Vertex config): {e}")
        except Exception as e:
            print(f"AI Service Error (Vertex): {e}")

    out = generate_fallback_response(budget)
    out["output_source"] = "fallback_deterministic"
    return out


def _build_grade_quiz_prompt(quiz_question: str, quiz_answer_key: str, user_answer: str) -> str:
    return f"""You are grading a student's short answer for a financial literacy quiz.

Question:
{quiz_question.strip()}

Reference answer (core ideas the student should show; their wording does not need to match):
{quiz_answer_key.strip()}

Student answer:
{user_answer.strip()}

Use these rules:
- CORRECT: the student captures the main numbers or relationships and the right rule or conclusion.
- PARTIALLY CORRECT: some right ideas but missing an important number, nuance, or part of the rule.
- INCORRECT: wrong math, wrong rule, or answer that does not address the question.

Respond in EXACTLY this format (two lines, then optional blank lines):
VERDICT: CORRECT
FEEDBACK: Write 2-4 sentences. Be specific about what they got right and what to tighten. Stay encouraging.

Use only one of these verdicts (exact spelling): CORRECT, PARTIALLY CORRECT, INCORRECT
"""


def _parse_grade_llm_output(text: str) -> tuple[str, str]:
    """Returns (verdict, feedback)."""
    verdict = "PARTIALLY CORRECT"
    vm = re.search(
        r"VERDICT:\s*(CORRECT|PARTIALLY\s+CORRECT|INCORRECT)",
        text,
        re.IGNORECASE,
    )
    if vm:
        raw = re.sub(r"\s+", " ", vm.group(1).strip().upper())
        if "PARTIALLY" in raw:
            verdict = "PARTIALLY CORRECT"
        elif raw == "CORRECT":
            verdict = "CORRECT"
        else:
            verdict = "INCORRECT"
    fm = re.search(r"FEEDBACK:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    feedback = fm.group(1).strip() if fm else text.strip()
    return verdict, feedback


def _call_grader_llm(prompt: str) -> tuple[str, str]:
    """
    Short Gemini call for quiz grading. Returns (response_text, output_source).
    Raises on total failure after both backends tried (caller uses fallback).
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()

    if api_key and GENAI_STUDIO_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=api_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            model = genai.GenerativeModel(model_name)
            try:
                gen_cfg = genai.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.25,
                )
            except Exception:
                gen_cfg = {"max_output_tokens": 2000, "temperature": 0.25}
            response = model.generate_content(prompt, generation_config=gen_cfg)
            text = _extract_google_generativeai_text(response)
            if text:
                return text, "google_ai_studio"
        except Exception as e:
            print(f"Grade quiz (Google AI Studio): {type(e).__name__}: {e}")

    if project_id and VERTEX_AVAILABLE and vertexai is not None and VertexGenerativeModel is not None and VertexGenerationConfig is not None:
        try:
            init_vertex_ai()
            model = VertexGenerativeModel("gemini-1.5-flash")
            generation_config = VertexGenerationConfig(
                max_output_tokens=2000,
                temperature=0.25,
            )
            response = model.generate_content(prompt, generation_config=generation_config)
            text = (response.text or "").strip()
            if text:
                return text, "vertex_ai"
        except Exception as e:
            print(f"Grade quiz (Vertex): {type(e).__name__}: {e}")

    raise RuntimeError("No grader response")


def grade_quiz_answer(quiz_question: str, quiz_answer_key: str, user_answer: str) -> Dict[str, Any]:
    """
    AI-assisted grading (terminal-style verdict). Same credential order as analyze_budget.
    """
    q = (quiz_question or "").strip()
    key = (quiz_answer_key or "").strip()
    ans = (user_answer or "").strip()
    if not q or not ans:
        raise ValueError("quiz_question and user_answer are required and cannot be empty")

    if not GEMINI_AVAILABLE:
        v, fb = "PARTIALLY CORRECT", (
            "The grader service is not available in this environment. Use the answer key and "
            "explanation on the next step to check your reasoning."
        )
        return {"verdict": v, "feedback": fb, "output_source": "fallback_deterministic"}

    prompt = _build_grade_quiz_prompt(q, key or "See the grounded explanation for core ideas.", ans)
    try:
        raw, src = _call_grader_llm(prompt)
        verdict, feedback = _parse_grade_llm_output(raw)
        return {"verdict": verdict, "feedback": feedback, "output_source": src}
    except Exception as e:
        print(f"Grade quiz fallback: {e}")
        return {
            "verdict": "PARTIALLY CORRECT",
            "feedback": (
                "We could not get an automated grade right now. When you continue, compare your answer "
                "to the answer key and the full explanation."
            ),
            "output_source": "fallback_deterministic",
        }


def generate_fallback_response(budget: BudgetInput) -> Dict[str, Any]:
    """Rule-based fallback when Gemini is unavailable or errors."""
    savings = budget.expenses.get("savings", 0)
    savings_pct = (savings / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
    housing_pct = (
        (budget.expenses.get("rent", 0) / budget.monthly_income) * 100
        if budget.monthly_income > 0
        else 0
    )

    # Financial advice
    financial_advice = (
        f"Based on your income of ${budget.monthly_income:.2f} and expenses of "
        f"${budget.total_expenses:.2f}, you have ${budget.remaining:.2f} left. "
    )
    if budget.remaining < 0:
        financial_advice += (
            f"⚠️ Your expenses exceed income by ${abs(budget.remaining):.2f}. "
            "Focus on reducing spending or increasing income before saving."
        )
    elif housing_pct > 30:
        financial_advice += (
            f"Housing is {housing_pct:.1f}% of your income (often recommended under 30%). "
        )
    if savings_pct < 20 and savings_pct >= 0 and budget.remaining >= 0:
        financial_advice += (
            f"You're saving {savings_pct:.1f}%; building toward 20% can help long-term. "
        )
    financial_advice += "Small steps add up—focus on one category to improve first."

    quiz_question = ""
    if budget.monthly_income <= 0:
        quiz_question = (
            "Why is entering a positive monthly income required before the tool can compute "
            "percentages like savings rate or housing share of income?"
        )
    else:
        quiz_question = (
            f"Your documented savings line is ${savings:.2f} per month, which is {savings_pct:.1f}% of "
            f"your ${budget.monthly_income:.2f} income. Per Savings Benchmarks in financial_rules.md, "
            "what is the recommended range for savings as a percentage of income?"
        )

    if budget.monthly_income <= 0:
        quiz_answer_key = (
            "Income is needed so the tool can divide savings (and other categories) by income to get "
            "percentages. Add your monthly take-home pay, then re-run Analyze."
        )
    else:
        quiz_answer_key = (
            f"Strong answers note that you save {savings_pct:.1f}% (${savings:.2f} of "
            f"${budget.monthly_income:.2f}). Savings Benchmarks in financial_rules.md describe about "
            "10% as a common minimum floor, roughly 15–20% as a healthy target, and 20%+ as strong."
        )

    grounded_tip = ""
    if housing_pct > 30 and budget.monthly_income > 0:
        grounded_tip = (
            f"Housing is {housing_pct:.1f}% of income; our financial_rules.md housing guideline suggests "
            "keeping housing near or below ~30% when possible—so this is a key area to revisit."
        )
    elif savings_pct < 15 and budget.monthly_income > 0:
        grounded_tip = (
            f"Per Savings Benchmarks (financial_rules.md), recommended savings are about 15–20% of income; "
            f"at {savings_pct:.1f}% (${savings:.2f}/month on ${budget.monthly_income:.2f}), gradual increases help."
        )
    else:
        grounded_tip = (
            "Per the Emergency Fund Guideline (financial_rules.md), aim for 3–6 months of essential expenses "
            f"in accessible savings; your total expenses are ${budget.total_expenses:.2f}/month in this budget."
        )

    grounded_rule_citation = (
        "Housing ~30% guideline"
        if housing_pct > 30 and budget.monthly_income > 0
        else "Savings Benchmarks"
        if savings_pct < 15 and budget.monthly_income > 0
        else "Emergency Fund Guideline"
    )

    saving_tips = []
    if budget.remaining > 0:
        saving_tips.append(f"Consider directing part of the ${budget.remaining:.2f} remaining toward savings.")
    saving_tips.append("Set up automatic transfers to savings on payday.")
    if budget.remaining < 0:
        saving_tips.insert(0, "Review your top expenses—reducing any category improves the gap.")

    # Saving plan (fallback)
    saving_plan = {
        "months_1_3": [
            f"Increase savings from {savings_pct:.1f}% to {(savings_pct + 2):.1f}%",
            "Set up automatic transfer of $50-100/month to savings",
            "Build emergency fund: aim for $500-1000 first"
        ],
        "months_4_6": [
            f"Grow savings to {(savings_pct + 5):.1f}% of income",
            "Increase emergency fund to 1-2 months of expenses",
            "Review and optimize top expense categories"
        ]
    }

    where_savings_could_go = (
        "After an emergency fund, people often learn about high-yield savings accounts, "
        "retirement accounts (e.g. 401(k), IRA), and broad market index funds. "
        "Talk to a licensed financial advisor for your situation."
    )

    # Breakdown
    breakdown = []
    for category, amount in sorted(
        budget.expenses.items(), key=lambda x: x[1], reverse=True
    ):
        pct = (amount / budget.monthly_income * 100) if budget.monthly_income > 0 else 0
        breakdown.append({
            "category": category.replace("_", " ").title(),
            "amount": amount,
            "percentage": round(pct, 1),
        })

    # Insights
    insights = []
    if budget.monthly_income > 0:
        insights.append(
            f"Total expenses: {(budget.total_expenses / budget.monthly_income * 100):.1f}% of income"
        )
    if budget.remaining != 0:
        insights.append(f"Remaining: ${budget.remaining:.2f}")
    if savings_pct >= 20:
        insights.append("✅ Excellent savings rate")
    else:
        insights.append("50/30/20: 50% needs, 30% wants, 20% savings")

    return {
        "analysis": f"{financial_advice}\n\n" + "\n".join(f"- {t}" for t in saving_tips),
        "financial_advice": financial_advice,
        "quiz_question": quiz_question,
        "quiz_answer_key": quiz_answer_key,
        "grounded_tip": grounded_tip,
        "grounded_rule_citation": grounded_rule_citation,
        "saving_tips": saving_tips,
        "saving_plan": saving_plan,
        "where_savings_could_go": where_savings_could_go,
        "breakdown": breakdown,
        "insights": insights,
        "goal": budget.goal,
        "output_source": "fallback_deterministic",
    }
