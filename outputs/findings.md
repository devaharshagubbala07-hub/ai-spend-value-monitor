# Findings from the example workload

All usage, outcomes, prices, fees, and time baselines are simulated. This AI-assisted portfolio example evaluates measurement choices, not a real vendor or deployment.

## What the fixture shows

- 3,510 business tasks; 75.1% accepted without rework.
- $2,057.61 in modeled technology cost, comprising API usage, recurring fees, and one-time setup fees.
- $0.63 per usable AI-assisted task. All attempted tasks contribute cost; the denominator includes accepted and reworked tasks, and excludes manual fallback.
- 631.9 net hours relative to the assumed manual baseline, after review, rework, and manual fallback. These hours are simulated capacity, not observed savings.
- At an assumed $45/hour, 7.2% of that capacity value would need to become an economic benefit to cover the modeled technology cost. Whether this is achievable is unknown.

## What a decision-maker should ask

Choose a quality threshold before judging value. Include retry usage and failed attempts in costs; count monthly fees once. Separate time freed from money saved. At 0% realization, positive capacity creates no modeled financial benefit. Negative capacity is always treated as additional labor cost. Compare departments within their workflow context; workload mix prevents causal model comparisons.

## Evidence needed before a real rollout decision

Replace the generated workload with authorized task and billing logs. Measure manual baselines and human review effort on comparable work, use independently reviewed outcome labels, reconcile invoices, and test results on a later time period. Add infrastructure, integration, security review, and ongoing maintenance costs where applicable. This prototype does not automate staffing or vendor decisions.

## Why this is a current question

The [2026 State of FinOps report](https://data.finops.org/) identifies AI cost management and business-value measurement as priorities. It motivates the question; it does not provide the simulated outcomes or fictional model prices in this repository.
