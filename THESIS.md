# Does NEAR Keep Its Users?

## NEAR HACKATHON 2026 · Investment Thesis

### Research question
When an account first appears signing transactions on NEAR, does it return to sign transactions in later weeks?

The study groups accounts by the Monday-start UTC week of their first observed signed transaction after a 12-week look-back period.

### Results from the supplied CSV
The supplied file contains 40 weekly groups from 2 February to 2 November 2026. The headline sensitivity filter excludes accounts with more than 50 transactions in their first observed week. This is not a verified bot classifier. 36 groups have enough follow-up to reach week 4.

- Accounts in groups with complete four-week follow-up: 4,627,825
- Accounts that signed again in follow-up week 4: 18,989
- Pooled week-4 return rate: 0.410% (about 4 in every 1,000 accounts)
- Earliest eight-group average: 1.89%
- Latest eight-group average: 3.18%
- Difference: 1.29 percentage points
- Approximate Welch 95% interval: -0.92 to 3.51 percentage points

The interval includes zero. The latest eight groups have a higher average in this sample, but this comparison does not establish that retention improved.

### Filter sensitivity
| Filter | Week-4 returned | Week-4 accounts | Pooled rate | Early-to-recent change |
|---|---:|---:|---:|---:|
| all | 19,657 | 4,630,464 | 0.425% | 1.39 pp |
| filtered_200 | 19,506 | 4,629,912 | 0.421% | 1.36 pp |
| filtered_50 | 18,989 | 4,627,825 | 0.410% | 1.29 pp |
| filtered_20 | 17,288 | 4,622,006 | 0.374% | 1.34 pp |

### Why the pooled rate needs context

The pooled rate weights every account equally, so very large cohorts dominate it. The unweighted cohort average gives each weekly cohort equal weight. For the headline filter at week 4, the pooled rate is **0.41%**, the average cohort rate is **2.41%**, and the median cohort rate is **2.31%**. The median mature cohort contains **18,439 accounts**, while the largest contains **1,660,162**. The five largest cohorts account for **88.4%** of all accounts, but only **24.0%** of week-4 returns. Their pooled week-4 rate is **0.11%**, compared with **2.68%** across the other 31 cohorts. The reason for this difference is unknown. The pooled rate should not be read as a typical week's result.

The same five weeks remain the largest under all first-week transaction thresholds. The >20 filter removes only 3,355 accounts (0.082%) from these five cohorts compared with no filter. That rules out a simple explanation based on accounts signing more than 20 transactions in their first week; it does not rule out one-time or low-frequency automation or campaign activity.

| First observed week | All accounts | After >50 filter | After >20 filter | Week-four active (>50) | Week-four rate |
|---|---:|---:|---:|---:|---:|
| 2026-02-09 | 1,660,185 | 1,660,162 | 1,660,089 | 671 | 0.040% |
| 2026-02-16 | 1,059,473 | 1,059,422 | 1,059,195 | 877 | 0.083% |
| 2026-02-02 | 750,129 | 750,108 | 749,997 | 999 | 0.133% |
| 2026-09-28 | 345,045 | 344,247 | 342,698 | 828 | 0.241% |
| 2026-10-05 | 276,536 | 276,298 | 276,034 | 1,182 | 0.428% |



### Retention across follow-up windows

| Follow-up week | Eligible cohorts | Accounts | Accounts active | Pooled retention |
|---:|---:|---:|---:|---:|
| 1 | 39 | 4,695,104 | 44,255 | 0.943% |
| 4 | 36 | 4,627,825 | 18,989 | 0.410% |
| 8 | 32 | 3,941,854 | 11,345 | 0.288% |
| 12 | 28 | 3,906,626 | 8,007 | 0.205% |

These are exact-week activity measures. The eligible denominator falls at longer horizons because newer cohorts have not yet had enough follow-up time. These numbers do not mean that the same accounts stayed continuously active between weeks 1 and 12.

### Method
- Activity means at least one signed transaction (`signer_account_id`) in a Monday-start UTC week.
- A group contains accounts whose first observed signed transaction falls in that week, after a 12-week burn-in.
- Week 4 counts accounts that sign in that exact fourth follow-up week, not accounts that were active at any point during the first four weeks.
- Four variants are reported: no filter, and excluding accounts with more than 200, 50, or 20 transactions in their first week. The 50-transaction filter is the headline sensitivity setting, not a verified bot classifier.
- The trend comparison uses the earliest eight and latest eight groups with a complete week-4 observation. It uses one retention rate per group and a Welch confidence interval. The 20 middle groups are not part of this endpoint comparison. The interval is exploratory and does not adjust for correlation between adjacent weeks or explain shared shocks.

### Investment interpretation

This dataset does not support a confident claim that NEAR's account retention is improving. The observed early-to-late difference is positive, but its 95% interval crosses zero. The pooled result is heavily affected by a handful of unusually large cohorts, and the reason for those spikes is unknown. Treat this as an exploratory usage signal, not evidence of durable customer retention, revenue growth, token value accrual, or an investment recommendation. A stronger thesis would require explaining the cohort spikes, testing alternative definitions of new accounts and activity, and showing the pattern persists in later data.

### Investment economics and valuation

