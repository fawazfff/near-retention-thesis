-- NEAR new-account retention, weekly cohorts (one scan of the transactions table).
--
-- Definitions
--   active account : signed at least one transaction (signer_account_id) in a week
--   week           : Monday-start, UTC (block_date)
--   cohort week    : first week an account signs a transaction inside the scan window
--   new account    : cohort week >= @start_date, i.e. no signed transaction during the
--                    burn-in weeks before it (@scan_start .. @start_date). Accounts that
--                    were dormant for longer than the burn-in look "new" (limitation).
--   k              : whole weeks since the cohort week (0 = cohort week itself)
--   variants       : 'all' keeps every new account; 'filtered_N' drops accounts that signed
--                    more than N transactions in their first week (bot / airdrop-farm proxy).
--
-- Parameters (set by fetch_data.py; in the BigQuery console add matching DECLARE lines):
--   @scan_start      DATE  first day scanned (start_date minus the burn-in)
--   @start_date      DATE  Monday of the first cohort week
--   @end_date        DATE  Sunday ending the last complete week
--   @last_week_start DATE  Monday of the last complete week (= end_date - 6 days)
--   @max_weeks       INT64 largest k reported
--
-- Output: one row per (variant, cohort_week, k) with accounts_active > 0, only for weeks
-- that are fully observed. cohort_size is the k = 0 row. Missing rows mean zero accounts.
-- Cost: reads only block_date and signer_account_id. Check "This query will process" first.

WITH weekly AS (
  SELECT
    signer_account_id AS acct,
    DATE_TRUNC(block_date, WEEK(MONDAY)) AS wk,
    COUNT(*) AS txs
  FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`
  WHERE block_date BETWEEN @scan_start AND @end_date
  GROUP BY acct, wk
),
tagged AS (
  SELECT
    acct,
    wk,
    MIN(wk) OVER (PARTITION BY acct) AS cohort_wk,
    FIRST_VALUE(txs) OVER (PARTITION BY acct ORDER BY wk) AS first_wk_txs
  FROM weekly
),
cohort_activity AS (
  SELECT
    acct,
    cohort_wk,
    first_wk_txs,
    DIV(DATE_DIFF(wk, cohort_wk, DAY), 7) AS k
  FROM tagged
  WHERE cohort_wk >= @start_date
)
SELECT
  v.variant AS variant,
  a.cohort_wk AS cohort_week,
  a.k AS k,
  COUNT(*) AS accounts_active
FROM cohort_activity AS a
JOIN (
  SELECT 'all' AS variant, 1000000000 AS max_first_wk_txs
  UNION ALL SELECT 'filtered_200', 200
  UNION ALL SELECT 'filtered_50', 50
  UNION ALL SELECT 'filtered_20', 20
) AS v
  ON a.first_wk_txs <= v.max_first_wk_txs
WHERE a.k <= @max_weeks
  AND DATE_DIFF(@last_week_start, a.cohort_wk, DAY) >= a.k * 7
GROUP BY variant, cohort_week, k
ORDER BY variant, cohort_week, k
