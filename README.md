# Does NEAR Keep Its Users?

An evidence-first investment thesis on NEAR, built for **NEAR HACKATHON 2026**, **Investment Thesis** track (`thesis`).

**Live research dashboard:** https://near-retention-thesis.vercel.app  
**Source code:** https://github.com/fawazfff/near-retention-thesis  
**Written thesis:** [THESIS.md](THESIS.md)

## Judge quickstart

This is a research dashboard, not a wallet app. You do not need a NEAR wallet, private key, testnet funds, API key, or blockchain transaction to inspect it. The dashboard reads the committed cohort CSV and summary JSON. It does not claim to stream live data.

### Try the hosted project

1. Open **https://near-retention-thesis.vercel.app**.
   - **Expected:** the page title is “Does NEAR keep its users?” and the retention dashboard loads.
2. In **Account filter**, switch between all accounts and the three first-week transaction thresholds.
   - **Expected:** the KPI values, cohort chart, group-size chart, return curve, and tables update to the selected filter.
3. In **Check activity in follow-up week**, choose week 1, 4, 8, or 12.
   - **Expected:** the eligible cohort count and return figures change. Newer cohorts are excluded when they do not yet have enough follow-up.
4. Select a point in the cohort chart or a bar in the group-size chart.
   - **Expected:** the dashboard shows the selected cohort's exact date and figures.
5. Scroll to the method, caveats, and research sections. Open [THESIS.md](THESIS.md) and [the outlier investigation](research/cohort_outliers.md).
   - **Expected:** you can inspect the cohort definition, the difference between pooled and median retention, the five unusually large cohorts, and the outstanding attribution work.

### Run the dashboard locally

Python 3 is enough to serve the static dashboard. From the repository root:

```bash
python -m http.server 8000 --directory docs
```

Open http://localhost:8000 in your browser.

- **Expected:** the same dashboard loads from `docs/index.html` and reads `docs/data/retention.csv` plus `docs/data/summary.json`.
- Keep the terminal running while you use the page. Press Ctrl+C to stop the local server.

### Reproduce the published analysis

Python 3.10 or newer is recommended.

```bash
python -m unittest -v
python rebuild.py
```

- **Expected:** the standard-library test suite passes, and `THESIS.md` is regenerated from `data/retention.csv` and the analysis code.
- The normal rebuild does not replace the designed dashboard.
- Optional SQL-to-reference tests use DuckDB and SQLGlot. Install them with `python -m pip install -r requirements-dev.txt`, then run `python -m unittest -v` again.

For the exact SQL, BigQuery refresh procedure, 12-week versus 26-week comparison, and application-attribution checks, see the sections below. A fresh BigQuery export requires the judge or researcher to have Google Cloud / BigQuery access; it is not required to inspect the published result.

## What this project is

The project asks whether NEAR accounts that first appear signing transactions return to sign transactions in later weeks. It combines:

- An interactive cohort dashboard with selectable activity filters and follow-up weeks.
- A reproducible analysis script and BigQuery SQL.
- A written investment thesis covering usage, network economics, token value capture, valuation hurdles, and risks.
- Explicit limitations and follow-up diligence tasks.

**How NEAR fits:** NEAR is the network being studied. The analysis uses the public NEAR mainnet transactions dataset in BigQuery. This is an Investment Thesis research project, not an on-chain application; it does not deploy a contract, connect a wallet, or ask users to sign transactions. The track does not require a particular protocol integration.

## Data provenance and interpretation

The currently published analysis uses a supplied aggregate CSV export. The original BigQuery job ID, execution timestamp, bytes processed, and query hash were not supplied. The calculations are reproducible from the committed CSV, but this repository does **not** claim an independently verified BigQuery rerun.

The headline is a week-four exact-week activity measure, not continuous retention. It measures accounts signing transactions, not unique people. The first-week transaction thresholds are sensitivity checks, not bot detection. The five unusually large cohorts have not yet been attributed to specific applications or campaigns, and the 26-week burn-in comparison has not been run. Read [THESIS.md](THESIS.md) for the full interpretation and limitations.

## Repository map

- `docs/index.html`: static interactive dashboard.
- `docs/data/retention.csv`: dashboard cohort data.
- `docs/data/summary.json`: calculated metrics and diligence status.
- `data/retention.csv`: canonical analysis input.
- `THESIS.md`: written investment thesis generated from the canonical data.
- `sql/retention.sql`: cohort extraction query.
- `sql/near_schema_check.sql` and `sql/contract_attribution.sql`: prepared schema and attribution research queries. Attribution has not yet been completed.
- `research/network_economics_and_valuation.md`: network economics and valuation research.
- `research/cohort_outliers.md`: investigation of the five unusually large cohorts.
- `tests/`: metric, rendering, and SQL-reference tests.

