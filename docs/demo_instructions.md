# Demo Instructions
## My Dolla $ign Milestone 1 Technical Walkthrough

This guide covers how to record the 5 to 8 minute technical walkthrough video for Milestone 1.

## First Time Setup

If this is your first time running the project, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/MyDolla-Sign.git
cd MyDolla-Sign
```

### 2. Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Then edit the `.env` file and add the Gemini API key:

```
GEMINI_API_KEY=your-api-key-here
```

To get an API key:
1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click Create API Key
4. Copy the key and paste it in your .env file

### 5. Verify Setup

```bash
python test_tutor.py
```

If this runs successfully and shows "Status: ok", you are ready.

## Requirements

- Python 3.10 or higher
- Internet connection (to call Gemini API)

## Quick Start (If Already Set Up)

```bash
cd backend
source venv/bin/activate
python demo.py
```

## Video Structure (5 to 8 minutes)

### Part 1: Code Walkthrough (2 to 3 minutes)

Before running the demo, walk through the code architecture.

#### 1.1 Show ai_tutor.py

Open `backend/src/ai_tutor.py` and explain:

```
"This is the core AI tutor module. It has three main responsibilities:

First, it validates user data. The _has_minimum_data method checks that 
we have both income and expenses before proceeding. If data is missing, 
we return a safe refusal response instead of generating potentially 
misleading advice.

Second, it loads financial rules through the RuleEngine. These rules 
like the 50/30/20 guideline and housing cost thresholds are what ground 
our AI responses in verified financial principles.

Third, the generate_session method orchestrates everything. It builds 
a structured prompt, calls the Gemini API, and parses the JSON response 
into a validated TutorResult object."
```

#### 1.2 Show rule_engine.py

Open `backend/src/rule_engine.py` and explain:

```
"The RuleEngine loads our financial rules from a JSON file. Each rule 
has an ID like R_50_30_20 or R_HOUSING_COST, along with parameters 
and thresholds.

The select_relevant_rules method analyzes the user data and picks 
which rules apply. For example, if housing exceeds 30% of income, 
it flags the R_HOUSING_COST rule as relevant. This helps the AI 
focus on the most important issues for each user."
```

#### 1.3 Show prompt_templates.py

Open `backend/src/prompt_templates.py` and explain:

```
"This module builds our structured prompt. The key innovation here 
is grounding. We explicitly tell the AI:

One, you can only use the numbers provided in user_profile.
Two, every tip must reference a rule by its ID.
Three, if data is missing, refuse with status Insufficient data.

We also enforce JSON output format. The AI must return exactly one 
JSON object with status, explanation, quiz, tip, and used_rule_ids 
fields. This makes the response predictable and easy to validate."
```

#### 1.4 Show financial_rules.json

Open `backend/src/rules/financial_rules.json` and explain:

```
"Here are our documented financial rules. Each rule has:

An ID for reference, like R_50_30_20.
A name and description explaining what it is.
Parameters with specific thresholds.

For example, the 50/30/20 rule specifies 50% for needs, 30% for wants, 
and 20% for savings. The housing cost rule sets 30% as the maximum 
recommended percentage for housing expenses.

These rules are injected into the prompt so the AI can cite them 
in its responses. This prevents hallucination and ensures every 
piece of advice is grounded in documented principles."
```

### Part 2: Live Demo (3 to 4 minutes)

#### 2.1 Run the Demo

```bash
python demo.py
```

#### 2.2 Enter Budget Data

Use these example values:

| Field | Value |
|-------|-------|
| Income | 3500 |
| Rent | 1200 |
| Food | 400 |
| Transportation | 200 |
| Utilities | 150 |
| Entertainment | 300 |
| Savings | 200 |
| Other | 100 |
| Goal | 1 (emergency fund) |

While entering, explain:

```
"I am entering a monthly income of $3500. For rent, I am putting $1200 
which is about 34% of my income. This is above the 30% housing guideline, 
so we should see the AI flag this."
```

#### 2.3 Show AI Analysis

When the analysis appears, explain:

```
"The AI analysis references my actual numbers. It says my rent is 34% 
of income and mentions this exceeds the R_HOUSING_COST guideline. 
Notice it is not giving generic advice. Every statement ties back to 
my specific budget data."
```

#### 2.4 Answer Quiz Questions

When quiz appears:

```
"The quiz questions are generated based on my data. This question asks 
about the percentage I spend on housing compared to the guideline.

Let me answer... The AI checks my response and gives feedback. It tells 
me whether I was correct, partially correct, or incorrect, and explains 
why. This creates an interactive learning experience."
```

#### 2.5 Show Personalized Tip

When tip appears:

```
"The tip section gives actionable advice. Notice at the bottom it says 
Based on R_SAVINGS_BENCHMARKS and R_HOUSING_COST. This is the grounding 
in action. Every tip must cite at least one financial rule."
```

### Part 3: Refusal Case (1 minute)

Run the demo again:

```bash
python demo.py
```

Enter 0 for income and 0 for all expenses. Explain:

```
"Now I will demonstrate what happens with insufficient data. I am 
entering zero for income and zero for all expenses.

The AI returns status Insufficient data. It does not try to generate 
advice because there is nothing meaningful to analyze. Instead, it 
gives a safe generic message asking for more information.

This refusal logic is critical. We never want the AI to hallucinate 
advice when it does not have real data to work with."
```

### Part 4: Wrap Up (30 seconds)

```
"To summarize what we built:

One, a grounded AI tutoring system that only uses actual user data.
Two, financial rules that the AI must cite for every tip.
Three, structured JSON output for predictable integration.
Four, refusal logic that prevents advice when data is insufficient.

This meets the Milestone 1 requirement of real AI integration with 
grounded tutoring logic. Thank you."
```

## Quick Reference

### Commands

```bash
cd backend
source venv/bin/activate
python demo.py
```

### Files to Show

| File | Purpose |
|------|---------|
| backend/src/ai_tutor.py | Main AI orchestration |
| backend/src/rule_engine.py | Loads and filters rules |
| backend/src/prompt_templates.py | Builds grounded prompt |
| backend/src/rules/financial_rules.json | Documented rules |

### 5 Things Video Must Demonstrate

1. User enters financial data
2. AI explanation references actual numbers
3. Quiz question based on user data
4. Tip cites financial rules
5. Refusal when data is missing

## Save Video

Save as `/docs/demo_video.mp4` or upload to YouTube/Google Drive and add link to README.md
