# Does NEAR Keep Its Users?

An evidence-first investment thesis on NEAR, built for **NEAR HACKATHON**, track **Investment Thesis** (`thesis`).

**The question:** what share of newly observed NEAR accounts signs a transaction in the exact fourth follow-up week, and is that changing across weekly cohorts?

The repository contains the BigQuery SQL and a script that can fetch a fresh snapshot when run by an authenticated researcher. The currently published analysis uses a supplied aggregate CSV export. Its original BigQuery job ID, execution timestamp, bytes processed and query hash were not provided, so this repository does not claim an independently verified rerun.

- Dashboard: [docs/index.html](docs/index.html), backed by the supplied cohort CSV in `docs/data/retention.csv`.
- Contract attribution: `sql/near_schema_check.sql` and `sql/contract_attribution.sql`.
- Network economics and valuation: [research/network_economics_and_valuation.md](research/network_economics_and_valuation.md).
- Written thesis: [THESIS.md](THESIS.md), calculated from the supplied CSV.
- Canonical analysis input: `data/retention.csv`; published dashboard copy: `docs/data/retention.csv`; calculated summary: `docs/data/summary.json`.

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

The default maximum billed bytes is 100 GB. The script refuses to run if the dry-run estimate exceeds `--max-gb`, and the real query also sets BigQuery's `maximum_bytes_billed` to the same cap.

### Compare 12-week and 26-week definitions of “new”

Run the same cohort dates twice, changing only the burn-in. The script now writes separate CSV and metadata files so one run does not overwrite the other:

```bash
# 12-week burn-in
python fetch_data.py --project YOUR_GCP_PROJECT --burn-in-weeks 12 --output-stem retention_12w --dry-run
python fetch_data.py --project YOUR_GCP_PROJECT --burn-in-weeks 12 --output-stem retention_12w

# 26-week burn-in
python fetch_data.py --project YOUR_GCP_PROJECT --burn-in-weeks 26 --output-stem retention_26w --dry-run
python fetch_data.py --project YOUR_GCP_PROJECT --burn-in-weeks 26 --output-stem retention_26w
```

Compare the same cohort weeks, follow-up horizons and first-week activity filters:

```bash
python compare_burnin.py
```

This writes `data/burnin_comparison.json` with sample sizes, exact-week retention and early-to-late comparisons for every filter. The 26-week result is not yet run because the supplied export only contains the 12-week definition. The current dashboard must not be described as having passed the 26-week robustness test.

### Attribute the large cohorts to applications

1. Run `sql/near_schema_check.sql` to inspect the available BigQuery fields.
2. Review the estimated bytes for `sql/contract_attribution.sql` before running it.
3. The draft query counts distinct cohort signers whose transactions generated receipts to receiver accounts, with cohort sizes as denominators. It includes all receipt kinds, so it is not yet a verified contract-call or application attribution query.
4. Resolve high-activity receiver accounts to verified application/contract names and compare their deployment dates with public campaign dates.

A receiver account is only a contract candidate. Do not call it an application or campaign without confirming the deployed code/account and independent campaign evidence. The supplied aggregate CSV does not contain account IDs, so no application-level conclusion has been made yet.

### Network economics and valuation

See [the economics and valuation research framework](research/network_economics_and_valuation.md). It records the dated market snapshot, protocol issuance and fee mechanisms, required revenue verification, valuation ratios and key risks. The current retention CSV does not contain economic inputs, so the thesis does not yet claim that NEAR is cheap, expensive or undervalued.

Useful options:

- `--cohort-weeks 40`: number of cohort weeks, including both endpoints. Must be at least 19 for the week-4 trend comparison.
- `--burn-in-weeks 12` or `26`: prior weeks used to decide whether an account is new.
- `--output-stem retention_26w`: write a separately named CSV and metadata file without overwriting the default export.
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
