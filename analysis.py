"""AI unit economics and capacity scenarios; deterministic example, no API calls."""
from pathlib import Path
import calendar
import csv
import json
import random
import sqlite3

ROOT=Path(__file__).resolve().parent

def generate(config):
    rng=random.Random(config['seed']);tasks=[];fees=[]
    for month_index,month in enumerate(config['months']):
        for department_index,(department,settings) in enumerate(config['departments'].items()):
            fees.append(dict(department=department,month=month,license_cents=round(settings['monthly_fee_usd']*100),setup_cents=round(settings['setup_fee_usd']*100) if month_index==0 else 0))
            for i in range(260+department_index*60+month_index*70):
                model=rng.choices(['Economy','Extended'],[0.7,0.3])[0]
                outcome=rng.choices(['accepted','reworked','fallback'],[0.79-department_index*0.045,0.16+department_index*0.025,0.05+department_index*0.02])[0]
                retries=rng.choices([0,1,2],[0.84,0.13,0.03])[0]
                input_tokens=sum(rng.randint(800,5200) for _ in range(retries+1))
                output_tokens=sum(rng.randint(120,950) for _ in range(retries+1))
                review=rng.randint(2,6)
                baseline=settings['baseline_minutes']+rng.randint(-3,5)
                human=review+(rng.randint(5,22) if outcome=='reworked' else baseline if outcome=='fallback' else 0)
                rates=config['model_rates_usd_per_million_tokens'][model]
                tasks.append(dict(task_id=f'TASK-{len(tasks)+1:05d}',month=month,department=department,model=model,outcome=outcome,retries=retries,input_tokens=input_tokens,output_tokens=output_tokens,api_cost_microusd=input_tokens*rates['input']+output_tokens*rates['output'],baseline_minutes=baseline,human_minutes=human))
    return tasks,fees

