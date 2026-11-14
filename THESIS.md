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

### Method
- Activity means at least one signed transaction (`signer_account_id`) in a Monday-start UTC week.
- A group contains accounts whose first observed signed transaction falls in that week, after a 12-week burn-in.
- Week 4 counts accounts that sign in that exact fourth follow-up week, not accounts that were active at any point during the first four weeks.
- Four variants are reported: no filter, and excluding accounts with more than 200, 50, or 20 transactions in their first week. The 50-transaction filter is the headline sensitivity setting, not a verified bot classifier.
- The trend comparison uses the earliest eight and latest eight groups with a complete week-4 observation. It uses one retention rate per group and a Welch confidence interval. The 20 middle groups are not part of this endpoint comparison. The interval is exploratory and does not adjust for correlation between adjacent weeks or explain shared shocks.

### Investment interpretation

This dataset does not support a confident claim that NEAR's account retention is improving. The observed early-to-late difference is positive, but its 95% interval crosses zero. The pooled result is heavily affected by a handful of unusually large cohorts, and the reason for those spikes is unknown. Treat this as an exploratory usage signal, not evidence of durable customer retention, revenue growth, token value accrual, or an investment recommendation. A stronger thesis would require explaining the cohort spikes, testing alternative definitions of new accounts and activity, and showing the pattern persists in later data.

### Investment economics and valuation

A dated CoinGecko snapshot on 14 November 2026 showed NEAR around **$3.36**, market capitalization around **$4.40 billion**, FDV around **$4.40 billion**, circulating supply around **1.312 billion NEAR**, and TVL around **$107.1 million**. DeFiLlama reported a materially different **$276.2 million TVL** on the same date. This changes the market-cap/TVL ratio from about **41×** to about **16×**. The provider difference must be reconciled before using TVL as a valuation denominator.

DeFiLlama reported approximately **$5.95 million fees** and **$1.93 million protocol revenue** over 30 days, with trailing-year figures of **$54.14 million fees** and **$9.64 million revenue**. At a roughly $4.38 billion market cap, these imply about **81× market-cap/trailing-year fees** and **454× market-cap/trailing-year revenue**. These are screening multiples, not a fair-value model. Product attribution, costs, and what reaches NEAR tokenholders still need verification. A single 24-hour figure must not be multiplied by 365 and treated as sustainable annual revenue.

As of 14 November 2026, the active maximum annual issuance remains **2.5%**. House of Stake proposal HSP-029 passed its vote on 2 November and proposes a linear 24-month reduction to **1.6%**, but the Security Council veto window runs through 16 November and protocol implementation/validator adoption is still required. Do not model 1.6% as already active.

The developer gas rebate was removed under HSP-027 and protocol version 87, activated on **4 November 2026**. Eligible execution gas that previously generated a 30% contract rebate is now fully burned. This is a change from the older 70% burn / 30% developer-rebate model. Confirm live protocol parameters and distinguish fee components before modelling.

NEAR's February 2026 tokenomics post describes product-revenue capture and buyback mechanisms. Verify governance status, on-chain transfers and realized token amounts before treating buybacks or revenue capture as completed. The NEAR Revenue dashboard provides a live source to reconcile product fees, net revenue, emissions and buybacks.



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
