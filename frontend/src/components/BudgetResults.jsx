import { useState, useEffect } from 'react'
import WhatIfPanel from './WhatIfPanel'

function verdictStyles(verdict) {
  const v = (verdict || '').toUpperCase()
  if (v === 'CORRECT') {
    return 'border-emerald-200 bg-emerald-50/80'
  }
  if (v === 'INCORRECT') {
    return 'border-red-200 bg-red-50/80'
  }
  return 'border-amber-200 bg-amber-50/70'
}

function BudgetResults({ results, monthlyIncome, budgetPayload, onReanalyze, isReanalyzing }) {
  const [phase, setPhase] = useState('quiz')
  const [answerDraft, setAnswerDraft] = useState('')
  const [gradeResult, setGradeResult] = useState(null)
  const [gradeError, setGradeError] = useState(null)
  const [isGrading, setIsGrading] = useState(false)

  useEffect(() => {
    setPhase('quiz')
    setAnswerDraft('')
    setGradeResult(null)
    setGradeError(null)
    setIsGrading(false)
  }, [results])

  if (!results) return null

  const {
    financial_advice,
    analysis,
    quiz_question,
    quiz_answer_key,
    grounded_tip,
    grounded_rule_citation,
    breakdown,
    goal,
    output_source,
    saving_plan,
  } = results

  const explanation = financial_advice || analysis

  const savingPlanItems =
    Array.isArray(saving_plan) && saving_plan.length > 0
      ? saving_plan
      : [
          'Month 1: Set aside a fixed amount from each paycheck.',
          'Month 2: Reduce one flexible category and move that money to savings.',
          'Month 3: Build toward an emergency fund and review progress.',
        ]

  const income = monthlyIncome || 0

  const goalLabels = {
    general: 'General financial wellness',
    emergency_fund: 'Build emergency fund',
    debt_payoff: 'Pay down debt',
    big_purchase: 'Save for a big purchase',
  }

  const sourceLabel =
    output_source === 'google_ai_studio'
      ? 'AI (Google AI Studio)'
      : output_source === 'vertex_ai'
        ? 'AI (Vertex Gemini)'
        : output_source === 'fallback_deterministic'
          ? 'Deterministic fallback (no AI call)'
          : output_source === 'demo_static'
            ? 'Static demo payload'
            : output_source || 'Unknown'

  const answerKey =
    quiz_answer_key ||
    'Strong answers tie back to your actual income and category amounts and to the rules in financial_rules.md.'

  const stepLine =
    phase === 'quiz'
      ? 'Step 1 of 3 — answer the quiz before viewing the full explanation and tip.'
      : phase === 'feedback'
        ? 'Step 2 of 3 — review your grade, feedback, and answer key.'
        : 'Step 3 of 3 — review the grounded explanation and financial tip.'

  const submitForGrading = async () => {
    const trimmed = answerDraft.trim()
    if (!trimmed || !quiz_question) return

    setGradeError(null)
    setIsGrading(true)

    try {
      const response = await fetch('/api/grade-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quiz_question,
          quiz_answer_key: quiz_answer_key || '',
          user_answer: trimmed,
        }),
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        throw new Error(data.message || 'Grading request failed')
      }

      setGradeResult({
        verdict: data.verdict || 'PARTIALLY CORRECT',
        feedback: data.feedback || '',
        output_source: data.output_source,
      })
      setPhase('feedback')
    } catch (err) {
      setGradeError(err.message || 'Something went wrong while grading.')
    } finally {
      setIsGrading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
      <div className="border-b border-slate-200 bg-slate-50 px-5 py-4">
        <h2 className="text-lg font-semibold text-slate-900">Analysis results</h2>
        <p className="text-sm text-slate-600 mt-1">
          Output source: <span className="font-medium text-slate-800">{sourceLabel}</span>
          {goal && (
            <span className="text-slate-500">
              {' '}
              · Goal: {goalLabels[goal] || goal}
            </span>
          )}
        </p>
        <p className="text-xs text-slate-500 mt-2">{stepLine}</p>
      </div>

      <div className="p-5 md:p-6 space-y-6">
        {budgetPayload && onReanalyze && (
          <WhatIfPanel
            budgetPayload={budgetPayload}
            onReanalyze={onReanalyze}
            isLoading={Boolean(isReanalyzing)}
          />
        )}

        {breakdown && breakdown.length > 0 && income > 0 && (
          <section aria-labelledby="breakdown-heading">
            <h3
              id="breakdown-heading"
              className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-3"
            >
              Your categories (from your inputs)
            </h3>
            <ul className="space-y-2">
              {breakdown.map((item, i) => (
                <li
                  key={i}
                  className="flex justify-between text-sm text-slate-700 border-b border-slate-100 pb-2 last:border-0"
                >
                  <span>{item.category}</span>
                  <span className="tabular-nums text-slate-600">
                    ${Number(item.amount).toFixed(2)} ({Number(item.percentage).toFixed(1)}%)
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {phase === 'quiz' && quiz_question && (
          <section aria-labelledby="quiz-heading" className="space-y-4">
            <h3
              id="quiz-heading"
              className="text-xs font-semibold uppercase tracking-wide text-slate-500"
            >
              Quiz
            </h3>
            <p className="text-slate-800 leading-relaxed rounded-lg border border-emerald-100 bg-emerald-50/60 p-4">
              {quiz_question}
            </p>

            <div>
              <label htmlFor="quiz-answer" className="block text-sm font-medium text-slate-700 mb-1">
                Your answer
              </label>
              <textarea
                id="quiz-answer"
                value={answerDraft}
                onChange={(e) => setAnswerDraft(e.target.value)}
                rows={4}
                disabled={isGrading}
                placeholder="Write a short answer. It will be graded before you see the tutor explanation and tip."
                className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm text-slate-900 focus:border-emerald-600 focus:ring-1 focus:ring-emerald-500/30 outline-none resize-y disabled:bg-slate-100 disabled:text-slate-500"
              />
            </div>

            {gradeError && (
              <p className="text-sm text-red-700" role="alert">
                {gradeError}
              </p>
            )}

            <button
              type="button"
              disabled={!answerDraft.trim() || isGrading}
              onClick={submitForGrading}
              className="w-full sm:w-auto bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-medium py-2.5 px-5 rounded-md transition-colors"
            >
              {isGrading ? 'Grading…' : 'Submit for grading'}
            </button>
          </section>
        )}

        {phase === 'feedback' && gradeResult && (
          <>
            <section aria-labelledby="verdict-heading" className="space-y-3">
              <h3
                id="verdict-heading"
                className="text-xs font-semibold uppercase tracking-wide text-slate-500"
              >
                Grader result
              </h3>

              <div className={`rounded-lg border p-4 ${verdictStyles(gradeResult.verdict)}`}>
                <p className="text-sm font-semibold text-slate-900">
                  Verdict: {gradeResult.verdict}
                </p>

                {gradeResult.output_source && (
                  <p className="text-xs text-slate-600 mt-1">
                    Grader source: {gradeResult.output_source}
                  </p>
                )}

                <p className="text-sm text-slate-800 mt-3 leading-relaxed whitespace-pre-wrap">
                  {gradeResult.feedback}
                </p>
              </div>
            </section>

            <section aria-labelledby="your-answer-heading">
              <h3
                id="your-answer-heading"
                className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
              >
                What you submitted
              </h3>
              <p className="text-slate-800 border border-slate-200 rounded-lg p-4 bg-slate-50/80 whitespace-pre-wrap">
                {answerDraft.trim()}
              </p>
            </section>

            <section aria-labelledby="answer-key-heading">
              <h3
                id="answer-key-heading"
                className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
              >
                Answer key (core ideas)
              </h3>
              <p className="text-slate-800 leading-relaxed border border-amber-100 rounded-lg p-4 bg-amber-50/50">
                {answerKey}
              </p>
            </section>

            <button
              type="button"
              onClick={() => setPhase('revealed')}
              className="w-full sm:w-auto bg-slate-800 hover:bg-slate-900 text-white font-medium py-2.5 px-5 rounded-md transition-colors"
            >
              Continue to explanation and tip
            </button>
          </>
        )}

        {phase === 'revealed' && (
          <>
            {explanation && (
              <section aria-labelledby="explanation-heading">
                <h3
                  id="explanation-heading"
                  className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
                >
                  Grounded explanation
                </h3>
                <p className="text-slate-800 leading-relaxed border border-slate-100 rounded-lg p-4 bg-slate-50/80">
                  {explanation}
                </p>
              </section>
            )}

            {savingPlanItems.length > 0 && (
              <section aria-labelledby="saving-plan-heading">
                <h3
                  id="saving-plan-heading"
                  className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
                >
                  Saving plan
                </h3>

                <div className="border border-blue-100 rounded-lg p-4 bg-blue-50/50 space-y-3">
                  {savingPlanItems.map((step, index) => (
                    <div key={index} className="flex gap-3">
                      <div className="flex flex-col items-center">
                        <div className="w-7 h-7 rounded-full bg-blue-600 text-white text-xs font-semibold flex items-center justify-center">
                          {index + 1}
                        </div>
                        {index !== savingPlanItems.length - 1 && (
                          <div className="w-px flex-1 bg-blue-200 mt-2" />
                        )}
                      </div>

                      <p className="text-slate-800 leading-relaxed pt-1">
                        {typeof step === 'string' ? step : JSON.stringify(step)}
                      </p>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {grounded_tip && (
              <section aria-labelledby="tip-heading">
                <h3
                  id="tip-heading"
                  className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
                >
                  Financial tip (rule-grounded)
                </h3>
                <p className="text-slate-800 leading-relaxed border border-emerald-100 rounded-lg p-4 bg-emerald-50/60">
                  {grounded_tip}
                </p>

                {grounded_rule_citation && (
                  <p className="text-xs text-slate-500 mt-2">
                    Rule touchpoints: {grounded_rule_citation}
                  </p>
                )}
              </section>
            )}

            {quiz_question && (
              <button
                type="button"
                onClick={() => {
                  setPhase('quiz')
                  setGradeResult(null)
                  setGradeError(null)
                }}
                className="text-sm text-emerald-700 hover:text-emerald-800 underline"
              >
                Back to quiz
              </button>
            )}
          </>
        )}

        <p className="text-xs text-slate-500 border-t border-slate-100 pt-4">
          <strong className="text-slate-600">Disclaimer:</strong> This tool is for educational
          purposes only and does not constitute financial advice. Consult a qualified professional
          for your situation.
        </p>
      </div>
    </div>
  )
}

export default BudgetResults