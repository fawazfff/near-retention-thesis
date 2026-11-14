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

The pooled rate weights every account equally, so very large cohorts dominate it. The unweighted cohort average gives each weekly cohort equal weight. For the headline filter at week 4, the pooled rate is **0.41%**, while the average of the 36 individual cohort rates is **2.41%**. The median mature cohort contains **18,439 accounts**, while the largest contains **1,660,162**. The five largest cohorts account for **88.4%** of all accounts in the 36 mature cohorts. This concentration means the pooled rate should not be read as a typical week's result. Neither weighting choice explains the cohort-size spikes.

### Method
- Activity means at least one signed transaction (`signer_account_id`) in a Monday-start UTC week.
- A group contains accounts whose first observed signed transaction falls in that week, after a 12-week burn-in.
- Week 4 counts accounts that sign again in the fourth follow-up week.
- Four variants are reported: no filter, and excluding accounts with more than 200, 50, or 20 transactions in their first week. The 50-transaction filter is the headline setting.
- The trend comparison uses the earliest eight and latest eight groups with a complete week-4 observation. It uses one retention rate per group and a Welch confidence interval.

### Investment interpretation

This dataset does not support a confident claim that NEAR's account retention is improving. The observed early-to-late difference is positive, but its 95% interval crosses zero. The pooled result is heavily affected by a handful of unusually large cohorts, and the reason for those spikes is unknown. Treat this as an exploratory usage signal, not evidence of durable customer retention, revenue growth, token value accrual, or an investment recommendation. A stronger thesis would require explaining the cohort spikes, testing alternative definitions of new accounts and activity, and showing the pattern persists in later data.

### Limitations
An account is not necessarily a person. “New” means no signed transaction was observed during the 12-week burn-in, so an older dormant account may look new. The transaction-count filter is a sensitivity check, not proof of automation. Signer-based activity omits accounts that only receive tokens or act only through relayers. Several weekly groups are much larger than the others; the supplied export does not explain why. Retention alone does not establish revenue, fees, token value, or product-market fit.

### Data provenance
Source table named in the supplied query: `bigquery-public-data.crypto_near_mainnet_us.transactions`. The aggregate CSV supplied for this project is stored at `data/retention.csv` and mirrored at `docs/data/retention.csv` for the static dashboard; the query is in `sql/retention.sql`. The upload did not include a BigQuery job ID, execution timestamp, or bytes-processed metadata. Those execution details have not been independently verified here.

The dashboard reads the published CSV. It does not run a new BigQuery query or claim to refresh live chain data.
