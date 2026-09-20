# Explain the business case

This project was built with AI assistance. Run it, read the SQL, and modify an assumption before discussing it in an interview.

1. **Frame the current problem.** A low cost per token does not answer whether a business workflow is worthwhile.
2. **Explain the grain.** A task can have retries, but it still counts as one attempted task. All its token costs remain included.
3. **Show the denominator choice.** Cost per usable task includes accepted and reworked tasks. Manual fallback contributes cost but is excluded from usable AI output.
4. **Find the fee-join trap.** Explain why monthly fees are aggregated separately rather than repeated for every task.
5. **Move realization to 0%.** Explain why freed capacity creates no modeled financial benefit under that assumption, while technology cost remains.
6. **Change the quality threshold.** A positive value scenario can coexist with a failed acceptance threshold. A rollout decision needs both quality and value evidence.
7. **Name the evidence you would collect.** Actual billing, task complexity, manual effort, independent outcome reviews, maintenance costs, and how the freed capacity will be used.

Practice change: add a realistic maintenance-fee assumption as a separate monthly cost. Update the pipeline, the dashboard disclosure, and the reconciliation. Do not describe the new output as measured savings.
