#!/usr/bin/env python3
"""Smoke + regression tests: analyze_budget(), parsing, token config. Run: python test_tutor.py"""

import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BACKEND_DIR))

from dotenv import load_dotenv

load_dotenv(_BACKEND_DIR / ".env")

from app.models.budget import BudgetInput
from app.services.ai_service import (
    analyze_budget,
    build_budget_prompt,
    parse_ai_response,
    _studio_generation_config,
)


def test_smoke_analyze_budget() -> None:
    b = BudgetInput(
        monthly_income=4000.0,
        expenses={
            "rent": 1200,
            "food": 500,
            "transportation": 200,
            "utilities": 150,
            "entertainment": 200,
            "savings": 400,
            "other": 150,
        },
        goal="general",
    )
    out = analyze_budget(b)
    assert out.get("quiz_question")
    print("OK smoke — output_source:", out.get("output_source"))


def test_studio_generation_config_token_ceiling() -> None:
    """
    Regression: commit 87d9b78 raised Google AI Studio max_output_tokens so long tutor
    responses are not truncated. Keep this floor if config is available.
    """
    cfg = _studio_generation_config()
    if cfg is None:
        print("SKIP studio token ceiling — google.generativeai GenerationConfig unavailable")
        return
    max_out = getattr(cfg, "max_output_tokens", None)
    if max_out is None and isinstance(cfg, dict):
        max_out = cfg.get("max_output_tokens")
    assert max_out == 2500, (
        f"expected max_output_tokens=2500 for analyze_budget (regression guard), got {max_out!r}"
    )
    print("OK studio GenerationConfig max_output_tokens:", max_out)


def test_parse_ai_response_long_output() -> None:
    """Very long FINANCIAL ADVICE body should still yield structured sections (truncation safeguard)."""
    filler = "Consider your budget carefully. " * 400
    text = f"""## FINANCIAL ADVICE
{filler}
Your income is $9000.00 and savings line is $900.00 per month.

## QUIZ QUESTION
Given income $9000.00, what fraction of income is the $900.00 savings line?

## QUIZ ANSWER KEY
Strong answers compute 900 / 9000 = 10% and compare to Savings Benchmarks in financial_rules.md.

## GROUNDED TIP
Per Savings Benchmarks (financial_rules.md), your $900.00 savings on $9000.00 income is worth improving toward 15–20%.

## SAVING TIPS
- Move $50 from entertainment toward savings ($900.00 baseline).
- Review subscriptions using your $9000.00 income as the anchor.

## SAVING PLAN (3-6 MONTHS)
Months 1-3:
- Track spending against $9000.00 income
- Add $25/week to savings from the $900.00 line

Months 4-6:
- Aim to grow savings toward 15% of $9000.00

## WHERE SAVINGS COULD GO
High-yield savings and retirement accounts in general terms. Talk to a licensed financial advisor for your situation.

Disclaimer: This is for education only and is not financial advice.
"""
    b = BudgetInput(
        monthly_income=9000.0,
        expenses={
            "rent": 2700,
            "food": 900,
            "transportation": 450,
            "utilities": 300,
            "entertainment": 450,
            "savings": 900,
            "other": 300,
        },
        goal="general",
    )
    out = parse_ai_response(text, b)
    assert "900" in (out.get("quiz_question") or "")
    assert out.get("grounded_tip")
    assert out.get("saving_plan") is not None
    assert out["saving_plan"].get("months_1_3")
    print("OK parse_ai_response long output — quiz + tip + saving_plan present")


def test_build_budget_prompt_many_categories() -> None:
    """Long real-world budgets inflate the prompt; ensure builder still produces a coherent prompt."""
    expenses = {f"line_item_{i}": float(20 * i + 30) for i in range(22)}
    b = BudgetInput(monthly_income=15000.0, expenses=expenses, goal="emergency_fund")
    p = build_budget_prompt(b)
    assert len(p) >= 2800, "prompt should grow materially with many categories"
    assert "CALCULATED SUMMARY" in p
    assert "DETAILED EXPENSES:" in p
    assert "DOCUMENTED RULES" in p
    print("OK build_budget_prompt many categories — len", len(p))


def main() -> None:
    test_smoke_analyze_budget()
    test_studio_generation_config_token_ceiling()
    test_parse_ai_response_long_output()
    test_build_budget_prompt_many_categories()
    print("All tests passed.")


if __name__ == "__main__":
    main()
