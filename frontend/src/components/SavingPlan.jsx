function SavingPlan({ savingPlanItems }) {
  if (!savingPlanItems || savingPlanItems.length === 0) return null

  return (
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
  )
}

export default SavingPlan