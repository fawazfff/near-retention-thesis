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

The same five weeks remain the largest under all first-week transaction thresholds. The >20 filter removes only 3,355 accounts (0.082%) from these five cohorts compared with no filter. That rules out a simple explanation based on accounts signing more than 20 transactions in their first week; it does not rule out one-time or low-frequency automation or campaign activity.

| First observed week | All accounts | After >50 filter | After >20 filter | Week-four active (>50) | Week-four rate |
|---|---:|---:|---:|---:|---:|
{{top_five_rows}}



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

A dated 14 November 2026 snapshot showed NEAR around **$3.36** and a market capitalization around **$4.40B**. CoinGecko listed about **$107.1M** TVL. DeFiLlama's chain-only NEAR TVL was about **$125.08M**, while its **$276.2M NEAR Protocol Combined** figure includes assets on multiple chains, including Ethereum. Use chain-only figures for a chain TVL multiple. NEAR Intents separately reported about **$176.7M** TVL across 26 chains; this is cross-chain collateral and may overlap with other protocol totals. Do not add these TVL figures together.

NEAR Intents processed about **$3.63B** of DEX volume in 30 days, generated **$5.83M** of fees and captured **$1.81M** of revenue. The wider NEAR Protocol view showed **$5.95M** fees, **$1.93M** protocol revenue and **$1.81M** holders revenue over 30 days. Captured revenue was about **32.4%** of gross fees. DeFiLlama describes holders revenue as captured Intents revenue used to buy back NEAR since 23 February 2026. This is buyback-based value capture, **not a burn**. The 30-day $1.81M holder-revenue figure annualizes mechanically to about $21.7M, around 0.50% of current market capitalization. This is a snapshot, not a guaranteed yield.

Trailing-year DeFiLlama fees were about **$54.14M** and protocol revenue about **$9.64M**. These imply roughly **81× market-cap/fees** and **454× market-cap/revenue**. At the same market capitalization, 100× revenue requires $43.8M a year (4.5× current revenue), 50× requires $87.5M (9.1×), and 25× requires $175M (18.2×). These are arithmetic hurdles, not price targets or justified valuation multiples. The **$3.63B of monthly volume is not revenue**.

As of 14 November 2026, the active maximum annual issuance remains **2.5%**. HSP-029 passed its House of Stake vote to target **1.6%** over 24 months, but the Security Council review, grace period, protocol upgrade and validator adoption still matter. Do not model the target as active before implementation.

HSP-027 and protocol version 87 removed the former 30% developer gas rebate, effective 4 November 2026. Eligible execution fees that previously funded that rebate are now burned. Keep this base-layer gas mechanism separate from NEAR Intents buybacks: one reduces supply, the other purchases tokens on the market. A recent chain-data analysis estimated about **88,000 NEAR issued per day** versus **890 NEAR burned per day** in the first eight days after protocol version 87 took effect on 4 November. That is roughly **1% of issuance** offset by gas burn at those observed rates. The sample is short, but it shows that 100% of eligible gas being burned does not mean NEAR is deflationary. Net issuance remains strongly positive at the observed rate. [Unlocks Insights, 13 November 2026](https://insights.unlocks.app/near-halved-its-inflation-a-year-ago-the-chain-shows-the-cut-held/).

The 1 October 2026 NEAR Intents exploit is a material product/security-control risk. The 16 October postmortem says the root cause was a deposit-notification bug in the NEAR Intents contract, not an Omni bridge bug. Twenty-three failed notifications created unbacked internal balances. The team says all funds were returned on 2 October and affected users were made whole. The notification feature was removed on 7 October after another critical report. The reported recovery reduces the direct financial loss, but the incident exposed weaknesses in contract accounting and monitoring. It is not evidence of a NEAR base-layer consensus failure.


### Base, bull and bear evidence framework

| Case | Evidence that would support it | What would invalidate it |
|---|---|---|
| Bear | NEAR Intents revenue falls, captured buybacks fade, gas burn remains around 1% of issuance, and adjusted cohort retention remains weak or concentrated | Sustained product revenue, broader recurring users, and a materially higher share of issuance offset by burn/buybacks |
| Base | Intents continues to capture meaningful fees, but token capture remains modest; issuance still exceeds burn; user retention is mixed | Revenue growth stalls or the 26-week cohort definition removes much of the apparent user base |
| Bull | Recurring annual captured revenue approaches $87.5M (the arithmetic hurdle for 50× revenue at today's market cap), buybacks are verified, issuance falls after implementation, and repeat usage broadens beyond a few cohorts/apps | Buybacks are one-off, product revenue accrues elsewhere, or retention gains disappear after outlier and campaign adjustments |

These are evidence conditions, not forecasts or price targets. The 50× hurdle is not a claim that 50× is the right multiple. It simply shows the scale of revenue needed to make the current market capitalization less demanding under a conventional revenue-multiple lens.

**Current valuation status: not yet underwritten.** Retention does not establish revenue. Product volume is not revenue, protocol fees are not automatically holder cash flow, and staking yield can be issuance-funded. A credible valuation needs at least 12 months of comparable protocol fees, product net revenue, net issuance, buybacks, staking participation and market data, plus explicit base, bull and bear cases.

Key risks include incentive-driven or automated activity, application concentration, cross-chain volume that does not create recurring NEAR-denominated revenue, product economics that accrue to operators rather than token holders, issuance dilution, bridge and smart-contract risk, governance changes, liquidity and competition.

Sources: [CoinGecko market data](https://www.coingecko.com/en/coins/near), [DeFiLlama fees, revenue and TVL](https://defillama.com/protocol/near-protocol), [DeFiLlama NEAR Intents](https://defillama.com/protocol/near-intents), [DeFiLlama NEAR chain TVL](https://defillama.com/chains/NEAR), [DeFiLlama holders revenue](https://defillama.com/holders-revenue/chain/near), [NEAR Intents postmortem](https://x.com/AlexAuroraDev/status/2106049685928677585), [deposit-notification removal](https://github.com/near/intents/pull/374), [HSP-029 proposal](https://gov.near.org/t/hsp-029-establish-a-24-month-issuance-ramp-to-a-1-6-target-rate-of-near-token-emissions/42644), [HSP-027 ratification](https://houseofstake.org/blog/house-of-stake-update-hsp-027-ratified), [nearcore releases](https://github.com/near/nearcore/releases), [NEAR Revenue dashboard](https://revenue.near.org/), [NEAR Foundation tokenomics post](https://near.org/blog/evolving-near-tokenomics).

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
