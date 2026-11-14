# Investigating the five unusually large NEAR cohorts

**Status:** aggregate-data investigation completed; application and campaign attribution still requires account-level BigQuery results.

## Finding

The supplied CSV contains 40 weekly cohorts, from 2 February through 2 November 2026. Under the headline `filtered_50` definition, 36 cohorts have a complete week-four observation.

The five largest cohorts contain **4,090,237 of 4,627,825 accounts (88.38%)**, but only **4,557 of 18,989 week-four returners (24.00%)**. Their pooled week-four rate is **0.111%**. The other 31 mature cohorts have a pooled week-four rate of **2.685%**.

The first three February cohorts alone contain **3,469,692 accounts (74.97% of the mature denominator)** and have a combined week-four rate of **0.073%**. The size spikes are therefore not a small tail effect: they dominate the pooled retention calculation.

## Five largest cohorts

| First observed week | Accounts, >50 filter | Week-four active | Week-four rate |
|---|---:|---:|---:|
| 9 Feb 2026 | 1,660,162 | 671 | 0.040% |
| 16 Feb 2026 | 1,059,422 | 877 | 0.083% |
| 2 Feb 2026 | 750,108 | 999 | 0.133% |
| 28 Sep 2026 | 344,247 | 828 | 0.241% |
| 5 Oct 2026 | 276,298 | 1,182 | 0.428% |

The rates are exact-week returns, not continuous four-week retention.

## Does the high-activity filter explain the spikes?

No. The same five weeks remain the largest under all four variants.

| First observed week | All accounts | >200 first-week tx filter | >50 filter | >20 filter |
|---|---:|---:|---:|---:|
| 9 Feb 2026 | 1,660,185 | 1,660,182 | 1,660,162 | 1,660,089 |
| 16 Feb 2026 | 1,059,473 | 1,059,469 | 1,059,422 | 1,059,195 |
| 2 Feb 2026 | 750,129 | 750,128 | 750,108 | 749,997 |
| 28 Sep 2026 | 345,045 | 344,913 | 344,247 | 342,698 |
| 5 Oct 2026 | 276,536 | 276,408 | 276,298 | 276,034 |

Across these five weeks, the all-accounts variant has 4,091,368 accounts, compared with 4,088,013 under the >20 filter. That removes only **3,355 accounts (0.082%)**. The >50 filter removes 1,131 accounts (0.028%).

This rules out only one narrow explanation: that a large share of the spike is made up of accounts signing more than 20 transactions in their first week. It does **not** rule out one-time bots, low-frequency automation, faucet or airdrop claims, incentive campaigns, bulk account creation, or other short-lived activity.

## Why this matters for the investment case

The headline pooled week-four retention rate is **0.410%**. It is mathematically correct for the supplied filtered-50 export, but it is not representative of a typical cohort because three February groups dominate the denominator.

For context:
- Pooled rate across all 36 mature cohorts: **0.410%**.
- Unweighted mean of cohort rates: **2.413%**.
- Median cohort rate: **2.315%**.
- Pooled rate across the five largest cohorts: **0.111%**.
- Pooled rate across the other 31 cohorts: **2.685%**.

The mean and median answer a different question from the pooled rate. Neither should silently replace the other. Report both, explain their weighting, and keep the five outliers visible.

The current dataset cannot establish that these are bots or identify the applications behind them. It contains aggregate counts by cohort and follow-up week, not account IDs, transaction hashes, receiver accounts, campaign labels or application names.

## Required attribution work

1. Run `sql/near_schema_check.sql` in BigQuery. Confirm the exact column names and data types in `transactions` and `receipts`. Do not assume the receipt join fields exist.
2. Run a BigQuery dry-run for `sql/contract_attribution.sql`. Check estimated bytes and the maximum billing cap before executing it.
3. Execute the attribution query only after the schema check confirms the join fields. It currently counts receiver interactions from cohort signers and includes all receipt kinds. It is not yet a verified function-call-only query.
4. Resolve high-frequency receiver accounts to verified deployed contracts using account/code metadata and public ecosystem directories. Do not infer a project name from an account string.
5. Compare first-seen and activity dates with public launch, points, faucet, grant, airdrop and incentive campaign dates. A date coincidence is a lead, not proof of causation.
6. Quantify concentration: share of cohort signers and receipts accounted for by the top 5, 10 and 20 receivers, separately for each outlier cohort and for the rest of the sample.
7. Recalculate retention excluding identified campaign or application activity only when the attribution rule is independently documented and reproducible. Publish both original and adjusted results.

## Interpretation to use until attribution is complete

The February cohorts create a severe denominator and composition issue. The existing high-transaction filters do not resolve it. This weakens the use of the pooled rate as a standalone signal of durable user adoption. It does not by itself prove the underlying activity was artificial, nor does it show which application or campaign caused it.

**Investment implication:** do not claim improving user retention or broad-based adoption from the aggregate cohort totals until the February spike is explained and the result is robust to the 26-week burn-in definition and application-level concentration checks.

## Reproduction

The calculations in this note are derived from `docs/data/retention.csv`, using the `filtered_50` variant for the headline cohort table and all four variants for the threshold comparison. The source export's BigQuery job ID, execution timestamp and bytes processed were not supplied. The figures can be recalculated from the committed CSV, but this note does not claim an independent BigQuery rerun.
