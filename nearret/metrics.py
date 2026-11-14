"""Retention metrics. Standard library only.

Everything the dashboard and THESIS.md say is computed here from data/retention.csv.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

VARIANT_ORDER = ["all", "filtered_200", "filtered_50", "filtered_20"]
# Fixed before any data was pulled, so the headline cannot be cherry-picked.
HEADLINE_VARIANT = "filtered_50"
HEADLINE_WEEK = 4
MIN_EFFECT = 0.01  # smallest change (1 percentage point) we call a real change
MAX_GROUP = 8      # cohorts per comparison group (earliest vs latest)
MIN_GROUP = 5

# Two-sided 95% Student-t critical values, keyed by degrees of freedom.
_T95 = {5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201,
        12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 18: 2.101,
        20: 2.086, 25: 2.060, 30: 2.042}


def t_crit(df: float) -> float:
    """Conservative: use the tabulated value at or below df."""
    usable = [k for k in _T95 if k <= df]
    return _T95[max(usable)] if usable else _T95[5]


def wilson(x: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Point estimate and Wilson score interval for a proportion."""
    if n <= 0:
        return (math.nan, math.nan, math.nan)
    p = x / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (p, max(0.0, centre - half), min(1.0, centre + half))


@dataclass
class Cohort:
    week: date
    size: int
    retained: dict  # k -> accounts active in week cohort+k (zero-filled when observed)

    def p(self, k: int) -> float:
        return self.retained[k] / self.size


def load(csv_path: Path, meta_path: Path):
    """Return (data, meta) where data[variant] is a list of Cohort sorted by week."""
    if not csv_path.exists() or not meta_path.exists():
        raise FileNotFoundError(
            f"Missing {csv_path} or {meta_path}. Run `python fetch_data.py` first "
            "(needs a Google Cloud login), or `python rebuild.py --demo` for a "
            "clearly labelled synthetic preview."
        )
    meta = json.loads(meta_path.read_text())
    last_week_start = date.fromisoformat(meta["params"]["last_week_start"])
    max_weeks = int(meta["params"]["max_weeks"])

    raw: dict = {}
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        need = {"variant", "cohort_week", "k", "accounts_active"}
        if not need <= set(reader.fieldnames or []):
            raise ValueError(f"{csv_path} must have columns {sorted(need)}")
        for row in reader:
            wk = date.fromisoformat(row["cohort_week"])
            raw.setdefault(row["variant"], {}).setdefault(wk, {})[int(row["k"])] = int(
                row["accounts_active"]
            )

    data = {}
    for variant, weeks in raw.items():
        cohorts = []
        for wk, ks in sorted(weeks.items()):
            if 0 not in ks:
                raise ValueError(f"{variant} {wk}: no k=0 row, cohort size unknown")
            size = ks[0]
            span = (last_week_start - wk).days // 7
            retained = {k: ks.get(k, 0) for k in range(0, min(max_weeks, span) + 1)}
            cohorts.append(Cohort(wk, size, retained))
        data[variant] = cohorts
    missing = [v for v in VARIANT_ORDER if v not in data]
    if missing:
        raise ValueError(f"retention.csv is missing variants: {missing}")
    return data, meta


def _mean(xs):
    return sum(xs) / len(xs)


