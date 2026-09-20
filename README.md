# AI spend & value monitor

**[Explore the monitor](https://devaharshagubbala07-hub.github.io/projects/ai-value/)** · [Findings](outputs/findings.md) · [Methodology](METHODOLOGY.md) · [Walkthrough](WALKTHROUGH.md)

A new business analytics project about a current question: **does an AI-assisted workflow deliver usable output at a cost the organization can justify?**

The [2026 State of FinOps report](https://data.finops.org/) identifies AI cost management and value measurement as priorities. This motivates the analysis. The project's workload, outcomes, model prices, fees, and time baselines are all **synthetic or illustrative**, developed with AI assistance. It is not a vendor benchmark, a real deployment result, or an employer project.

## What it analyzes

- Task-level AI costs including retry tokens and manual fallback.
- Recurring and setup fees, aggregated separately to prevent join duplication.
- Cost per usable AI-assisted task and first-pass acceptance.
- Human review/rework effort relative to an assumed manual baseline.
- A scenario model that separates freed capacity from realized economic benefit.
- Department/month filters, adjustable labor/realization/quality assumptions, and CSV export.

The fixture has 3,510 tasks across three fictional departments in June–August 2026. Seven tests and six reconciliations check analytical boundaries. No model API key, paid service, or third-party dependency is required.

## Run it

Python 3.11 or newer.

```bash
python analysis.py
python -m unittest discover -s tests -v
python -m http.server 8000
```

Visit `http://localhost:8000/dashboard/`. The pipeline recreates generated task rows in `data/generated/` (ignored by Git), fees in `data/fees.csv`, results in `outputs/`, and `dashboard/data.json`.

## Files to inspect

| File | Purpose |
|---|---|
| `assumptions.json` | Fictional prices, baseline effort, fees, months, and seed |
| `sql/task_summary.sql` | Task grain, outcomes, tokens, and human effort |
| `sql/fee_summary.sql` | Independent fee aggregation |
| `analysis.py` | Fixture generation, summaries, value model, and exports |
| `tests/test_analysis.py` | Fee duplication, fallback denominators, scope, and capacity/value boundaries |
| `outputs/findings.md` | Interpretation and the evidence needed for a real pilot |

At 0% realization, positive time savings do not become financial benefits. Negative capacity always remains additional modeled labor cost. The quality threshold is an explicit user assumption, not an industry standard. Infrastructure, maintenance, and other deployment costs would need to be added where relevant.
