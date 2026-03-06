# Prompt Design Documentation
## My Dolla $ign AI Budget Tutor

Version: 1.0  
Date: February 15, 2026  
Authors: Hugo, Rene, Gauge, Allison

## 1. Overview

This document describes how we design prompts for the AI Budget Tutor. The goal is to make sure all AI outputs are:

1. Based on real user financial data
2. Linked to documented financial rules
3. Returned in a predictable JSON format
4. Free from made up numbers or unsupported claims

## 2. Prompt Template

The prompt is built in `/backend/src/prompt_templates.py` using the `build_tutor_prompt()` function.

### 2.1 Structure

The prompt has four main sections:

1. System Instructions (role, allowed data, rules, output format)
2. User Data (income, expenses, goal, remaining balance)
3. Financial Rules (all rules plus relevant ones for this user)
4. Output Reminder (JSON format requirements)

### 2.2 Key Instructions

**Role Definition**
```
You are an educational budgeting tutor for a student project.
```

**Data Access Constraints**
```
You are ONLY allowed to use:
- The user financial data under "user_profile" below.
- The financial rules under "financial_rules" below.

You MUST NOT:
- Invent or estimate any numbers that are not present in user_profile.
- Add external financial products, providers, or projections.
- Give personalized investment recommendations.
```

**Grounding Requirements**
```
- Every explanation MUST reference at least one actual numeric value from user_profile.
- Every tip MUST reference at least one rule from financial_rules by its "id".
- The quiz question MUST clearly relate to the user's specific budget breakdown.
```

## 3. Grounding Mechanism

### 3.1 How Financial Rules Are Injected

1. Rule Loading: `RuleEngine` loads rules from `/backend/src/rules/financial_rules.json`
2. Rule Selection: `select_relevant_rules()` filters rules based on user data
3. Prompt Injection: Both all rules and relevant rules are added to the prompt

### 3.2 Rule Reference Enforcement

The prompt requires:
- `tip.rule_ids` must contain at least one rule ID when status is "ok"
- `used_rule_ids` must list all rules referenced anywhere in the response
- Rule IDs must match exactly (for example, `R_50_30_20`, `R_HOUSING_COST`)

### 3.3 Available Financial Rules

| Rule ID | Name | Description |
|---------|------|-------------|
| R_50_30_20 | 50/30/20 Budget Guideline | 50% needs, 30% wants, 20% savings |
| R_HOUSING_COST | Housing Cost Guideline | Housing should be 30% or less of income |
| R_SAVINGS_BENCHMARKS | Savings Rate Benchmarks | 10 to 20% savings rate targets |
| R_EMERGENCY_FUND | Emergency Fund Target | 3 to 6 months of expenses |
| R_DEBT_WARNING | Debt to Income Warning | DTI should stay below 36% |

## 4. Refusal Strategy

The AI is told to refuse tutoring when data is missing:

```
If any of the following are missing or null:
- user_profile.monthly_income
- user_profile.expenses (empty or missing)
then you MUST NOT attempt to tutor and MUST respond with a JSON object whose
"status" field is exactly "Insufficient data".
```

### 4.1 Refusal Response Format

When refusing, the AI returns:
```json
{
  "status": "Insufficient data",
  "explanation": "Key budget information is missing. Please provide income and categorized expenses.",
  "quiz": {
    "question": "Why is it important to know both income and expenses?",
    "answer": "Without both, you cannot see whether you are overspending.",
    "rule_ids": []
  },
  "tip": {
    "text": "Start by listing all sources of monthly income and main expense categories.",
    "rule_ids": []
  },
  "used_rule_ids": []
}
```

## 5. Output Format Requirements

### 5.1 JSON Schema

```json
{
  "status": "ok or Insufficient data",
  "explanation": "budget analysis with real numbers",
  "quiz": {
    "question": "question about user budget",
    "answer": "correct answer",
    "rule_ids": ["array of rule IDs"]
  },
  "tip": {
    "text": "actionable suggestion",
    "rule_ids": ["array of rule IDs"]
  },
  "used_rule_ids": ["array of all rule IDs used"]
}
```

### 5.2 Format Enforcement

The prompt specifies:
- Return exactly one JSON object
- The JSON must be valid (no comments, no trailing commas)
- Do not include any text outside the JSON
- Do not include backticks or code fences

