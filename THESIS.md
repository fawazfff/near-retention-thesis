# Does NEAR Keep Its Users?

**Track:** Investment Thesis  
**Status:** Research in progress  
**Last updated:** Not yet generated from verified data

## Executive question

Of the accounts first observed on NEAR, what share returns to make another qualifying transaction after 14 and 30 days? Is that share improving across cohorts?

## Current conclusion

No conclusion is published yet. The live BigQuery schema and query costs must be verified before calculating retention. This document will be generated from the same metrics artifact as the dashboard so that narrative and charts cannot drift apart.

## Hypothesis

NEAR's account retention may be improving over time. If the share of newly active accounts that return for another qualifying transaction rises across comparable cohorts, that would be a stronger signal of recurring network usage than new-account counts alone.

## Measurement plan

- Define first qualifying activity from verified source columns.
- Group accounts by first-activity week.
- Calculate 14-day and 30-day return rates only for cohorts with complete observation windows.
- Report all-account results and a separately documented automation sensitivity filter.
- Publish query text, schema, cost estimates, data coverage, and limitations.

## Limitations

On-chain account activity is not the same as unique human activity. One person may control multiple accounts, and an account may interact with applications in ways that are not captured by the selected event definition. Heuristic automation filters can misclassify legitimate activity.

## Reproducibility

The final version of this document will be rendered from `data/metrics.json`. Until then, no numerical claims are made.
