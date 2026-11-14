#!/usr/bin/env python3
"""Compare otherwise identical 12-week and 26-week new-account definitions.

Run after producing data/retention_12w.csv + metadata and
data/retention_26w.csv + metadata with fetch_data.py.
"""
import argparse
import json
from pathlib import Path

from nearret import metrics


def compare(data12, meta12, data26, meta26):
    p12, p26 = meta12["params"], meta26["params"]
    if meta12.get("burn_in_weeks") != 12 or meta26.get("burn_in_weeks") != 26:
        raise ValueError("Expected a 12-week export and a 26-week export; check the metadata files.")
    if p12["start_date"] != p26["start_date"] or p12["last_week_start"] != p26["last_week_start"]:
        raise ValueError("Burn-in exports must use identical cohort start and last-week dates.")
    if p12["max_weeks"] != p26["max_weeks"]:
        raise ValueError("Burn-in exports must use the same maximum follow-up week.")
    out = {
        "method": "Same cohort dates and follow-up horizon; only the no-activity look-back differs.",
        "burn_in_weeks": {"short": 12, "long": 26},
        "cohort_window": {"start_date": p12["start_date"], "last_week_start": p12["last_week_start"]},
        "variants": {},
    }
    for variant in metrics.VARIANT_ORDER:
        c12 = data12[variant]
        c26 = data26[variant]
        weeks12 = [c.week.isoformat() for c in c12]
        weeks26 = [c.week.isoformat() for c in c26]
        if weeks12 != weeks26:
            raise ValueError(f"{variant}: cohort-week sets differ between exports.")
        w12 = metrics.retention_windows(c12)
        w26 = metrics.retention_windows(c26)
        trend12 = metrics.compare_groups(c12)
        trend26 = metrics.compare_groups(c26)
        out["variants"][variant] = {
            "12_week_burn_in": {
                "new_accounts_by_week": {x["week"]: x["accounts"] for x in w12},
                "retention_by_week": [
                    {"week": x["week"], "eligible_cohorts": x["cohorts"],
                     "accounts": x["accounts"], "returned": x["returned"],
                     "retention_percent": x["rate"] * 100}
                    for x in w12
                ],
                "week4_trend": {"early_mean_percent": trend12["early_mean"] * 100,
                                "recent_mean_percent": trend12["recent_mean"] * 100,
                                "change_pp": trend12["diff"] * 100,
                                "interval_pp": [trend12["diff_lo"] * 100, trend12["diff_hi"] * 100],
                                "verdict": trend12["verdict"]},
            },
            "26_week_burn_in": {
                "new_accounts_by_week": {x["week"]: x["accounts"] for x in w26},
                "retention_by_week": [
                    {"week": x["week"], "eligible_cohorts": x["cohorts"],
                     "accounts": x["accounts"], "returned": x["returned"],
                     "retention_percent": x["rate"] * 100}
                    for x in w26
                ],
                "week4_trend": {"early_mean_percent": trend26["early_mean"] * 100,
                                "recent_mean_percent": trend26["recent_mean"] * 100,
                                "change_pp": trend26["diff"] * 100,
                                "interval_pp": [trend26["diff_lo"] * 100, trend26["diff_hi"] * 100],
                                "verdict": trend26["verdict"]},
            },
        }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--short-csv", type=Path, default=Path("data/retention_12w.csv"))
    parser.add_argument("--short-meta", type=Path, default=Path("data/retention_12w_meta.json"))
    parser.add_argument("--long-csv", type=Path, default=Path("data/retention_26w.csv"))
    parser.add_argument("--long-meta", type=Path, default=Path("data/retention_26w_meta.json"))
    parser.add_argument("--output", type=Path, default=Path("data/burnin_comparison.json"))
    args = parser.parse_args()
    short_data, short_meta = metrics.load(args.short_csv, args.short_meta)
    long_data, long_meta = metrics.load(args.long_csv, args.long_meta)
    result = compare(short_data, short_meta, long_data, long_meta)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote burn-in comparison to {args.output}")


if __name__ == "__main__":
    main()
