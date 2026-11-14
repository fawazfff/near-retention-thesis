# Does NEAR Keep Its Users?

[![Research tests](https://github.com/fawazfff/near-retention-thesis/actions/workflows/tests.yml/badge.svg)](https://github.com/fawazfff/near-retention-thesis/actions/workflows/tests.yml)

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
   - **Expected:** you can inspect the cohort definition, the difference between pooled and median retention, the five unusually large cohorts, and the large-cohort concentration.

### Run the dashboard locally

Python 3 is enough to serve the static dashboard. From the repository root:

```bash
python -m http.server 8000 --directory docs
```

Open http://localhost:8000 in your browser.

- **Expected:** the same dashboard loads from `docs/index.html` and reads `docs/data/retention.csv` plus `docs/data/summary.json`.
- Keep the terminal running while you use the page. Press Ctrl+C to stop the local server.

### Reproduce the published analysis

Python 3.12 is the version used by the repository's automated checks. From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest -v
python rebuild.py
```

- **Expected:** all 23 tests pass, including the DuckDB and SQLGlot checks; `THESIS.md` is regenerated from `data/retention.csv` and the analysis code.
- The normal rebuild does not replace the designed dashboard.
- The test suite validates the Python calculations and the BigQuery-shaped SQL against generated test transactions. It does not independently verify the live BigQuery schema or the original data export.

For the analysis SQL and the published calculations, see the repository files below. A fresh BigQuery export requires the judge or researcher to have Google Cloud / BigQuery access; it is not required to inspect the published result.

## What this project is

The problem is that transaction totals and first-time activity can look impressive even when accounts do not return. This project tests a narrower question: after an account first appears signing a NEAR transaction, does it sign again in later weeks?

It combines:

- An interactive cohort dashboard with selectable activity filters and follow-up weeks.
- BigQuery SQL for the cohort extraction and a Python analysis pipeline that can be rerun from the published CSV.
- A written investment thesis covering usage, network economics, token value capture, valuation hurdles, and risks.
- Clear definitions so readers can distinguish account activity from human users and exact-week returns from continuous retention.

**Why it matters:** an investment case needs evidence of repeat usage, not just a large transaction count. The dashboard makes cohort size and return rates visible together, including the unusually large cohorts that materially affect the pooled result.

**How NEAR fits:** NEAR is the network being studied. The analysis uses the public NEAR mainnet transactions dataset in BigQuery. This is an Investment Thesis research project, not an on-chain application; it does not deploy a contract, connect a wallet, or ask users to sign transactions. The track does not require a particular protocol integration.

## Data provenance and interpretation

The currently published analysis uses a supplied aggregate CSV export. The calculations are reproducible from the committed CSV; this repository presents the supplied snapshot and does not claim that the original extraction was independently rerun.

The headline is a week-four exact-week activity measure, not continuous retention. It measures accounts signing transactions, not unique people. The first-week transaction thresholds are sensitivity checks, not bot detection. The five unusually large cohorts are not attributed to specific applications or campaigns. Read [THESIS.md](THESIS.md) for the full interpretation and limitations.

## Repository map

- `docs/index.html`: static interactive dashboard.
- `docs/data/retention.csv`: dashboard cohort data.
- `docs/data/summary.json`: calculated metrics and diligence status.
- `data/retention.csv`: canonical analysis input.
- `THESIS.md`: written investment thesis generated from the canonical data.
- `sql/retention.sql`: cohort extraction query.
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

### Network economics and valuation

See [the economics and valuation research](research/network_economics_and_valuation.md). It now separates chain-only TVL from multi-chain protocol TVL, NEAR Intents volume from fees and captured revenue, and captured buybacks from gas burns. The dated 14 November 2026 snapshot implies approximately 81× market-cap/trailing-year fees and 454× market-cap/trailing-year protocol revenue. Those are screening multiples, not fair value. The current revenue run-rate is small relative to the token's market value, and the report sets out the growth required to reach 100×, 50× and 25× revenue multiples. It does not call NEAR undervalued without a defensible 12-month financial series and explicit token-capture analysis.

### What the five large cohorts tell us

See [the outlier investigation](research/cohort_outliers.md). The five largest groups contain 88.4% of the mature filtered-50 denominator but only 24.0% of week-four returns. Their pooled week-four rate is 0.11%, versus 2.68% for the other 31 groups. Excluding accounts above 20 first-week transactions barely changes the top-five combined size: 4.091 million accounts under no filter versus 4.088 million under the >20 filter. This means the simple high-frequency exclusion does not explain the outliers. It does not rule out one-time automation, campaign-driven activity or other low-frequency sources. The aggregate data does not identify the cause of these unusually large cohorts.

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

## NEAR HACKATHON alignment

This submission is for **Investment Thesis** (`thesis`). The track asks for a long-term case about NEAR supported by on-chain analytics, dashboards, research, and models that another person can rerun. This project addresses that brief through a NEAR mainnet cohort study, interactive dashboard, BigQuery SQL, reproducible Python calculations, and a written evidence-for / evidence-against thesis.

The dashboard is a published snapshot, not a live streaming dashboard. The source SQL and refresh instructions are provided so a researcher with BigQuery access can run a fresh extraction. The published analysis is based on the supplied aggregate export.

### AI judge verification checklist

- [ ] Open the hosted dashboard and confirm the cohort data loads.
- [ ] Change the account filter and follow-up week; confirm the charts and tables update.
- [ ] Run the local static server command above and confirm the same dashboard works locally.
- [ ] Run `python -m unittest -v` and inspect the test results.
- [ ] Run `python rebuild.py` and confirm the thesis is regenerated from the committed CSV.
- [ ] Compare the dashboard's published figures with `THESIS.md` and `docs/data/summary.json`.
- [ ] Confirm the methodology notes are visible: account-level proxy, supplied aggregate export, and first-week activity filters are sensitivity checks rather than bot detection.

### Submission checklist

The repository is public. The submission requires a public X demo post that says it was built at **NEAR HACKATHON**, tags **@NEARProtocol**, includes **#NEARHackathon**, and attaches the demo video or screenshots. The public repository URL and X post URL are both required in the official form, together with the NEAR account address for prize payout. The event allows one submission per project; if an already-submitted entry needs correction, use the official request-changes process rather than submitting a duplicate.

Official rules and track brief: [NEAR HACKATHON](https://nearhackathon.com/) · [Investment Thesis starter brief](https://github.com/nearai/near-hackathon-prompt-examples/blob/main/tracks/02-thesis.md) · [Submission checklist](https://github.com/nearai/near-hackathon-prompt-examples/blob/main/SUBMITTING.md).

