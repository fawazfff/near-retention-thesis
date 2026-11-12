-- First checkpoint: inspect the live dataset before writing analytical SQL.
-- Run this in BigQuery Studio with a billing project selected.
-- This metadata query reads INFORMATION_SCHEMA, not the full chain tables.

SELECT
  table_name,
  table_type
FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name;

-- Then inspect the columns for each candidate table.
-- Keep the output as data/schema.json in the repository.
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable
FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position;

-- Do not run cohort analysis until the actual table names, columns,
-- partition fields, and data coverage have been checked.
