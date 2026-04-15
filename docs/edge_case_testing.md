1. Zero Income

Input:
Monthly income = $0, with various expenses entered

Observations:

The application did not crash and still returned analysis results.
The expense pie chart did not render, which is expected since percentages cannot be calculated without income.

Conclusion:
The system handles zero-income scenarios correctly by preventing invalid visualizations while still providing meaningful feedback.

2. Expenses Greater Than Income

Input:
Monthly income = $2000, total expenses exceed $2000

Observations:

The application successfully generated analysis results.
The pie chart rendered correctly and displayed the expense distribution.
The system identified and reflected overspending behavior in the analysis.

Conclusion:
The system correctly handles overspending scenarios and continues to provide accurate feedback and visualizations.

3. Single Expense Category

Input:
Monthly income = $3000, only one category (e.g., rent) has a value

Observations:

The pie chart rendered with a single segment.
No UI errors or crashes occurred.

Conclusion:
The system supports minimal input cases and maintains correct visualization behavior.

4. Extreme Values

Input:
Monthly income = $100,000 with very large expense values

Observations:

The application handled large values without crashing.
Number formatting remained readable and consistent.
The pie chart rendered correctly.

Conclusion:
The system is stable under extreme numeric inputs and maintains usability and formatting.

Overall Assessment

The My Dolla $ign application demonstrates strong stability and reliability across multiple edge cases. The system continues to provide meaningful analysis and maintains correct UI behavior even when given unusual or extreme inputs.

Minor Issues Identified
Pie chart percentage labels may appear slightly misaligned within segments.
Minor UI adjustments could improve label positioning and readability.