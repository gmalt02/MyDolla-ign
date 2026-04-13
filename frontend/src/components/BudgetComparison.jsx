function BudgetComparison({ breakdown, monthlyIncome }) {
  if (!breakdown || monthlyIncome === 0) return null

  // Categorize expenses into Needs, Wants, Savings
  const needsCategories = ['rent', 'utilities', 'food', 'transportation']
  const wantsCategories = ['entertainment', 'other']
  const savingsCategories = ['savings']

  const needs = breakdown
    .filter((item) =>
      needsCategories.some((cat) =>
        item.category.toLowerCase().includes(cat)
      )
    )
    .reduce((sum, item) => sum + item.amount, 0)

  const wants = breakdown
    .filter((item) =>
      wantsCategories.some((cat) =>
        item.category.toLowerCase().includes(cat)
      )
    )
    .reduce((sum, item) => sum + item.amount, 0)

  const savings = breakdown
    .filter((item) =>
      savingsCategories.some((cat) =>
        item.category.toLowerCase().includes(cat)
      )
    )
    .reduce((sum, item) => sum + item.amount, 0)

  const needsPct = (needs / monthlyIncome) * 100
  const wantsPct = (wants / monthlyIncome) * 100
  const savingsPct = (savings / monthlyIncome) * 100

  const categories = [
    {
      name: 'Needs',
      current: needsPct,
      target: 50,
      amount: needs,
      color: 'emerald',
      description: 'Rent, utilities, food, transportation',
    },
    {
      name: 'Wants',
      current: wantsPct,
      target: 30,
      amount: wants,
      color: 'teal',
      description: 'Entertainment, dining out, hobbies',
    },
    {
      name: 'Savings',
      current: savingsPct,
      target: 20,
      amount: savings,
      color: 'blue',
      description: 'Emergency fund, future goals',
    },
  ]

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1">
        <h3 className="text-sm font-semibold text-slate-700">
          50/30/20 Rule Comparison
        </h3>
        <span className="text-xs text-slate-500">Target vs Your Budget</span>
      </div>
      {categories.map((cat) => {
        const isOver = cat.current > cat.target
        const isUnder = cat.current < cat.target * 0.8
        const colorClasses = {
          emerald: {
            bg: 'bg-emerald-100',
            bar: 'bg-emerald-500',
            text: 'text-emerald-700',
          },
          teal: {
            bg: 'bg-teal-100',
            bar: 'bg-teal-500',
            text: 'text-teal-700',
          },
          blue: {
            bg: 'bg-blue-100',
            bar: 'bg-blue-500',
            text: 'text-blue-700',
          },
        }
        const colors = colorClasses[cat.color]

        return (
          <div key={cat.name} className="space-y-1">
            <div className="flex justify-between items-center text-sm">
              <div className="flex items-center gap-2">
                <span className={`font-medium ${colors.text}`}>
                  {cat.name}
                </span>
                {isOver && (
                  <span className="text-xs text-red-600 font-medium">
                    Higher than target
                  </span>
                )}
                {isUnder && (
                  <span className="text-xs text-amber-600 font-medium">
                    Lower than target
                  </span>
                )}
              </div>
              <div className="text-right">
                <span className={`font-semibold ${colors.text}`}>
                  {cat.current.toFixed(1)}%
                </span>
                <span className="text-slate-400 text-xs ml-1">
                  / {cat.target}%
                </span>
              </div>
            </div>
            <div className="relative">
              {/* Target line */}
              <div
                className="absolute h-full w-0.5 bg-slate-300 z-10"
                style={{ left: `${cat.target}%` }}
              />
              {/* Current progress */}
              <div className={`h-3 ${colors.bg} rounded-full overflow-hidden`}>
                <div
                  className={`h-full ${colors.bar} transition-all duration-700 ease-out rounded-full`}
                  style={{ width: `${Math.min(cat.current, 100)}%` }}
                />
              </div>
            </div>
            <p className="text-xs text-slate-500">{cat.description}</p>
          </div>
        )
      })}
    </div>
  )
}

export default BudgetComparison
