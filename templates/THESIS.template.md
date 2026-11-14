{{banner}}# Does NEAR keep its users?

## The claim

Of the accounts that first appear on NEAR in a given week, the share that are still active {{week}} weeks later is **improving** over time.

I treat this as a test, not a conclusion. The verdict below is computed from the data and can say "improving", "declining" or "no clear change".

## Verdict: {{verdict}}

The pooled return rate is **{{headline_rate_pct}}** (95% interval {{headline_ci_pct}}) at week {{week}}, measured across the latest {{group}} weekly cohorts ({{recent_span}}) after excluding accounts above the selected first-week transaction threshold.

Week-{{week}} retention was {{early_mean}} in the earliest {{group}} cohorts ({{early_span}}) and is {{recent_mean}} in the latest. Change: {{diff}} (95% interval {{diff_ci}}).

{{verdict_sentence}} {{robust_sentence}}

| Filter | Early mean | Recent mean | Change | 95% interval | Verdict |
|---|---|---|---|---|---|
{{variant_table_rows}}

## Why the pooled rate needs context

The pooled rate weights every account equally, so very large cohorts dominate it. The unweighted cohort average gives each weekly cohort equal weight. For the headline filter at week 4, the pooled rate is **{{pooled_rate}}**, the average cohort rate is **{{mean_cohort_rate}}**, and the median cohort rate is **{{median_cohort_rate}}**. The median mature cohort contains **{{median_cohort_size}}** accounts, while the largest contains **{{max_cohort_size}}**. The five largest cohorts account for **{{top_five_share}}** of all accounts, but only **{{top_five_return_share}}** of week-4 returns. Their pooled week-4 rate is **{{top_five_rate}}**, compared with **{{other_cohorts_rate}}** across the other 31 cohorts. The reason for this difference is unknown. The pooled rate should not be read as a typical week's result.

## Retention across follow-up windows

The denominator changes at each horizon because newer cohorts have not had enough time to reach later weeks. Each row includes only cohorts with a complete observation for that exact week.

| Follow-up week | Eligible cohorts | Accounts | Accounts active | Pooled retention |
|---:|---:|---:|---:|---:|
| 1 | 39 | 4,695,104 | 44,255 | 0.94% |
| 4 | 36 | 4,627,825 | 18,989 | 0.41% |
| 8 | 32 | 3,941,854 | 11,345 | 0.29% |
| 12 | 28 | 3,906,626 | 8,007 | 0.20% |

These are separate exact-week activity measures. They do not mean that an account remained continuously active from week 1 through week 12.

## Why retention

Raw new-account counts can be affected by automation, incentive campaigns and short-lived activity. Accounts that keep coming back provide a stronger usage signal than a first transaction alone, although repeat activity does not prove human use. This study measures returning signers and compares retention with cohort size. It cannot identify which accounts belong to real people.

## Definitions (fixed before pulling any data)

- **Active**: the account signed at least one transaction (`signer_account_id`) in a Monday-start UTC week.
- **New account**: first signed transaction falls in the cohort week, and it signed nothing in the burn-in period {{burn_in}}.
- **Retention at week k**: share of a cohort that signed in that exact k-th follow-up week, not the share that was active at any time during the weeks before it.
- **Headline filter** (`{{headline_variant}}`): exclude accounts that signed more than 50 transactions in their first observed week. This is a sensitivity check only. Thresholds of 20 and 200 and no filter are reported too.
- **Trend test**: compare the {{group}} earliest and {{group}} latest cohorts with a complete week-{{week}} observation, using one retention rate per cohort (Welch interval). The middle cohorts are not included in this endpoint comparison. The interval is exploratory and does not adjust for correlation between adjacent weeks or shared shocks. A change counts only if its interval excludes zero and is at least {{min_effect}} percentage point.

## Investment interpretation

This dataset does not support a confident claim that NEAR's account retention is improving. The observed early-to-late difference is positive, but its 95% interval crosses zero. The pooled result is heavily affected by a handful of unusually large cohorts, and the reason for those spikes is unknown. Treat this as an exploratory usage signal, not evidence of durable customer retention, revenue growth, token value accrual, or an investment recommendation. A stronger thesis would require explaining the cohort spikes, testing alternative new-account definitions and activity measures, and showing the pattern persists in later data.

## Investment economics and valuation

A dated CoinGecko snapshot on 14 November 2026 showed NEAR around **$3.36**, market capitalization around **$4.40 billion**, FDV around **$4.40 billion**, circulating supply around **1.312 billion NEAR**, TVL around **$107.1 million**, and a market-cap/TVL ratio around **41.1×**. These are third-party snapshot figures, not a valuation conclusion. A one-day fee or revenue figure is not a sustainable annual run rate.

NEAR's February 2026 tokenomics post describes a reduction in maximum annual issuance to **2.5%** and new product-revenue capture mechanisms. The base transaction fee mechanism is described as 70% burn and 30% contract rebate. These mechanisms need to be reconciled against live governance decisions, issuance, fee burn and verified buyback transactions before estimating net supply effects or holder value capture.

**Current valuation status: not yet underwritten.** Retention does not establish revenue. Product volume is not revenue, protocol fees are not automatically holder cash flow, and staking yield can be issuance-funded. A credible valuation needs at least 12 months of comparable protocol fees, product net revenue, net issuance, buybacks, staking participation and market data, plus explicit base, bull and bear cases.

Key risks include incentive-driven or automated activity, application concentration, cross-chain volume that does not create recurring NEAR-denominated revenue, product economics that accrue to operators rather than token holders, issuance dilution, bridge and smart-contract risk, governance changes, liquidity and competition.

Sources: [CoinGecko market and financial data](https://www.coingecko.com/en/coins/near), [NEAR Foundation tokenomics post (24 February 2026)](https://near.org/blog/evolving-near-tokenomics), [SEC filing (16 September 2026)](https://www.sec.gov/Archives/edgar/data/2067111/000119312526393240/ck0002067111-20260916.htm).

## Further diligence still outstanding

- **26-week burn-in:** not run. The committed export only supports the 12-week definition. Use `fetch_data.py --burn-in-weeks 26 --output-stem retention_26w`, then `compare_burnin.py`.
- **Application and campaign attribution:** not run. The supplied CSV has cohort aggregates, not account IDs. Schema-check and contract-attribution SQL have been added, but receiver accounts still need to be resolved to verified applications and matched against independently sourced campaign dates.
- **Network economics:** the dated market snapshot is context only. A full supply, fees, revenue, staking and token-holder value-capture series has not yet been calculated.

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
- `python rebuild.py` regenerates this thesis from `data/retention.csv` and preserves the designed `docs/index.html`. Use `python rebuild.py --overwrite-dashboard` only if you intentionally want the simpler generated report page.
- `python fetch_data.py` re-queries BigQuery (see README).