## What it does

1. `sql/retention.sql` groups accounts that sign transactions into weekly cohorts, then counts how many sign again in later weeks.
2. It reports four versions: no filter, and three high-activity filters that exclude accounts with more than 200, 50, or 20 transactions in their first week. The headline uses the 50-transaction threshold as a sensitivity setting. It is not a verified bot classifier. All variants remain visible.
3. `rebuild.py` regenerates `THESIS.md` from `data/retention.csv` and the analysis code. The published interactive dashboard reads the committed CSV directly. Normal rebuilds preserve its design. Use `python rebuild.py --overwrite-dashboard` only if you intentionally want to replace it with the simpler generated report page.

## Quick start

Python 3.10+ is recommended.

```bash
python -m unittest -v
python rebuild.py
```

The default rebuild regenerates the real-data thesis and leaves the designed dashboard untouched. `python rebuild.py --demo` writes a synthetic preview to `demo/`. It is fake data, prominently labelled as synthetic, and never overwrites `THESIS.md` or the real-data dashboard in `docs/`.

## Refreshing real data

Install the BigQuery client and authenticate locally:

```bash
python -m pip install -r requirements.txt
gcloud auth application-default login
```

Then run a dry run first:

```bash
python fetch_data.py --project YOUR_GCP_PROJECT --dry-run
```

The script prints the estimated bytes processed and exits without running the query. If the estimate is acceptable, run:

```bash
python fetch_data.py --project YOUR_GCP_PROJECT
python rebuild.py
```

The default maximum billed bytes is 100 GB. The script refuses to run if the dry-run estimate exceeds `--max-gb`, and the real query also sets BigQuery's `maximum_bytes_billed` to the same cap.

### Compare 12-week and 26-week definitions of “new”

Run the same cohort dates twice, changing only the burn-in. The script now writes separate CSV and metadata files so one run does not overwrite the other:

```bash
# 12-week burn-in
python fetch_data.py --project YOUR_GCP_PROJECT --cohort-weeks 40 --max-weeks 12 --last-week-start 2026-11-02 --burn-in-weeks 12 --output-stem retention_12w --dry-run
python fetch_data.py --project YOUR_GCP_PROJECT --cohort-weeks 40 --max-weeks 12 --last-week-start 2026-11-02 --burn-in-weeks 12 --output-stem retention_12w

# 26-week burn-in
python fetch_data.py --project YOUR_GCP_PROJECT --cohort-weeks 40 --max-weeks 12 --last-week-start 2026-11-02 --burn-in-weeks 26 --output-stem retention_26w --dry-run
python fetch_data.py --project YOUR_GCP_PROJECT --cohort-weeks 40 --max-weeks 12 --last-week-start 2026-11-02 --burn-in-weeks 26 --output-stem retention_26w
```

Compare the same cohort weeks, follow-up horizons and first-week activity filters:

```bash
python compare_burnin.py --cohort-csv docs/data/retention.csv
```

This writes `data/burnin_comparison.json` with sample sizes, exact-week retention and early-to-late comparisons for every filter. The 26-week result is not yet run because the supplied export only contains the 12-week definition. The `--last-week-start 2026-11-02` option pins both exports to the same 40 cohort weeks as the supplied CSV. The comparison also reports the difference in newly classified accounts by cohort week. This tests how sensitive the results are to the look-back period, but it does not identify the reason for reactivation. The dashboard must not be described as having passed the 26-week robustness test.

### Attribute the large cohorts to applications

1. Open the BigQuery Console with a Google Cloud project that can run queries. Paste the contents of `sql/near_schema_check.sql` and run it first. This reads `INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`, not transaction history, so it is a schema lookup rather than a full data scan. Copy the result rows (table name, field path and data type) and save them with the research notes.

2. Only after confirming the receipt and transaction join fields exist, paste `sql/contract_attribution.sql` into BigQuery. Set its parameters, run a dry run first, and inspect estimated bytes. Do not run the full receipt join if the field names differ or the cost estimate is unacceptable.
3. The draft query counts distinct cohort signers whose transactions generated receipts to receiver accounts, with cohort sizes as denominators. For the supplied 12-week study, set `@scan_start` = `2025-11-10`, `@start_date` = `2026-02-02`, `@end_date` = `2026-11-08`, `@last_week_start` = `2026-11-02`, `@max_weeks` = `12`, and `@max_first_week_transactions` = `50`. It includes all receipt kinds, so it is not yet a verified contract-call or application attribution query.
4. Resolve high-activity receiver accounts to verified application/contract names and compare their deployment dates with public campaign dates.