def database(tasks,fees):
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE tasks(task_id TEXT PRIMARY KEY,month TEXT,department TEXT,model TEXT,outcome TEXT CHECK(outcome IN (\'accepted\',\'reworked\',\'fallback\')),retries INTEGER CHECK(retries>=0),input_tokens INTEGER CHECK(input_tokens>=0),output_tokens INTEGER CHECK(output_tokens>=0),api_cost_microusd INTEGER CHECK(api_cost_microusd>=0),baseline_minutes REAL CHECK(baseline_minutes>=0),human_minutes REAL CHECK(human_minutes>=0))')
    db.execute('CREATE TABLE fees(department TEXT,month TEXT,license_cents INTEGER CHECK(license_cents>=0),setup_cents INTEGER CHECK(setup_cents>=0),PRIMARY KEY(department,month))')
    db.executemany('INSERT INTO tasks VALUES(:task_id,:month,:department,:model,:outcome,:retries,:input_tokens,:output_tokens,:api_cost_microusd,:baseline_minutes,:human_minutes)',tasks)
    db.executemany('INSERT INTO fees VALUES(:department,:month,:license_cents,:setup_cents)',fees)
    return db

def summarize(db,department='All departments',month='All months'):
    scope={'department':department,'month':month}
    r=dict(db.execute((ROOT/'sql/task_summary.sql').read_text(),scope).fetchone())
    f=dict(db.execute((ROOT/'sql/fee_summary.sql').read_text(),scope).fetchone())
    useful=r['accepted']+r['reworked']
    total=r['api_cost_microusd']/1_000_000+(f['license_cents']+f['setup_cents'])/100
    return {**scope,**r,**f,'useful_tasks':useful,'technology_cost_usd':total,
            'cost_per_useful_task_usd':total/useful if useful else None,
            'first_pass_pct':100*r['accepted']/r['tasks'] if r['tasks'] else None,
            'net_capacity_minutes':r['baseline_minutes']-r['human_minutes']}

def value_scenario(summary,hourly_rate,realization_pct):
    if hourly_rate<0 or not 0<=realization_pct<=100:raise ValueError('Scenario inputs outside supported range')
    capacity=summary['net_capacity_minutes']/60*hourly_rate
    # Additional labor is always a modeled cost; only freed capacity is discounted.
    benefit=max(capacity,0)*realization_pct/100+min(capacity,0)
    technology=summary['technology_cost_usd']
    return {'capacity_value_usd':capacity,'modeled_benefit_usd':benefit,
            'modeled_net_value_usd':benefit-technology,
            'modeled_roi_pct':100*(benefit-technology)/technology if technology else None,
            'break_even_realization_pct':100*technology/capacity if capacity>0 else None}

def main():
    config=json.loads((ROOT/'assumptions.json').read_text());tasks,fees=generate(config)
    db=database(tasks,fees)
    summaries=[summarize(db,d,m) for d in ['All departments',*config['departments']] for m in ['All months',*config['months']]]
    total=summaries[0]
    monthly=[s for s in summaries if s['department']=='All departments' and s['month']!='All months']
    departmental=[s for s in summaries if s['department']!='All departments' and s['month']=='All months']
    checks={
        'unique_task_ids':len({t['task_id'] for t in tasks})==len(tasks),
        'outcomes_reconcile':total['tasks']==total['accepted']+total['reworked']+total['fallback'],
        'monthly_costs_reconcile':abs(sum(s['technology_cost_usd'] for s in monthly)-total['technology_cost_usd'])<1e-8,
        'department_costs_reconcile':abs(sum(s['technology_cost_usd'] for s in departmental)-total['technology_cost_usd'])<1e-8,
        'tokens_reprice_exactly':sum(t['input_tokens']*config['model_rates_usd_per_million_tokens'][t['model']]['input']+t['output_tokens']*config['model_rates_usd_per_million_tokens'][t['model']]['output'] for t in tasks)==total['api_cost_microusd'],
        'fees_counted_once':sum(f['license_cents']+f['setup_cents'] for f in fees)==total['license_cents']+total['setup_cents'],
    }
    if not all(checks.values()):raise AssertionError(checks)
    data={'data_kind':'synthetic_scenario','period':'June–August 2026','assumptions':config,'summary':summaries,'checks':checks}
    for folder in ('outputs','dashboard'):
        (ROOT/folder).mkdir(exist_ok=True);(ROOT/folder/'data.json').write_text(json.dumps(data,indent=2)+'\n')
    (ROOT/'data/generated').mkdir(parents=True,exist_ok=True)
    for name,rows in [('data/generated/tasks.csv',tasks),('data/fees.csv',fees),('outputs/summary.csv',summaries)]:
        with (ROOT/name).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    example=value_scenario(total,45,25)
    (ROOT/'outputs/findings.md').write_text(f'''# Findings from the example workload

All usage, outcomes, prices, fees, and time baselines are simulated. This AI-assisted portfolio example evaluates measurement choices, not a real vendor or deployment.

## What the fixture shows

- {total['tasks']:,} business tasks; {total['first_pass_pct']:.1f}% accepted without rework.
- ${total['technology_cost_usd']:,.2f} in modeled technology cost, comprising API usage, recurring fees, and one-time setup fees.
- ${total['cost_per_useful_task_usd']:.2f} per usable AI-assisted task. All attempted tasks contribute cost; the denominator includes accepted and reworked tasks, and excludes manual fallback.
- {total['net_capacity_minutes']/60:,.1f} net hours relative to the assumed manual baseline, after review, rework, and manual fallback. These hours are simulated capacity, not observed savings.
- At an assumed $45/hour, {example['break_even_realization_pct']:.1f}% of that capacity value would need to become an economic benefit to cover the modeled technology cost. Whether this is achievable is unknown.

## What a decision-maker should ask

Choose a quality threshold before judging value. Include retry usage and failed attempts in costs; count monthly fees once. Separate time freed from money saved. At 0% realization, positive capacity creates no modeled financial benefit. Negative capacity is always treated as additional labor cost. Compare departments within their workflow context; workload mix prevents causal model comparisons.

## Evidence needed before a real rollout decision

Replace the generated workload with authorized task and billing logs. Measure manual baselines and human review effort on comparable work, use independently reviewed outcome labels, reconcile invoices, and test results on a later time period. Add infrastructure, integration, security review, and ongoing maintenance costs where applicable. This prototype does not automate staffing or vendor decisions.

## Why this is a current question

The [2026 State of FinOps report](https://data.finops.org/) identifies AI cost management and business-value measurement as priorities. It motivates the question; it does not provide the simulated outcomes or fictional model prices in this repository.
''')
    db.close();print(json.dumps({'tasks':total['tasks'],'technology_cost':total['technology_cost_usd'],'first_pass_pct':total['first_pass_pct'],'checks':checks},indent=2))

if __name__=='__main__':main()
