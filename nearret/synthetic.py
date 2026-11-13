"""Synthetic data. ONLY for tests and `rebuild.py --demo`. Never presented as NEAR data."""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

THRESHOLDS = {"all": 10 ** 9, "filtered_200": 200, "filtered_50": 50, "filtered_20": 20}


def monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


def make_params(last_week_start: date, cohort_weeks: int, burn_in_weeks: int, max_weeks: int = 12) -> dict:
    if cohort_weeks < 1:
        raise ValueError("cohort_weeks must be at least 1")
    start = last_week_start - timedelta(weeks=cohort_weeks - 1)
    return {
        "scan_start": (start - timedelta(weeks=burn_in_weeks)).isoformat(),
        "start_date": start.isoformat(),
        "end_date": (last_week_start + timedelta(days=6)).isoformat(),
        "last_week_start": last_week_start.isoformat(),
        "max_weeks": max_weeks,
    }


def synthetic_transactions(params: dict, seed: int = 7, trend: float = 0.06, scale: int = 1, base: float = 0.14):
    """Fake (account, date) transaction rows with a mild upward retention trend."""
    rng = random.Random(seed)
    scan_start = date.fromisoformat(params["scan_start"])
    end = date.fromisoformat(params["end_date"])
    n_weeks = (end - scan_start).days // 7 + 1
    rows, acct_id = [], 0
    for w in range(n_weeks):
        week0 = scan_start + timedelta(weeks=w)
        progress = w / max(1, n_weeks - 1)
        for _ in range(rng.randint(60 * scale, 90 * scale)):
            acct_id += 1
            name = f"acct{acct_id}.near"
            farm = rng.random() < 0.12
            first = week0 + timedelta(days=rng.randint(0, 6))
            n_first = rng.randint(60, 400) if farm else rng.randint(1, 6)
            rows += [(name, first)] * n_first
            p_week = 0 if farm else base + trend * progress
            for k in range(1, 13):
                if rng.random() < p_week * (0.8 ** (k - 1)):
                    d = week0 + timedelta(weeks=k, days=rng.randint(0, 6))
                    if d <= end:
                        rows.append((name, d))
    return rows


def reference_retention(txs, params: dict) -> list:
    """Pure-Python version of sql/retention.sql. Returns (variant, cohort_week, k, active)."""
    scan_start = date.fromisoformat(params["scan_start"])
    start = date.fromisoformat(params["start_date"])
    end = date.fromisoformat(params["end_date"])
    last = date.fromisoformat(params["last_week_start"])
    max_weeks = int(params["max_weeks"])
    weekly = defaultdict(int)
    for acct, d in txs:
        if scan_start <= d <= end:
            weekly[(acct, monday(d))] += 1
    first = {}
    for (acct, wk) in weekly:
        first[acct] = min(first.get(acct, wk), wk)
    counts = defaultdict(int)
    for (acct, wk), _n in weekly.items():
        cohort = first[acct]
        if cohort < start:
            continue
        k = (wk - cohort).days // 7
        if k > max_weeks or (last - cohort).days < k * 7:
            continue
        first_txs = weekly[(acct, cohort)]
        for variant, cap in THRESHOLDS.items():
            if first_txs <= cap:
                counts[(variant, cohort, k)] += 1
    order = list(THRESHOLDS)
    return [(v, c, k, n) for (v, c, k), n in sorted(counts.items(), key=lambda kv: (order.index(kv[0][0]), kv[0][1], kv[0][2]))]


def write_demo(out_dir: Path, last_week_start: date, trend: float = 0.08, seed: int = 7, scale: int = 6) -> None:
    """Write a labelled synthetic retention.csv + run_meta.json into out_dir."""
    params = make_params(last_week_start, cohort_weeks=40, burn_in_weeks=12)
    rows = reference_retention(synthetic_transactions(params, seed=seed, trend=trend, scale=scale, base=0.22), params)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "retention.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["variant", "cohort_week", "k", "accounts_active"])
        for v, c, k, n in rows:
            w.writerow([v, c.isoformat(), k, n])
    (out_dir / "run_meta.json").write_text(json.dumps({
        "synthetic": True,
        "fetched_at_utc": "SYNTHETIC",
        "bytes_processed": 0,
        "params": params,
        "sql_sha256": "n/a",
    }, indent=2))
