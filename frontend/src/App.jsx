import { useState } from 'react'
import Header from './components/Header'
import BudgetForm from './components/BudgetForm'
import BudgetResults from './components/BudgetResults'
import Toast from './components/Toast'
import { normalizeBudgetPayload } from './utils/budgetPayload'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [monthlyIncome, setMonthlyIncome] = useState(0)
  const [lastBudgetPayload, setLastBudgetPayload] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleBudgetSubmit = async (budgetData) => {
    setIsLoading(true)
    setError(null)
    const normalized = normalizeBudgetPayload(budgetData)
    setLastBudgetPayload(normalized)
    setMonthlyIncome(normalized.monthly_income || 0)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(normalized),
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.message || 'Failed to analyze budget')
      }

      const result = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(err.message)
      console.error('Budget analysis error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Header />

      <main className="mx-auto w-full max-w-3xl px-4 py-8 md:px-6 md:py-12">
        <header className="mb-8 md:mb-10">
          <div className="inline-flex items-center rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-4">
            Milestone 2 MVP
          </div>

          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight text-white mb-3">
            Budget check-in
          </h1>

          <p className="max-w-2xl text-sm md:text-base leading-7 text-slate-300">
            Enter your monthly income and expenses to generate a quiz-first budget analysis flow.
            After you submit your answer, the app will show the grader verdict, answer key,
            grounded explanation, and a financial tip.
          </p>
        </header>

        <section className="mb-6" id="budget">
          <BudgetForm
            onSubmit={handleBudgetSubmit}
            isLoading={isLoading}
            syncedBudget={lastBudgetPayload}
          />
        </section>

        {isLoading && (
          <div
            className="mb-6 flex items-center gap-3 rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-100"
            role="status"
            aria-live="polite"
          >
            <span
              className="inline-block h-4 w-4 rounded-full border-2 border-emerald-300 border-t-transparent animate-spin"
              aria-hidden="true"
            />
            Analyzing your budget...
          </div>
        )}

        <Toast
          message={error ? `Could not complete analysis: ${error}` : null}
          onDismiss={() => setError(null)}
        />

        {analysisResult && (
          <section className="mb-10 w-full min-w-0">
            <BudgetResults
              results={analysisResult}
              monthlyIncome={monthlyIncome}
              budgetPayload={lastBudgetPayload}
              onReanalyze={handleBudgetSubmit}
              isReanalyzing={isLoading}
            />
          </section>
        )}

        <footer className="pt-8 pb-4 text-center text-xs text-slate-400">
          Educational use only — not financial advice.
        </footer>
      </main>
    </div>
  )
}

export default App
