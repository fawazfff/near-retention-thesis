# Does NEAR Keep Its Users?


## Research status: data not yet fetched

This repository contains the analysis pipeline and a local synthetic dashboard preview. It does not yet contain a real BigQuery result, so no investment conclusion is published here.

The research question is whether NEAR mainnet accounts that first sign a transaction in a given week return to sign transactions in later weeks, and whether week-4 retention changes across cohorts.

## What must happen before a conclusion is possible

1. Fetch the public NEAR mainnet transactions table using `python fetch_data.py --project YOUR_GCP_PROJECT --dry-run` first.
2. Confirm the estimated bytes processed are within the configured cap, then run `python fetch_data.py --project YOUR_GCP_PROJECT`.
3. Run `python rebuild.py`. This generates the metrics, charts, dashboard, and this thesis from the fetched CSV and metadata.
4. Review the query assumptions, bot-filter sensitivity, confidence intervals, and limitations before interpreting the result.

## Fixed research choices

- Activity means at least one signed transaction (`signer_account_id`) in a Monday-start UTC week.
- New accounts have no signed transaction in the preceding 12-week burn-in window.
- Week-4 retention is the share of a cohort that signs again four weeks after its cohort week.
- The headline sensitivity variant excludes accounts with more than 50 transactions in their first week. Unfiltered, 200, and 20 transaction thresholds are also reported.
- The trend comparison uses the eight earliest and eight latest eligible cohorts, with a Welch 95% interval. A directional label requires the interval to exclude zero and a change of at least one percentage point.

## Current evidence

No real retention result has been computed. The dashboard preview uses synthetic transactions only. Synthetic numbers must not be cited as evidence about NEAR.

## Limitations to keep visible

- An account is not necessarily a person.
- The 12-week burn-in can classify long-dormant accounts as new.
- The transaction-count filter is a heuristic, not proof of automation.
- Signer-based activity omits accounts that only receive tokens or act exclusively through relayers.
- Retention alone does not establish revenue, fees, token value, or product-market fit.