def _sd(xs):
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def compare_groups(cohorts: list, k: int = HEADLINE_WEEK) -> dict:
    """Earliest vs latest cohorts that are observed at week k.

    The test works on cohort-level retention (one number per weekly cohort), because
    week-to-week swings (campaigns, airdrops) are far bigger than sampling error.
    """
    obs = [c for c in cohorts if k in c.retained]
    g = min(MAX_GROUP, len(obs) // 3)
    if g < MIN_GROUP:
        raise ValueError(
            f"Only {len(obs)} cohorts are observed at week {k}; need at least "
            f"{3 * MIN_GROUP}. Fetch a longer window (--cohort-weeks)."
        )
    early, recent = obs[:g], obs[-g:]
    pe = [c.p(k) for c in early]
    pr = [c.p(k) for c in recent]
    me, mr = _mean(pe), _mean(pr)
    ve, vr = _sd(pe) ** 2 / g, _sd(pr) ** 2 / g
    se = math.sqrt(ve + vr)
    if se == 0:
        df, tc = float("inf"), 1.96
    else:
        df = (ve + vr) ** 2 / (ve ** 2 / (g - 1) + vr ** 2 / (g - 1))
        tc = t_crit(df)
    diff = mr - me
    lo, hi = diff - tc * se, diff + tc * se
    if lo > 0 and diff >= MIN_EFFECT:
        verdict = "improving"
    elif hi < 0 and diff <= -MIN_EFFECT:
        verdict = "declining"
    else:
        verdict = "no clear change"
    pooled_e = wilson(sum(c.retained[k] for c in early), sum(c.size for c in early))
    pooled_r = wilson(sum(c.retained[k] for c in recent), sum(c.size for c in recent))
    return {
        "k": k, "group_size": g, "early": early, "recent": recent,
        "early_mean": me, "recent_mean": mr, "diff": diff, "diff_lo": lo, "diff_hi": hi,
        "pooled_early": pooled_e, "pooled_recent": pooled_r, "verdict": verdict,
        "early_span": (early[0].week, early[-1].week),
        "recent_span": (recent[0].week, recent[-1].week),
        "new_accounts_early": _mean([c.size for c in early]),
        "new_accounts_recent": _mean([c.size for c in recent]),
        "kept_early": _mean([c.retained[k] for c in early]),
        "kept_recent": _mean([c.retained[k] for c in recent]),
    }


def curve(group: list) -> list:
    """Pooled retention by week for a group, only for weeks observed in every cohort."""
    out = []
    k = 0
    while all(k in c.retained for c in group):
        out.append((k, sum(c.retained[k] for c in group) / sum(c.size for c in group)))
        k += 1
    return out


def cohort_series(cohorts: list, k: int = HEADLINE_WEEK) -> list:
    """(week, p, lo, hi) per cohort observed at week k."""
    rows = []
    for c in cohorts:
        if k in c.retained:
            p, lo, hi = wilson(c.retained[k], c.size)
            rows.append((c.week, p, lo, hi))
    return rows


def farm_share(all_cohorts: list, filtered: list) -> dict:
    """Share of new accounts removed by the headline filter, per cohort week."""
    kept = {c.week: c.size for c in filtered}
    return {c.week: 1 - kept.get(c.week, 0) / c.size for c in all_cohorts if c.size}


def analyse(data: dict) -> dict:
    """Run the comparison for every variant plus the supporting numbers."""
    results = {v: compare_groups(data[v]) for v in VARIANT_ORDER}
    head = results[HEADLINE_VARIANT]
    share = farm_share(data["all"], data[HEADLINE_VARIANT])
    early_weeks = {c.week for c in head["early"]}
    recent_weeks = {c.week for c in head["recent"]}
    share_early = _mean([v for w, v in share.items() if w in early_weeks])
    share_recent = _mean([v for w, v in share.items() if w in recent_weeks])
    verdicts = {v: results[v]["verdict"] for v in VARIANT_ORDER}
    mature = [c for c in data[HEADLINE_VARIANT] if HEADLINE_WEEK in c.retained]
    sizes = sorted(c.size for c in mature)
    total_accounts = sum(sizes)
    top_five = sorted(mature, key=lambda c: c.size, reverse=True)[:5]
    diagnostics = {
        "mature_cohorts": len(mature),
        "total_accounts": total_accounts,
        "total_returned": sum(c.retained[HEADLINE_WEEK] for c in mature),
        "pooled_rate": sum(c.retained[HEADLINE_WEEK] for c in mature) / total_accounts,
        "mean_cohort_rate": _mean([c.p(HEADLINE_WEEK) for c in mature]),
        "median_cohort_size": (sizes[(len(sizes) - 1) // 2] + sizes[len(sizes) // 2]) / 2,
        "max_cohort_size": max(sizes),
        "top_five_share": sum(c.size for c in top_five) / total_accounts,
    }
    return {
        "cohort_diagnostics": diagnostics,
        "variants": results,
        "headline": head,
        "robust": len(set(verdicts.values())) == 1,
        "verdicts": verdicts,
        "farm_share_early": share_early,
        "farm_share_recent": share_recent,
        "curve_early": curve(head["early"]),
        "curve_recent": curve(head["recent"]),
        "series_headline": cohort_series(data[HEADLINE_VARIANT]),
        "series_all": cohort_series(data["all"]),
    }


def last_complete_week(meta: dict) -> date:
    return date.fromisoformat(meta["params"]["last_week_start"]) + timedelta(days=6)