The model is also configured with `response_mime_type="application/json"` to force JSON output.

## 6. Example Input and Output

### Input (User Data)
```python
{
    "monthly_income": 4000,
    "total_expenses": 3500,
    "remaining": 500,
    "goal": "emergency_fund",
    "expenses": {
        "rent": 1400,
        "food": 500,
        "transportation": 300,
        "utilities": 150,
        "entertainment": 400,
        "savings": 400,
        "other": 350
    }
}
```

### Output (AI Response)
```json
{
  "status": "ok",
  "explanation": "Your monthly income is $4000, and your total expenses are $3500, leaving you with $500 remaining each month. Your rent of $1400 represents 35% of your income, which is above the recommended 30% guideline.",
  "quiz": {
    "question": "According to the Housing Cost Guideline, what percentage of your $4000 monthly income should your rent ideally be at or below?",
    "answer": "Your rent should ideally be at or below 30% of your income, which would be $1200 or less.",
    "rule_ids": ["R_HOUSING_COST"]
  },
  "tip": {
    "text": "To build your emergency fund faster, consider increasing your monthly savings from $400 (10%) toward $800 (20%). The 50/30/20 rule recommends allocating 20% of income to savings.",
    "rule_ids": ["R_50_30_20", "R_SAVINGS_BENCHMARKS"]
  },
  "used_rule_ids": ["R_HOUSING_COST", "R_50_30_20", "R_SAVINGS_BENCHMARKS"]
}
```

## 7. Model Configuration

```python
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=genai.GenerationConfig(
        temperature=0.0,
        top_p=0.1,
        max_output_tokens=4096,
        response_mime_type="application/json",
    ),
)
```

Why these settings:
- temperature=0.0: Ensures consistent, reproducible outputs
- top_p=0.1: Reduces randomness in word selection
- response_mime_type: Forces JSON only output

## 8. Validation Pipeline

After receiving the AI response:

1. JSON Parse: Try to parse as JSON. If it fails, use fallback response
2. Schema Validation: Check all required fields exist
3. Rule Verification: Make sure cited rule IDs exist in loaded rules
4. Fallback: Return safe response on any failure

## 9. Security Considerations

- No user data is stored or logged
- API keys are loaded from environment variables only
- Strict output format helps prevent prompt injection
- No external URLs or code execution in AI responses

## 10. Consistency of Output Design

The AI Budget Tutor is designed to produce structured and consistent outputs. Each response must follow a fixed JSON format containing a status field, explanation, quiz object, tip object, and used_rule_ids list. This makes the tutor easier to test, validate, and integrate with the rest of the application.

To support more consistent behavior, the model configuration uses a temperature of `0.0` and a `top_p` value of `0.1`. These settings reduce randomness and help the model stay focused on the provided financial data and documented financial rules.

This design is useful during development and evaluation because it makes tutor responses more stable and easier to compare against project requirements.

## 11. Rule Traceability

A key design feature of the AI Budget Tutor is rule traceability. The system includes rule identifiers such as `R_50_30_20`, `R_HOUSING_COST`, `R_SAVINGS_BENCHMARKS`, `R_EMERGENCY_FUND`, and `R_DEBT_WARNING` so that generated guidance can be connected back to documented financial rules.

This is especially important for the tip portion of the response. When the tutor returns a status of `ok`, the `tip.rule_ids` field must contain at least one valid rule ID. In addition, the `used_rule_ids` field provides a summary of the rules referenced in the final response.

Rule traceability helps keep the tutor grounded in the project rule base instead of relying on unsupported financial advice. It also makes validation easier because developers can check whether referenced rule IDs match the rules loaded by the system.

## 12. Educational Purpose

The AI Budget Tutor is designed as an educational budgeting tool for a student project. Its purpose is to help users better understand their income, expenses, and financial goals using grounded financial rules and their own budget data.

The response structure supports this goal by including an explanation, a quiz question, and a practical tip. The explanation interprets the user's financial data, the quiz reinforces a budgeting concept, and the tip provides an actionable suggestion linked to one or more financial rules.

By grounding responses in user data and rule-based guidance, the tutor supports financial literacy while staying within the limited scope defined by the project.