A receiver account is only a contract candidate. Do not call it an application or campaign without confirming the deployed code/account and independent campaign evidence. The supplied aggregate CSV does not contain account IDs, so no application-level conclusion has been made yet.

### Network economics and valuation

See [the economics and valuation research](research/network_economics_and_valuation.md). It now separates chain-only TVL from multi-chain protocol TVL, NEAR Intents volume from fees and captured revenue, and captured buybacks from gas burns. The dated 14 November 2026 snapshot implies approximately 81× market-cap/trailing-year fees and 454× market-cap/trailing-year protocol revenue. Those are screening multiples, not fair value. The current revenue run-rate is small relative to the token's market value, and the report sets out the growth required to reach 100×, 50× and 25× revenue multiples. It does not call NEAR undervalued without a defensible 12-month financial series and explicit token-capture analysis.

### What the five large cohorts tell us

See [the outlier investigation](research/cohort_outliers.md). The five largest groups contain 88.4% of the mature filtered-50 denominator but only 24.0% of week-four returns. Their pooled week-four rate is 0.11%, versus 2.68% for the other 31 groups. Excluding accounts above 20 first-week transactions barely changes the top-five combined size: 4.091 million accounts under no filter versus 4.088 million under the >20 filter. This means the simple high-frequency exclusion does not explain the outliers. It does not rule out one-time automation, campaign-driven activity or other low-frequency sources. Application attribution still requires account-level BigQuery data.

Useful options:

- `--cohort-weeks 40`: number of cohort weeks, including both endpoints. Must be at least 19 for the week-4 trend comparison.
- `--burn-in-weeks 12` or `26`: prior weeks used to decide whether an account is new.
- `--output-stem retention_26w`: write a separately named CSV and metadata file without overwriting the default export.
- `--last-week-start 2026-11-02`: pin the final cohort week so 12-week and 26-week burn-in exports use identical cohort dates.
- `--max-weeks 12`: furthest follow-up week to include. Must be at least 4.
- `--max-gb 100`: hard cap for query processing.
- `--literal-dates`: inline dates if BigQuery's dry-run estimate suggests parameterized partition pruning is not working.

## Method

An account is active in a week if it signed at least one transaction (`signer_account_id`) in a Monday-start UTC week. A cohort contains accounts whose first observed signed transaction occurs in that week after a 12-week burn-in. Retention at week 4 is the share of the cohort that signs in that exact fourth follow-up week, not the share that was active at any time during the first four weeks.

The trend test compares the eight earliest and eight latest cohorts with a complete week-4 observation, using one retention rate per cohort and a Welch 95% interval. A change is called improving or declining only if the interval excludes zero and the difference is at least one percentage point. If there are too few eligible cohorts, the analysis stops with an explicit error instead of producing a weak headline.

The SQL's scan window includes exactly the requested number of cohort weeks. The earlier version accidentally included one extra week; this is fixed and covered by a regression test.

## Known limits

- This measures accounts signing transactions, not unique humans.
- Accounts that only act through relayers or only receive tokens are not counted.
- A 12-week burn-in cannot distinguish a genuinely new account from one that was dormant for longer than 12 weeks.
- The first-week transaction-count filter is a sensitivity check, not a bot classifier.
- Retention is not value. This says nothing by itself about price, fees, revenue, or product-market fit.
- The query reads the public BigQuery dataset. Always dry-run before executing and inspect the reported bytes.

## Tests

```bash
python -m unittest -v
```

The standard-library tests cover the cohort window, metrics, confidence intervals, verdict logic, rendering, and missing-data errors. Two SQL-to-reference tests additionally run when the optional development dependencies are installed:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest -v
```

Those tests execute the BigQuery-shaped SQL translated to DuckDB against generated transactions and compare the output to an independent Python reference. They validate query logic, not BigQuery's live schema or billing estimate.

## AI assistance and libraries

Built with AI assistance for implementation, tests, and documentation. The research question, metric definitions, assumptions, and final interpretation must be reviewed by the author. Runtime for `rebuild.py` uses Python's standard library. `fetch_data.py` uses `google-cloud-bigquery`. Tests use `duckdb` and `sqlglot` as optional development dependencies. Charts are hand-built SVG, so the dashboard works offline.

## Hackathon notes

- Track: Investment Thesis (`thesis`).
- Data source: `bigquery-public-data.crypto_near_mainnet_us.transactions`.
- No on-chain deployment or signing is required. No keys or credentials belong in this repository.
- License: MIT, see [`LICENSE`](LICENSE).
