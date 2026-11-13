# Data files

Real runs of `python fetch_data.py` write:

- `retention.csv`: one row per variant, cohort week, and observed follow-up week.
- `run_meta.json`: fetch timestamp, query byte count, date window, source table, SQL hash, and row count.

These files are generated from the public BigQuery source. Do not replace them with synthetic demo output. Demo data lives under the ignored `demo/` directory and is clearly labelled.