A dated 14 November 2026 snapshot showed NEAR around **$3.36** and a market capitalization around **$4.40B**. CoinGecko listed about **$107.1M** TVL. DeFiLlama's chain-only NEAR TVL was about **$125.08M**, while its **$276.2M NEAR Protocol Combined** figure includes assets on multiple chains, including Ethereum. Use chain-only figures for a chain TVL multiple. NEAR Intents separately reported about **$176.7M** TVL across 26 chains; this is cross-chain collateral and may overlap with other protocol totals. Do not add these TVL figures together.

NEAR Intents processed about **$3.63B** of DEX volume in 30 days, generated **$5.83M** of fees and captured **$1.81M** of revenue. The wider NEAR Protocol view showed **$5.95M** fees, **$1.93M** protocol revenue and **$1.81M** holders revenue over 30 days. Captured revenue was about **32.4%** of gross fees. DeFiLlama describes holders revenue as captured Intents revenue used to buy back NEAR since 23 February 2026. This is buyback-based value capture, **not a burn**. The 30-day $1.81M holder-revenue figure annualizes mechanically to about $21.7M, around 0.50% of current market capitalization. This is a snapshot, not a guaranteed yield.

Trailing-year DeFiLlama fees were about **$54.14M** and protocol revenue about **$9.64M**. These imply roughly **81× market-cap/fees** and **454× market-cap/revenue**. At the same market capitalization, 100× revenue requires $43.8M a year (4.5× current revenue), 50× requires $87.5M (9.1×), and 25× requires $175M (18.2×). These are arithmetic hurdles, not price targets or justified valuation multiples. The **$3.63B of monthly volume is not revenue**.

As of 14 November 2026, the active maximum annual issuance remains **2.5%**. HSP-029 passed its House of Stake vote to target **1.6%** over 24 months, but the Security Council review, grace period, protocol upgrade and validator adoption still matter. Do not model the target as active before implementation.

HSP-027 and protocol version 87 removed the former 30% developer gas rebate, effective 4 November 2026. Eligible execution fees that previously funded that rebate are now burned. Keep this base-layer gas mechanism separate from NEAR Intents buybacks: one reduces supply, the other purchases tokens on the market.

The 1 October 2026 NEAR Intents exploit is a material product/bridge risk. DeFiLlama reports a $3.8M incident involving Omni deposit/withdrawal infrastructure and the Intents contract. The tracker says the vulnerability was patched and affected users were to be compensated in full. Verify completed reimbursement on-chain. This is not evidence of a NEAR base-layer consensus failure.

**Current valuation status: not yet underwritten.** Retention does not establish revenue. Product volume is not revenue, protocol fees are not automatically holder cash flow, and staking yield can be issuance-funded. A credible valuation needs at least 12 months of comparable protocol fees, product net revenue, net issuance, buybacks, staking participation and market data, plus explicit base, bull and bear cases.

Key risks include incentive-driven or automated activity, application concentration, cross-chain volume that does not create recurring NEAR-denominated revenue, product economics that accrue to operators rather than token holders, issuance dilution, bridge and smart-contract risk, governance changes, liquidity and competition.

Sources: [CoinGecko market data](https://www.coingecko.com/en/coins/near), [DeFiLlama fees, revenue and TVL](https://defillama.com/protocol/near-protocol), [HSP-029 proposal](https://gov.near.org/t/hsp-029-establish-a-24-month-issuance-ramp-to-a-1-6-target-rate-of-near-token-emissions/42644), [HSP-027 ratification](https://houseofstake.org/blog/house-of-stake-update-hsp-027), [nearcore releases](https://github.com/near/nearcore/releases), [NEAR Revenue dashboard](https://revenue.near.org/), [NEAR Foundation tokenomics post](https://near.org/blog/evolving-near-tokenomics).

### Further diligence still outstanding

- **26-week burn-in:** not run. The committed export only supports the 12-week definition. Use `fetch_data.py --burn-in-weeks 26 --output-stem retention_26w`, then `compare_burnin.py`.
- **Application and campaign attribution:** not run. The supplied CSV has cohort aggregates, not account IDs. Schema-check and contract-attribution SQL have been added, but receiver accounts still need to be resolved to verified applications and matched against independently sourced campaign dates.
- **Network economics:** the dated market snapshot is context only. A full supply, fees, revenue, staking and token-holder value-capture series has not yet been calculated.

### Limitations
An account is not necessarily a person. “New” means no signed transaction was observed during the 12-week burn-in, so an older dormant account may look new. The first-week transaction-count filter is a sensitivity check, not a bot classifier. Signer-based activity omits accounts that only receive tokens or act only through relayers. Several weekly groups are much larger than the others; the supplied export does not explain why. Retention alone does not establish revenue, fees, token value, or product-market fit.

### Data provenance
Source table named in the supplied query: `bigquery-public-data.crypto_near_mainnet_us.transactions`. The aggregate CSV supplied for this project is stored at `data/retention.csv` and mirrored at `docs/data/retention.csv` for the static dashboard; the query is in `sql/retention.sql`. The upload did not include a BigQuery job ID, execution timestamp, or bytes-processed metadata. Those execution details have not been independently verified here.

The dashboard reads the published CSV. It does not run a new BigQuery query or claim to refresh live chain data.
