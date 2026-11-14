-- Run this first to confirm the published NEAR BigQuery schema before contract attribution.
-- It inspects column names only; it does not scan transaction history.
SELECT table_name, column_name, field_path, data_type
FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
WHERE table_name IN ('transactions', 'receipts', 'receipt_actions')
  AND (
    column_name IN ('block_date', 'signer_account_id', 'receiver_account_id',
                    'transaction_hash', 'originated_from_transaction_hash', 'receiver_account_id',
                    'predecessor_account_id', 'receipt_id', 'action_kind')
    OR field_path IN ('signer_account_id', 'transaction_hash', 'originated_from_transaction_hash',
                      'receiver_account_id', 'predecessor_account_id', 'receipt_id', 'action_kind')
  )
ORDER BY table_name, field_path;
