-- One row per business task. Token counts already include every retry.
SELECT COUNT(*) AS tasks,
       COALESCE(SUM(outcome='accepted'),0) AS accepted,
       COALESCE(SUM(outcome='reworked'),0) AS reworked,
       COALESCE(SUM(outcome='fallback'),0) AS fallback,
       COALESCE(SUM(retries),0) AS retries,
       COALESCE(SUM(input_tokens),0) AS input_tokens,
       COALESCE(SUM(output_tokens),0) AS output_tokens,
       COALESCE(SUM(api_cost_microusd),0) AS api_cost_microusd,
       COALESCE(SUM(baseline_minutes),0) AS baseline_minutes,
       COALESCE(SUM(human_minutes),0) AS human_minutes
FROM tasks
WHERE (:department = 'All departments' OR department = :department)
  AND (:month = 'All months' OR month = :month);
