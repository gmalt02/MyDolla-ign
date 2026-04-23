"""
Sprint 3 — print markdown snippets for docs/fallback_quality_assessment.md (AI column).

Run on a machine with `google-generativeai` installed and a valid `GEMINI_API_KEY` in
`backend/.env` (or exported in the environment). Prints one JSON block per scenario.

Deterministic column: unset `GEMINI_API_KEY`, clear `GOOGLE_CLOUD_PROJECT`, or use a venv
without the Gemini SDK so `output_source` is `fallback_deterministic`.

Usage (from repo root):
  cd backend
  python scripts/sprint3_capture_ai_column.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.budget import BudgetInput  # noqa: E402
from app.services.ai_service import (  # noqa: E402
    GEMINI_AVAILABLE,
    analyze_budget,
)


def scenarios():
    return [
        (
            "1 — Balanced budget, positive remaining",
            BudgetInput(
                5000,
                {
                    "rent": 1200,
                    "food": 400,
                    "transportation": 200,
                    "utilities": 150,
                    "entertainment": 200,
                    "savings": 800,
                    "other": 100,
                },
                "general",
            ),
        ),
        (
            "2 — Expenses exceed income",
            BudgetInput(
                3000,
                {
                    "rent": 1500,
                    "food": 600,
                    "transportation": 400,
                    "utilities": 200,
                    "entertainment": 300,
                    "savings": 0,
                    "other": 1200,
                },
                "general",
            ),
        ),
        (
            "3 — Zero income",
            BudgetInput(0, {"rent": 800, "food": 200}, "general"),
        ),
        (
            "4 — Housing above ~30% of income",
            BudgetInput(
                4000,
                {
                    "rent": 1800,
                    "food": 400,
                    "transportation": 200,
                    "utilities": 100,
                    "entertainment": 100,
                    "savings": 400,
                    "other": 200,
                },
                "general",
            ),
        ),
        (
            "5 — One category dominates (savings line)",
            BudgetInput(
                6000,
                {
                    "rent": 800,
                    "food": 300,
                    "transportation": 200,
                    "utilities": 150,
                    "entertainment": 100,
                    "savings": 3500,
                    "other": 150,
                },
                "general",
            ),
        ),
    ]


def slim(out: dict) -> dict:
    keys = [
        "output_source",
        "financial_advice",
        "quiz_question",
        "quiz_answer_key",
        "grounded_tip",
        "grounded_rule_citation",
    ]
    return {k: out.get(k) for k in keys}


def _print_preflight() -> None:
    """Explain why runs may be fallback (reduces confusion vs the doc's AI column)."""
    lines = [
        "",
        "=" * 72,
        "SPRINT 3 — AI column capture (`sprint3_capture_ai_column.py`)",
        "=" * 72,
    ]
    if not GEMINI_AVAILABLE:
        lines += [
            "STATUS: No Gemini client library is importable.",
            "  → Install:  pip install google-generativeai",
            "  → Then set GEMINI_API_KEY in backend/.env (Google AI Studio key).",
            "  → Output below will be fallback_deterministic — same as the LEFT column",
            "    in docs/fallback_quality_assessment.md. Do NOT paste it into the AI fence.",
        ]
    elif not os.getenv("GEMINI_API_KEY", "").strip():
        lines += [
            "STATUS: SDK present but GEMINI_API_KEY is empty.",
            "  → Add your key to backend/.env and re-run.",
            "  → Output will stay fallback until the key is set.",
        ]
    else:
        lines += [
            "STATUS: GEMINI_API_KEY is set and a Gemini SDK is available.",
            "  → Expect output_source: google_ai_studio below (unless the API errors).",
        ]
    lines += [
        "",
        "Note: 'python-dotenv could not parse line 1' means fix line 1 of backend/.env",
        "(valid KEY=value or # comment; avoid BOM / odd characters).",
        "",
        "=" * 72,
        "",
    ]
    # stdout so Windows terminals show this before JSON (stderr order is often confusing)
    print("\n".join(lines))


def main() -> None:
    _print_preflight()
    print("<!-- Paste under each scenario's **Google AI Studio** fence in docs/fallback_quality_assessment.md -->\n")
    for title, budget in scenarios():
        out = analyze_budget(budget)
        src = out.get("output_source", "")
        print(f"### {title}\n")
        print(f"`output_source`: `{src}`\n")
        if src != "google_ai_studio":
            print(
                "_Not the AI column — this run used fallback (see STATUS block above). "
                "Fix install/key, then re-run._\n"
            )
        block = json.dumps(slim(out), indent=2, ensure_ascii=False)
        print("```json")
        print(block)
        print("```\n")


if __name__ == "__main__":
    main()
