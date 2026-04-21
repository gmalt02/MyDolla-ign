import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

// High-contrast, color-blind friendly-ish palette centered on dark greens
const COLORS = [
  '#065f46', // emerald-800
  '#047857', // emerald-700
  '#0f766e', // teal-700
  '#0ea5e9', // sky-500
  '#f97316', // orange-500
  '#e11d48', // rose-600
  '#7c3aed', // violet-600
]

const RADIAN = Math.PI / 180

const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}) => {
  // Move label a little closer to the center of the slice
  // so it looks more visually centered and avoids edge crowding.
  const radius = innerRadius + (outerRadius - innerRadius) * 0.42
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)

  // Hide tiny labels so they do not overlap or look awkward
  if (percent < 0.06) return null

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor="middle"
      dominantBaseline="middle"
      className="text-xs font-semibold"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

function ExpensePieChart({ breakdown, monthlyIncome }) {
  if (!breakdown || breakdown.length === 0 || monthlyIncome === 0) {
    return null
  }

  const chartData = breakdown
    .filter((item) => item.amount > 0)
    .map((item, index) => ({
      name: item.category,
      value: item.amount,
      percentage: item.percentage,
      color: COLORS[index % COLORS.length],
    }))

  if (chartData.length === 0) return null

  const chartSummary = chartData
    .map(
      (item) =>
        `${item.name}: $${item.value.toFixed(2)} (${item.percentage.toFixed(1)}% of income)`
    )
    .join('. ')

  return (
    <div
      className="w-full"
      role="img"
      aria-label={`Expense breakdown pie chart. ${chartSummary}`}
    >
      <p className="sr-only">
        Expense breakdown by category. {chartSummary}
      </p>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            animationBegin={0}
            animationDuration={800}
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.color}
                stroke="#0f172a"
                strokeWidth={1}
              />
            ))}
          </Pie>

          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0]
                return (
                  <div className="bg-white p-3 rounded-lg shadow-lg border border-slate-200">
                    <p className="font-semibold text-slate-800">{data.name}</p>
                    <p className="text-emerald-600 font-medium">
                      ${data.value.toFixed(2)}
                    </p>
                    <p className="text-slate-500 text-sm">
                      {data.payload.percentage.toFixed(1)}% of income
                    </p>
                  </div>
                )
              }
              return null
            }}
          />

          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value) => (
              <span className="text-slate-700 text-sm font-medium">
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export default ExpensePieChart