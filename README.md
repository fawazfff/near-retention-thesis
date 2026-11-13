# Does NEAR Keep Its Users?

An evidence-first investment thesis on NEAR, built for **NEAR HACKATHON**, track **Investment Thesis** (`thesis`).

**The question:** of every 100 newly observed NEAR accounts, how many are still signing transactions four weeks later, and is that changing across weekly cohorts?

The project fetches public NEAR mainnet data from BigQuery, calculates cohort retention, tests whether the change is meaningful, and generates both the dashboard and `THESIS.md` from the same source data.

- Dashboard preview: [`docs/index.html`](docs/index.html). It is clearly labelled **synthetic demo data**, not real NEAR results.
- Written thesis: [`THESIS.md`](THESIS.md). It is generated only from fetched data and is not replaced by demo mode.
- Source data: `data/retention.csv` and `data/run_meta.json` after a real fetch.

## What it does

1. `sql/retention.sql` groups accounts that sign transactions into weekly cohorts, then counts how many sign again in later weeks.
2. It reports four versions: no filter, and three bot-like filters that exclude accounts with more than 200, 50, or 20 transactions in their first week. The headline uses 50, fixed before data was pulled. All variants remain visible.
3. `rebuild.py` turns `data/retention.csv` into every number, chart, the dashboard and `THESIS.md`. Nothing is typed into the thesis by hand.

## Quick start

Python 3.10+ is recommended.

```bash
python -m unittest -v
python rebuild.py --demo
```

The demo command writes a synthetic preview to `demo/`. It is fake data, prominently labelled as synthetic, and never overwrites `THESIS.md` or the real-data dashboard in `docs/`.

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

Useful options:

- `--cohort-weeks 40`: number of cohort weeks, including both endpoints. Must be at least 19 for the week-4 trend comparison.
- `--burn-in-weeks 12`: prior weeks used to decide whether an account is new.
- `--max-weeks 12`: furthest follow-up week to include. Must be at least 4.
- `--max-gb 100`: hard cap for query processing.
- `--literal-dates`: inline dates if BigQuery's dry-run estimate suggests parameterized partition pruning is not working.

## Method

An account is active in a week if it signed at least one transaction (`signer_account_id`) in a Monday-start UTC week. A cohort contains accounts whose first observed signed transaction occurs in that week after a 12-week burn-in. Retention at week 4 is the share of the cohort that signs again in the fourth following week.

The trend test compares the eight earliest and eight latest cohorts with a complete week-4 observation, using one retention rate per cohort and a Welch 95% interval. A change is called improving or declining only if the interval excludes zero and the difference is at least one percentage point. If there are too few eligible cohorts, the analysis stops with an explicit error instead of producing a weak headline.

The SQL's scan window includes exactly the requested number of cohort weeks. The earlier version accidentally included one extra week; this is fixed and covered by a regression test.

## Known limits

- This measures accounts signing transactions, not unique humans.
- Accounts that only act through relayers or only receive tokens are not counted.
- A 12-week burn-in cannot distinguish a genuinely new account from one that was dormant for longer than 12 weeks.
- The transaction-count filter is a sensitivity check, not proof that an account is a bot or airdrop farmer.
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
