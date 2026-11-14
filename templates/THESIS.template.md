{{banner}}# Does NEAR keep its users?

## The claim

Of the accounts that first appear on NEAR in a given week, the share that are still active {{week}} weeks later is **improving** over time.

I treat this as a test, not a conclusion. The verdict below is computed from the data and can say "improving", "declining" or "no clear change".

## Verdict: {{verdict}}

About **{{headline_per100}} of every 100** new accounts are still active {{week}} weeks later (95% interval {{headline_ci}} per 100), measured on the latest {{group}} weekly cohorts ({{recent_span}}) after removing accounts above the selected first-week transaction threshold.

Week-{{week}} retention was {{early_mean}} in the earliest {{group}} cohorts ({{early_span}}) and is {{recent_mean}} in the latest. Change: {{diff}} (95% interval {{diff_ci}}).

{{verdict_sentence}} {{robust_sentence}}

| Filter | Early mean | Recent mean | Change | 95% interval | Verdict |
|---|---|---|---|---|---|
{{variant_table_rows}}

## Why retention

New-account counts are cheap to inflate with bots and airdrop farming. Accounts that keep coming back are a stronger sign of usage than a raw count, though bots can come back too. So I measure retention directly and put it next to new-account volume, so the two can be compared. I cannot prove which accounts are real users, only how many keep signing transactions.

## Definitions (fixed before pulling any data)

- **Active**: the account signed at least one transaction (`signer_account_id`) in a Monday-start UTC week.
- **New account**: first signed transaction falls in the cohort week, and it signed nothing in the burn-in period {{burn_in}}.
- **Retention at week k**: share of a cohort that signed again in the k-th week after its cohort week.
- **Headline filter** (`{{headline_variant}}`): exclude accounts that signed more than 50 transactions in their first observed week. This is a sensitivity check only. Thresholds of 20 and 200 and no filter are reported too.
- **Trend test**: compare the {{group}} earliest and {{group}} latest cohorts using one retention number per weekly cohort (Welch interval). A change counts only if its interval excludes zero and it is at least {{min_effect}} percentage point.

## Investment interpretation

This dataset does not support a confident claim that NEAR's account retention is improving. The observed early-to-late difference is positive, but its 95% interval crosses zero. The pooled result is heavily affected by a handful of unusually large cohorts, and the reason for those spikes is unknown. Treat this as an exploratory usage signal, not evidence of durable customer retention, revenue growth, token value accrual, or an investment recommendation. A stronger thesis would require explaining the cohort spikes, testing alternative new-account definitions and activity measures, and showing the pattern persists in later data.

## Evidence for

{{evidence_for}}

## Evidence against, or limiting it

{{evidence_against}}

## What would change my mind

- A stricter "new account" definition (for example a 26-week burn-in instead of 12) that reverses the sign of the change. I did not run it.
- The effect disappearing once accounts tied to a single app or campaign are excluded. I did not run it.
- A later re-run, with more cohorts, that moves the verdict back to "no clear change".
- A measure of activity that includes relayed transactions and receiving accounts pointing the other way.

## What I could not compute

- Users who act only through relayers (meta-transactions) or only receive tokens are invisible, because the data here counts transaction signers.
- Whether an account is a human. The filter is a proxy.
- Any link to price, fees paid or value per user.
- Account creation dates. "First signed transaction" stands in for them.

## Data and reproduction

- Source: `bigquery-public-data.crypto_near_mainnet_us.transactions` (columns `block_date`, `signer_account_id`).
- Cohort weeks: {{window}}. This analysis uses the supplied aggregate BigQuery CSV export. Its BigQuery job ID, query execution timestamp, bytes processed and query hash were not included, so they are not claimed or inferred. The calculations can be reproduced from the CSV without rerunning BigQuery.
- `python rebuild.py` regenerates this file, `docs/index.html` and every number from `data/retention.csv`. No Google account is needed for that.
- `python fetch_data.py` re-queries BigQuery (see README).
