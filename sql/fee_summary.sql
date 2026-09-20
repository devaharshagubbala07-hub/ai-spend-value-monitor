-- Aggregate fees independently. Joining fees to task rows would multiply them.
SELECT COALESCE(SUM(license_cents),0) AS license_cents,
       COALESCE(SUM(setup_cents),0) AS setup_cents
FROM fees
WHERE (:department = 'All departments' OR department = :department)
  AND (:month = 'All months' OR month = :month);
