# My Dolla $ign

An AI powered budget education tool that teaches budgeting concepts in simple, easy to understand terms for young adults, students, and first time earners.

## Problem We Are Solving

Many people struggle to budget and save due to a lack of accessible, trustworthy financial guidance. Our platform provides educational budget breakdowns and personalized tips to help users build financial confidence.

## Team Members and Roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| Hugo | Frontend Lead | UI/UX, React components, form handling |
| Rene | Backend Lead | API development, data processing, server setup |
| Gauge | AI/ML Lead | AI integration, prompt engineering, budget analysis |
| Allison | Documentation and QA | PRD, testing, deployment, documentation |

## MVP Features

1. Budget Input Form: Categorized expense breakdown (income, rent, food, etc.)
2. AI Generated Analysis (Google Gemini):
   - Financial advice personalized to the user budget
   - Saving tips with actionable suggestions
   - Quiz questions to test understanding
   - Personalized tips based on financial rules
3. Results: Expense breakdown, key insights, and disclaimer

## Tech Stack

- Frontend: React.js with Tailwind CSS (Vite)
- Backend: Python (Flask) with REST API
- AI: Google Gemini API for budget analysis and tutoring
- Database: None for MVP (no persistence)

## Project Structure

```
MyDolla-Sign/
├── README.md
├── docs/
│   ├── PRD.md                    # Product Requirements Document
│   ├── SPIKE_PLAN.md             # Engineering Spike Plan
│   ├── prompt_design.md          # AI Prompt Design Documentation
│   ├── spike_results.md          # AI Integration Results
│   ├── evaluation_test_cases.md  # 20 Test Cases
│   ├── financial_rules.md        # Financial Rule Base
│   └── architecture.png          # System Architecture Diagram
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   └── App.jsx               # Main app entry
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── ai_tutor.py           # AI Tutor Core
│   │   ├── rule_engine.py        # Financial Rules Engine
│   │   ├── prompt_templates.py   # Prompt Builder
│   │   └── rules/
│   │       └── financial_rules.json
│   ├── demo.py                   # Interactive Demo Script
│   ├── test_tutor.py             # Test Script
│   ├── requirements.txt
│   └── main.py                   # Server entry point
└── CONTRIBUTING.md               # Team contribution guide
```

## How to Run

### Prerequisites
- Python 3.10 or higher (for backend)
- Node.js 18 or higher (for frontend)
- Google Gemini API key from https://aistudio.google.com/apikey

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your GEMINI_API_KEY
```

### Run the AI Tutor Demo (Terminal)
```bash
cd backend
source venv/bin/activate
python demo.py
```

This interactive demo will:
1. Collect your budget information
2. Analyze it using AI
3. Quiz you with 2 to 3 questions
4. Give you personalized tips
5. Let you ask the AI any questions

### Run the Backend Server
```bash
cd backend
source venv/bin/activate
python main.py
```

### Run the Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## Documentation

- [Product Requirements Document (PRD)](docs/PRD.md)
- [Engineering Spike Plan](docs/SPIKE_PLAN.md)
- [Prompt Design Documentation](docs/prompt_design.md)
- [Spike Results and AI Integration](docs/spike_results.md)
- [Evaluation Test Cases](docs/evaluation_test_cases.md)
- [Financial Rules](docs/financial_rules.md)

## Milestone 1 Deliverables

| Deliverable | Status |
|-------------|--------|
| PRD with AI Role | Complete |
| Financial Rule Base | Complete |
| AI Tutor Backend | Complete |
| Prompt Design Documentation | Complete |
| Evaluation Test Cases (20) | Complete |
| Spike Results | Complete |
| Architecture Diagram | Complete |

## Demo Video

Watch the AI Budget Tutor generate grounded financial advice.

https://youtu.be/G4ZdeZaZjmY

## License

This project is licensed under the Apache License 2.0.

Built for AI Ventures Club Spring 2026
