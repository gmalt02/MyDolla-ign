/**
 * Dismissible toast for API and network errors (demo-friendly).
 */
function Toast({ message, onDismiss, variant = 'error' }) {
  if (!message) return null

  const styles =
    variant === 'error'
      ? 'border-red-800/70 bg-red-950/95 text-red-50 shadow-lg shadow-black/40'
      : 'border-slate-600 bg-slate-900 text-slate-100 shadow-lg shadow-black/40'

  return (
    <div
      className="fixed bottom-4 left-1/2 z-[100] flex max-w-[min(92vw,28rem)] -translate-x-1/2"
      role="alert"
      aria-live="assertive"
    >
      <div
        className={`animate-toast-in flex w-full items-start gap-3 rounded-lg border px-4 py-3 text-sm ${styles}`}
      >
        <p className="flex-1 leading-snug pt-0.5">{message}</p>
        <button
          type="button"
          onClick={onDismiss}
          className="shrink-0 rounded-md px-2 py-1 text-lg leading-none text-red-200 hover:bg-red-900/50 hover:text-white"
          aria-label="Dismiss notification"
        >
          ×
        </button>
      </div>
    </div>
  )
}

export default Toast
