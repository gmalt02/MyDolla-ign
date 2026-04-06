import { useState } from 'react'
import Header from './components/Header'
import BudgetForm from './components/BudgetForm'
import BudgetResults from './components/BudgetResults'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [monthlyIncome, setMonthlyIncome] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleBudgetSubmit = async (budgetData) => {
    setIsLoading(true)
    setError(null)
    setMonthlyIncome(budgetData.monthly_income || 0)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(budgetData),
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
          <BudgetForm onSubmit={handleBudgetSubmit} isLoading={isLoading} />
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

        {error && (
          <div
            className="mb-6 rounded-lg border border-red-800/60 bg-red-950/40 px-4 py-3 text-sm text-red-100"
            role="alert"
          >
            <strong className="text-red-200">Could not complete analysis:</strong> {error}
          </div>
        )}

        {analysisResult && !isLoading && (
          <section className="mb-10">
            <BudgetResults results={analysisResult} monthlyIncome={monthlyIncome} />
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
