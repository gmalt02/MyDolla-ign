/**
 * ============================================
 * ASSIGNED TO: Member 1 (Frontend Lead) & Member 3 (AI/ML Lead)
 * 
 * Investment Glossary Component
 * 
 * TODO (Member 1):
 * 1. Make the glossary searchable
 * 2. Add expand/collapse functionality for definitions
 * 3. Improve styling and readability
 * 
 * TODO (Member 3):
 * 1. Review and improve the definitions
 * 2. Add more terms as needed
 * 3. Consider AI-generated explanations for complex terms
 * ============================================
 */

import { useState } from 'react'
import Toast from './Toast'

function GlossaryAIInput({ term, onExplain, isLoading, customPrompt }) {
  const [showInput, setShowInput] = useState(false)
  const [prompt, setPrompt] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (prompt.trim()) {
      onExplain(term, prompt.trim())
      setShowInput(false)
      setPrompt('')
    } else {
      onExplain(term)
    }
  }

  return (
    <div className="space-y-2">
      {!showInput ? (
        <button
          type="button"
          onClick={() => setShowInput(true)}
          disabled={isLoading}
          className="text-xs inline-flex items-center px-3 py-1.5 rounded-full border border-emerald-500 text-emerald-700 hover:bg-emerald-50 disabled:opacity-60"
        >
          {isLoading ? 'Asking AI…' : 'Ask AI to explain'}
        </button>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Explain in simpler terms, How does this relate to budgeting?"
            className="w-full px-3 py-1.5 text-xs border border-emerald-300 rounded-lg focus:border-emerald-500 focus:ring-1 focus:ring-emerald-200 outline-none text-gray-900 placeholder:text-gray-400"
            autoFocus
          />
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={isLoading}
              className="px-3 py-1 text-xs bg-emerald-600 text-white rounded-md hover:bg-emerald-700 disabled:opacity-50"
            >
              {isLoading ? 'Asking…' : 'Ask'}
            </button>
            <button
              type="button"
              onClick={() => {
                setShowInput(false)
                setPrompt('')
              }}
              className="px-3 py-1 text-xs bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  )
}

// Financial terms glossary data
// TODO (Member 3): Review and expand this list
const GLOSSARY_TERMS = [
  {
    term: 'Budget',
    definition: 'A plan that helps you track your income and expenses over a specific period (usually monthly). It shows where your money comes from and where it goes.',
    example: 'If you earn $3,000/month and plan to spend $1,000 on rent, $400 on food, etc., that plan is your budget.'
  },
  {
    term: 'Stock',
    definition: 'A share of ownership in a company. When you buy stock, you own a tiny piece of that company and may benefit if the company grows in value.',
    example: 'Buying 1 share of Apple stock means you own a very small piece of Apple Inc.'
  },
  {
    term: 'ETF (Exchange-Traded Fund)',
    definition: 'A basket of multiple stocks or bonds that you can buy as a single investment. ETFs help you diversify without buying many individual stocks.',
    example: 'An S&P 500 ETF holds shares of 500 large U.S. companies, so buying one share gives you exposure to all of them.'
  },
  {
    term: 'Bond',
    definition: 'A loan you give to a company or government in exchange for regular interest payments. Bonds are generally considered safer than stocks.',
    example: 'A U.S. Treasury Bond means you\'re lending money to the government, and they pay you interest over time.'
  },
  {
    term: 'Risk',
    definition: 'The possibility of losing some or all of your investment. Higher risk investments might offer higher returns, but also higher potential for loss.',
    example: 'Stocks are riskier than savings accounts because their value can go up or down significantly.'
  },
  {
    term: 'Diversification',
    definition: 'Spreading your investments across different types of assets to reduce risk. "Don\'t put all your eggs in one basket."',
    example: 'Instead of buying only tech stocks, you might also invest in healthcare, real estate, and bonds.'
  },
  {
    term: 'Compound Interest',
    definition: 'Interest earned on both your original money AND the interest that has already been added. This makes your money grow faster over time.',
    example: 'If you invest $1,000 at 5% interest, after year 1 you have $1,050. In year 2, you earn 5% on $1,050, not just $1,000.'
  },
  {
    term: 'Emergency Fund',
    definition: 'Money set aside for unexpected expenses like medical bills, car repairs, or job loss. Experts recommend saving 3-6 months of living expenses.',
    example: 'If your monthly expenses are $2,000, aim to save $6,000-$12,000 in an easily accessible account.'
  },
  {
    term: '50/30/20 Rule',
    definition: 'A simple budgeting guideline: 50% of income for needs (rent, food), 30% for wants (entertainment), and 20% for savings and debt repayment.',
    example: 'With a $3,000 income: $1,500 for needs, $900 for wants, $600 for savings.'
  },
  {
    term: 'Inflation',
    definition: 'The gradual increase in prices over time, which means your money buys less in the future than it does today.',
    example: 'If inflation is 3%, something that costs $100 today might cost $103 next year.'
  },
]

function InvestmentGlossary() {
  const [expandedTerm, setExpandedTerm] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [loadingTerm, setLoadingTerm] = useState(null)
  const [aiExplanations, setAiExplanations] = useState({})
  const [customPrompts, setCustomPrompts] = useState({})
  const [error, setError] = useState(null)

  // Filter terms based on search query
  const filteredTerms = GLOSSARY_TERMS.filter(item =>
    item.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.definition.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const toggleTerm = (term) => {
    setExpandedTerm(expandedTerm === term ? null : term)
  }

  const fetchAiExplanation = async (term, customPrompt = null) => {
    try {
      setLoadingTerm(term)
      setError(null)
      
      // Build the request - if custom prompt, send it as part of the term explanation request
      const requestBody = { term, complexity: 'beginner' }
      if (customPrompt) {
        requestBody.custom_prompt = customPrompt
      }
      
      const response = await fetch('/api/glossary/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Failed to fetch AI explanation')
      }
      setAiExplanations((prev) => ({ ...prev, [term]: data.explanation }))
      if (customPrompt) {
        setCustomPrompts((prev) => ({ ...prev, [term]: customPrompt }))
      }
    } catch (err) {
      console.error('Glossary AI error:', err)
      setError(err.message)
    } finally {
      setLoadingTerm(null)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 md:p-8 relative" id="glossary">
      <Toast message={error} onDismiss={() => setError(null)} />
      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        Investment Literacy Glossary
      </h2>
      <p className="text-gray-600 mb-2">
        Learn essential financial terms in simple, easy-to-understand language.
      </p>
      {/* Search Bar */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search terms..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-gray-200 rounded-lg 
                     focus:border-green-500 focus:ring-1 focus:ring-green-200 
                     transition-colors outline-none text-gray-900 placeholder:text-gray-400"
        />
      </div>

      {/* Glossary Terms */}
      <div className="space-y-3">
        {filteredTerms.map((item) => (
          <div 
            key={item.term}
            className="border border-gray-200 rounded-lg overflow-hidden"
          >
            <button
              onClick={() => toggleTerm(item.term)}
              className="w-full px-4 py-3 text-left flex justify-between items-center
                         hover:bg-gray-50 transition-colors"
            >
              <span className="font-semibold text-gray-800">{item.term}</span>
              <span className="text-gray-400 text-xl">
                {expandedTerm === item.term ? '-' : '+'}
              </span>
            </button>
            
            {expandedTerm === item.term && (
              <div className="px-4 pb-4 bg-gray-50 space-y-3">
                <p className="text-gray-700">
                  {item.definition}
                </p>
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-sm text-gray-600">
                    <strong>Example:</strong> {item.example}
                  </p>
                </div>
                <div className="pt-2 border-t border-gray-200 space-y-2">
                  <GlossaryAIInput
                    term={item.term}
                    onExplain={fetchAiExplanation}
                    isLoading={loadingTerm === item.term}
                    customPrompt={customPrompts[item.term]}
                  />
                  {aiExplanations[item.term] && (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
                      <p className="text-xs font-semibold text-emerald-700 mb-1">
                        AI explanation
                        {customPrompts[item.term] && (
                          <span className="text-emerald-600 font-normal ml-2">
                            ({customPrompts[item.term]})
                          </span>
                        )}
                      </p>
                      <p className="text-sm text-emerald-900 whitespace-pre-line">
                        {aiExplanations[item.term]}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {filteredTerms.length === 0 && (
        <p className="text-center text-gray-500 py-8">
          No terms found matching "{searchQuery}"
        </p>
      )}

      {/* Educational Note */}
      <div className="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
        <p className="text-sm text-yellow-800">
          <strong>Note:</strong> This glossary is for educational purposes. 
          Before making any investment decisions, consider consulting with a 
          qualified financial advisor.
        </p>
      </div>
    </div>
  )
}

export default InvestmentGlossary
