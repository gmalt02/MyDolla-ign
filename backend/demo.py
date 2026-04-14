#!/usr/bin/env python3
"""
My Dolla $ign standalone terminal demo.

Purpose:
- This file is a standalone CLI utility for manually testing the backend
  budget analysis pipeline from the terminal.
- It is NOT the main application UI.
- The primary user experience lives in the frontend + Flask API flow.

What it uses:
- BudgetInput from app.models.budget
- analyze_budget() from app.services.ai_service

Run:
    python demo.py

Optional:
- Set GEMINI_API_KEY in backend/.env to enable AI output
- Without an API key, the deterministic fallback may be used
- Set DEMO_JSON=1 to print the full response payload
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BACKEND_DIR))

from dotenv import load_dotenv

load_dotenv(_BACKEND_DIR / ".env")

from app.models.budget import BudgetInput
from app.services.ai_service import analyze_budget


def _read_money(prompt: str) -> float:
    raw = input(f"{prompt} ($): ").strip().replace(",", "")
    if not raw:
        return 0.0

    try:
        return float(raw.replace("$", ""))
    except ValueError:
        print("Invalid amount entered. Using 0.")
        return 0.0


def _read_goal() -> str:
    print("\nGoal options:")
    print("1 = general")
    print("2 = emergency fund")
    print("3 = debt payoff")
    print("4 = big purchase")

    selected = input("Choice [1-4]: ").strip() or "1"

    goals = {
        "1": "general",
        "2": "emergency_fund",
        "3": "debt_payoff",
        "4": "big_purchase",
    }
    return goals.get(selected, "general")


def main() -> None:
    print("\n=== My Dolla $ign — Standalone Terminal Demo ===")
    print("This utility runs budget analysis directly from the terminal.\n")

    income = _read_money("Monthly income (after tax)")
    expenses = {
        "rent": _read_money("Rent / housing"),
        "food": _read_money("Food"),
        "transportation": _read_money("Transportation"),
        "utilities": _read_money("Utilities"),
        "entertainment": _read_money("Entertainment"),
        "savings": _read_money("Savings"),
        "other": _read_money("Other"),
    }
    goal = _read_goal()

    budget_input = BudgetInput(
        monthly_income=income,
        expenses=expenses,
        goal=goal,
    )

    print("\nAnalyzing budget...\n")
    result = analyze_budget(budget_input)

    print("output_source:", result.get("output_source"))
    print("\n--- financial_advice ---\n")
    print((result.get("financial_advice") or "")[:1200])

    print("\n--- quiz_question ---\n")
    print(result.get("quiz_question", ""))

    print("\n--- grounded_tip ---\n")
    print(result.get("grounded_tip", ""))

    if os.getenv("DEMO_JSON", "").strip().lower() in {"1", "true", "yes"}:
        print("\n--- full_response_json ---\n")
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
