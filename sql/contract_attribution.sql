-- Contract-touch analysis for the largest 12-week-burn-in cohort outliers.
-- First run sql/near_schema_check.sql and confirm the listed fields exist.
-- This draft attributes receipts originating from transactions signed by cohort accounts.
-- It is not yet schema-verified. Run near_schema_check.sql first and confirm every field.
-- Receiver accounts are candidates only. This query does not prove they are contracts,
-- identify the action kind, or establish a campaign/application name.
-- Campaign attribution requires external campaign dates and should not be inferred here.
--
-- Parameters:
-- @scan_start DATE       26-week burn-in start (for comparable 12w/26w cohorts)
-- @start_date DATE       first Monday of cohort window
-- @end_date DATE         Sunday ending last fully observed week
-- @last_week_start DATE  Monday of last fully observed week
-- @max_weeks INT64       maximum follow-up week
-- @max_first_week_transactions INT64  first-week transaction cap (use 50 for the headline filter)
--
-- Dry-run before executing. This query joins transactions and receipts and may be materially
-- more expensive than the signer-only retention query. It includes all receipt kinds;
-- inspect the receipt schema and add action-level filters only after verifying their fields.

WITH weekly_signers AS (
  SELECT
    signer_account_id,
    DATE_TRUNC(block_date, WEEK(MONDAY)) AS week_start,
    COUNT(*) AS signed_transactions
  FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`
  WHERE block_date BETWEEN @scan_start AND @end_date
  GROUP BY signer_account_id, week_start
),
cohorts AS (
  SELECT
    signer_account_id,
    MIN(week_start) AS cohort_week,
    ARRAY_AGG(signed_transactions ORDER BY week_start LIMIT 1)[OFFSET(0)]
      AS first_week_transactions
  FROM weekly_signers
  GROUP BY signer_account_id
),
eligible_cohorts AS (
  SELECT *
  FROM cohorts
  WHERE cohort_week >= @start_date
    AND first_week_transactions <= @max_first_week_transactions
),
cohort_sizes AS (
  SELECT cohort_week, COUNT(*) AS cohort_accounts
  FROM eligible_cohorts
  GROUP BY cohort_week
),
receiver_interactions AS (
  SELECT DISTINCT
    c.cohort_week,
    DATE_TRUNC(r.block_date, WEEK(MONDAY)) AS activity_week,
    c.signer_account_id,
    r.receiver_account_id,
    r.receipt_id
  FROM eligible_cohorts c
  JOIN `bigquery-public-data.crypto_near_mainnet_us.transactions` t
    ON t.signer_account_id = c.signer_account_id
   AND t.block_date BETWEEN @start_date AND @end_date
  JOIN `bigquery-public-data.crypto_near_mainnet_us.receipts` r
    ON r.originated_from_transaction_hash = t.transaction_hash
   AND r.block_date BETWEEN @start_date AND @end_date
  WHERE DATE_DIFF(DATE_TRUNC(r.block_date, WEEK(MONDAY)), c.cohort_week, DAY)
        BETWEEN 7 AND @max_weeks * 7
),
largest_cohorts AS (
  SELECT cohort_week
  FROM cohort_sizes
  ORDER BY cohort_accounts DESC
  LIMIT 5
)
SELECT
  f.cohort_week,
  DIV(DATE_DIFF(f.activity_week, f.cohort_week, DAY), 7) AS followup_week,
  f.receiver_account_id,
  COUNT(DISTINCT f.signer_account_id) AS distinct_cohort_signers,
  COUNT(DISTINCT f.receipt_id) AS receiver_receipts,
  s.cohort_accounts,
  SAFE_DIVIDE(COUNT(DISTINCT f.signer_account_id), s.cohort_accounts)
    AS share_of_cohort_signers
FROM receiver_interactions f
JOIN cohort_sizes s USING (cohort_week)
WHERE f.cohort_week IN (SELECT cohort_week FROM largest_cohorts)
GROUP BY f.cohort_week, followup_week, f.receiver_account_id, s.cohort_accounts
ORDER BY f.cohort_week, followup_week, distinct_cohort_signers DESC;
