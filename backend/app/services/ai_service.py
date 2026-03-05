"""
AI Service - Handles Gemini API for budget analysis.

Uses Google Vertex AI (paid, uses your Google Cloud credits) to generate:
- Financial advice (1 paragraph)
- Saving tips (personalized)
- Personalized saving plan (3-6 months timeline)
- Where savings could go (educational, no specific investment recommendations)
Calculations (totals, percentages, breakdown) are done in code.
"""

import os
import re
from typing import Dict, List, Any
from app.models.budget import BudgetInput

# Google Cloud Vertex AI SDK
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def init_vertex_ai():
    """Initialize Vertex AI with project and location from environment."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set")
    
    vertexai.init(project=project_id, location=location)


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

    return f"""You are a financial educator helping a young adult understand their budget. Use ONLY the calculated numbers I provide below. Do NOT recalculate percentages or totals.

{calculated_summary}

USER'S GOAL: {goal_text}

DETAILED EXPENSES:
{expenses_text}

{edge_case_instructions}

Respond with exactly FOUR sections using these exact headers:

## FINANCIAL ADVICE
[One short paragraph (3-4 sentences) of personalized financial advice. Use the exact numbers from the calculated summary above. Mention their biggest lever (e.g. housing, top expense) or what they're doing well. Tailor to their goal: {goal_text}. Be encouraging and realistic.]

## SAVING TIPS
[3 to 5 bullet points with specific, actionable saving tips. Base tips on their exact numbers. If overspending, focus on cutting expenses. If they have remaining money, suggest how to allocate it. Mention emergency fund if relevant. Tailor to goal: {goal_text}. No specific products.]

## SAVING PLAN (3-6 MONTHS)
[Create a realistic timeline with 2 phases:
- "Months 1-3": 2-3 specific actions with target savings percentage
- "Months 4-6": 2-3 next steps to build on progress
Use their current savings rate ({savings_pct:.1f}%) as starting point. Make small, achievable steps. Tailor to goal: {goal_text}.]

## WHERE SAVINGS COULD GO
[One short paragraph only. Explain in general terms where people often put savings after building an emergency fund: e.g. high-yield savings accounts, retirement accounts like 401(k) or IRA, broad market index funds. Do NOT recommend specific funds or products. End with: "Talk to a licensed financial advisor for your situation."]

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
    saving_tips_raw = find_section("SAVING TIPS")
    saving_plan_raw = find_section("SAVING PLAN")
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

    return {
        "analysis": response_text,  # keep full text for backward compatibility
        "financial_advice": financial_advice or response_text[:500],
        "saving_tips": saving_tips,
        "saving_plan": saving_plan if saving_plan else None,
        "where_savings_could_go": where_savings_could_go,
        "breakdown": breakdown,
        "insights": insights,
        "goal": budget.goal,
    }


def analyze_budget(budget: BudgetInput) -> Dict[str, Any]:
    """
    Analyze budget: calculations in code, narrative from Gemini via Vertex AI.
    Returns structured result with financial_advice, saving_tips, saving_plan, where_savings_could_go.
    """
    if not GEMINI_AVAILABLE:
        print("Vertex AI SDK not available, using fallback")
        return generate_fallback_response(budget)

    try:
        # Initialize Vertex AI
        init_vertex_ai()
        
        # Use gemini-1.5-flash (fast and cheap) or gemini-1.5-pro (better quality)
        model = GenerativeModel("gemini-1.5-flash")
        
        prompt = build_budget_prompt(budget)
        
        generation_config = GenerationConfig(
            max_output_tokens=1500,
            temperature=0.6,
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
        )
        
        text = response.text or ""
        return parse_ai_response(text, budget)
    except ValueError as e:
        print(f"AI Service Error (config): {e}")
        return generate_fallback_response(budget)
    except Exception as e:
        print(f"AI Service Error: {e}")
        return generate_fallback_response(budget)


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

    # Saving tips
    saving_tips = []
    if budget.remaining > 0:
        saving_tips.append(f"Add ${budget.remaining:.2f} to savings or an emergency fund.")
    saving_tips.append("Set up automatic transfers to savings on payday.")
    saving_tips.append("Aim for 3–6 months of expenses in an emergency fund.")
    if savings_pct < 20:
        saving_tips.append("Try increasing savings by 1–2% of income each month.")
    if budget.remaining < 0:
        saving_tips.insert(0, "Review your top 3 expenses—can any be reduced?")

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
        "saving_tips": saving_tips,
        "saving_plan": saving_plan,
        "where_savings_could_go": where_savings_could_go,
        "breakdown": breakdown,
        "insights": insights,
        "goal": budget.goal,
    }
