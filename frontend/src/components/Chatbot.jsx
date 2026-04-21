import { useState } from 'react'
import Toast from './Toast'

function Chatbot({ context }) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState(null)

  const handleSend = async (e) => {
    e?.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input.trim() }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsSending(true)
    setError(null)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          context,
        }),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Chatbot request failed')
      }
      const botMessage = { role: 'assistant', content: data.reply }
      setMessages((prev) => [...prev, botMessage])
    } catch (err) {
      console.error('Chatbot error:', err)
      setError(err.message)
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div className="fixed bottom-4 right-4 z-40">
      <Toast message={error} onDismiss={() => setError(null)} />
      {/* Toggle button */}
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="rounded-full bg-emerald-600 text-white shadow-lg shadow-emerald-500/40 w-14 h-14 flex items-center justify-center text-xl hover:bg-emerald-700 transition-colors"
          aria-label="Open budgeting chatbot"
        >
          💬
        </button>
      )}

      {isOpen && (
        <div className="w-80 sm:w-96 h-96 bg-slate-950/95 border border-emerald-700 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          <div className="px-4 py-3 bg-gradient-to-r from-emerald-800 to-emerald-900 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-emerald-50">DollaBot</p>
              <p className="text-xs text-emerald-200">
                AI budgeting coach (education only)
              </p>
            </div>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="text-emerald-100 hover:text-emerald-300 text-lg leading-none"
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>

          <div className="flex-1 px-3 py-2 overflow-y-auto space-y-2 text-sm bg-gradient-to-b from-slate-900 to-slate-950">
            {messages.length === 0 && (
              <div className="text-xs text-slate-400 mt-2">
                Ask me things like:
                <ul className="list-disc list-inside mt-1 space-y-0.5">
                  <li>“How can I save more each month?”</li>
                  <li>“What is an emergency fund?”</li>
                  <li>“How do I use the 50/30/20 rule?”</li>
                </ul>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-3 py-2 ${
                    msg.role === 'user'
                      ? 'bg-emerald-600 text-white rounded-br-sm'
                      : 'bg-slate-800 text-slate-100 rounded-bl-sm border border-emerald-700/40'
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>
                </div>
              </div>
            ))}
            {isSending && (
              <p className="text-xs text-slate-400">DollaBot is thinking…</p>
            )}
          </div>

          <form
            onSubmit={handleSend}
            className="border-t border-slate-800 bg-slate-900 px-3 py-2 flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a budgeting question…"
              className="flex-1 bg-slate-800 text-white text-sm px-3 py-2 rounded-full border border-slate-700 focus:border-emerald-500 focus:outline-none placeholder:text-slate-400"
            />
            <button
              type="submit"
              disabled={isSending || !input.trim()}
              className="px-3 py-2 rounded-full bg-emerald-600 text-white text-xs font-medium disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  )
}

export default Chatbot

