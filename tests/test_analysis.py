import unittest
import sqlite3
from analysis import database,summarize,value_scenario

def task(id='1',outcome='accepted',**extra):
    r=dict(task_id=id,month='2026-06',department='A',model='Economy',outcome=outcome,retries=1,input_tokens=200,output_tokens=100,api_cost_microusd=600,baseline_minutes=10,human_minutes=2);r.update(extra);return r
def fee(**extra):
    r=dict(department='A',month='2026-06',license_cents=10000,setup_cents=5000);r.update(extra);return r

class ValueTests(unittest.TestCase):
    def test_fees_are_not_multiplied_by_tasks(self):
        db=database([task(),task('2')],[fee()]);self.assertAlmostEqual(summarize(db)['technology_cost_usd'],150.0012)
    def test_failed_attempt_cost_remains_in_numerator(self):
        db=database([task(),task('2','fallback')],[]);s=summarize(db);self.assertEqual(s['useful_tasks'],1);self.assertAlmostEqual(s['cost_per_useful_task_usd'],.0012)
    def test_no_useful_tasks_has_missing_unit_cost(self):
        db=database([task(outcome='fallback')],[]);self.assertIsNone(summarize(db)['cost_per_useful_task_usd'])
    def test_scope_keeps_fees_even_without_tasks(self):
        db=database([], [fee()]);self.assertEqual(summarize(db,'A','2026-06')['technology_cost_usd'],150);self.assertEqual(summarize(db,'B')['technology_cost_usd'],0)
    def test_duplicate_tasks_and_fees_fail(self):
        with self.assertRaises(sqlite3.IntegrityError):database([task(),task()],[])
        with self.assertRaises(sqlite3.IntegrityError):database([], [fee(),fee()])
    def test_capacity_is_not_automatically_cash(self):
        s=dict(net_capacity_minutes=60,technology_cost_usd=10)
        self.assertEqual(value_scenario(s,40,0)['modeled_net_value_usd'],-10)
        self.assertEqual(value_scenario(s,40,25)['modeled_net_value_usd'],0)
    def test_negative_capacity_always_counts_as_labor_cost(self):
        s=value_scenario(dict(net_capacity_minutes=-60,technology_cost_usd=10),40,0);self.assertEqual(s['modeled_net_value_usd'],-50);self.assertIsNone(s['break_even_realization_pct'])

if __name__=='__main__':unittest.main()
