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

function QuizFlow({
  phase,
  quizQuestion,
  answerDraft,
  setAnswerDraft,
  isGrading,
  submitForGrading,
  gradeResult,
  answerKey,
  explanation,
  savingPlanItems,
  groundedTip,
  groundedRuleCitation,
  onRevealResults,
  onBackToQuiz,
  SavingPlanComponent,
}) {
  if (phase === 'quiz' && quizQuestion) {
    return (
      <section aria-labelledby="quiz-heading" className="space-y-4 animate-fade-slide-in">
        <h3
          id="quiz-heading"
          className="text-xs font-semibold uppercase tracking-wide text-slate-500"
        >
          Quiz
        </h3>
        <p className="text-slate-800 leading-relaxed rounded-lg border border-emerald-100 bg-emerald-50/60 p-4">
          {quizQuestion}
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

        <button
          type="button"
          disabled={!answerDraft.trim() || isGrading}
          onClick={submitForGrading}
          className="w-full sm:w-auto bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-medium py-2.5 px-5 rounded-md transition-colors"
        >
          {isGrading ? 'Grading…' : 'Submit for grading'}
        </button>
      </section>
    )
  }

  if (phase === 'feedback' && gradeResult) {
    return (
      <div className="animate-fade-slide-in space-y-6">
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
          onClick={onRevealResults}
          className="w-full sm:w-auto bg-slate-800 hover:bg-slate-900 text-white font-medium py-2.5 px-5 rounded-md transition-colors"
        >
          Continue to explanation and tip
        </button>
      </div>
    )
  }

  if (phase === 'revealed') {
    return (
      <div className="animate-fade-slide-in space-y-6">
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

        <SavingPlanComponent savingPlanItems={savingPlanItems} />

        {groundedTip && (
          <section aria-labelledby="tip-heading">
            <h3
              id="tip-heading"
              className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2"
            >
              Financial tip (rule-grounded)
            </h3>
            <p className="text-slate-800 leading-relaxed border border-emerald-100 rounded-lg p-4 bg-emerald-50/60">
              {groundedTip}
            </p>

            {groundedRuleCitation && (
              <p className="text-xs text-slate-500 mt-2">
                Rule touchpoints: {groundedRuleCitation}
              </p>
            )}
          </section>
        )}

        {quizQuestion && (
          <button
            type="button"
            onClick={onBackToQuiz}
            className="text-sm text-emerald-700 hover:text-emerald-800 underline"
          >
            Back to quiz
          </button>
        )}
      </div>
    )
  }

  return null
}

export default QuizFlow