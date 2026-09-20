# Methodology and assumptions

## Grain and provenance

One generated row represents one business task, not one model call. All retry input/output tokens are included in that row. Each task uses one fictional model rate and has one terminal outcome: accepted first pass, accepted after rework, or manual fallback. The generator deliberately varies workflow mix by department. It cannot support causal comparisons between models or departments.

All records are simulated. Prices and fees in `assumptions.json` are project assumptions, not scraped vendor quotes. A fixed seed recreates the workload. Human effort and manual baselines are generated, not experimentally measured.

## Cost model

Model rates are whole dollars per million tokens, numerically equal to microdollars per token. Multiplying integer token counts by these rates preserves exact microdollar API charges. Selected technology cost is all task API cost plus selected department-month recurring fees and one-time setup fees. Setup occurs in June only. Fees are summed in a separate SQL query and never joined onto task-level rows.

| Measure | Definition |
|---|---|
| First-pass acceptance | Accepted first-pass tasks / all attempted business tasks |
| Usable AI-assisted tasks | Accepted first pass + accepted after rework |
| Cost / usable task | All selected technology cost / usable AI-assisted tasks |
| Net capacity minutes | Sum of assumed manual baseline minutes − sum of human effort with AI |
| Human effort | Review + applicable rework or manual fallback effort |

Fallback and retry costs remain in the numerator. A zero usable-task denominator yields missing unit cost, not zero. Fees remain visible in a scope even when it has no task rows.

## Value scenario

Let H be net capacity hours, W the assumed labor value/hour, R the realization fraction, and T technology cost.

- Potential capacity value V = H × W.
- Modeled benefit B = max(V, 0) × R + min(V, 0).
- Modeled net value = B − T.
- Modeled return on technology cost = (B − T) / T, when T is positive.
- Break-even realization = T / V, when V is positive. A result above 100% is unattainable under the current assumptions.

Positive capacity needs a realization assumption. Additional labor is always treated as an economic cost. The model does not assume a payroll reduction or prove a causal financial return. The dashboard starts at $45/hour and 25% realization solely as editable scenario inputs.

The chosen first-pass threshold is displayed independently. Passing it does not establish safety, accuracy on unseen tasks, or readiness for deployment. The fixture's acceptance labels are generated. A real pilot needs independent evaluation, comparable manual baselines, invoice reconciliation, and later-period validation.

## Reconciliation and limitations

Checks cover unique task IDs, terminal outcomes, cost totals across time and departments, repricing from tokens, and fees counted once. Tests target the consequences of mistakes: inflated fixed fees, discarded fallback costs, wrong zero-denominator handling, false cash-savings claims, and discounted extra labor.

The model omits infrastructure, ongoing maintenance, training, risk losses, and integration costs beyond the declared setup fees. Add relevant costs before making a real business decision. No staffing, clinical, or vendor recommendation is produced.
