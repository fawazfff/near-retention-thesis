#!/usr/bin/env python3
"""Pull retention data from the NEAR public BigQuery dataset into data/.

    python fetch_data.py --project MY_GCP_PROJECT --dry-run     # prints bytes, runs nothing
    python fetch_data.py --project MY_GCP_PROJECT               # runs it (capped by --max-gb)

Needs `pip install google-cloud-bigquery` and a login: `gcloud auth application-default login`.
The free BigQuery sandbox is enough. You only need this to refresh data; judges can rebuild
everything from the committed data/ files with `python rebuild.py`.
"""
import argparse
import csv
import hashlib
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
SQL_PATH = ROOT / "sql" / "retention.sql"
DATA = ROOT / "data"


def window(today: date, cohort_weeks: int, burn_in_weeks: int, max_weeks: int) -> dict:
    """Last complete Monday-start week is the week before the current one."""
    this_monday = today - timedelta(days=today.weekday())
    last_week_start = this_monday - timedelta(weeks=1)
    if cohort_weeks < 19:
        raise ValueError("--cohort-weeks must be at least 19 so 15 cohorts can be compared at week 4")
    if burn_in_weeks < 1:
        raise ValueError("--burn-in-weeks must be at least 1")
    if max_weeks < 4:
        raise ValueError("--max-weeks must be at least 4 because the headline metric is week 4")
    start = last_week_start - timedelta(weeks=cohort_weeks - 1)
    return {
        "scan_start": (start - timedelta(weeks=burn_in_weeks)).isoformat(),
        "start_date": start.isoformat(),
        "end_date": (last_week_start + timedelta(days=6)).isoformat(),
        "last_week_start": last_week_start.isoformat(),
        "max_weeks": max_weeks,
    }


def output_paths(data_dir: Path, stem: str):
    """Keep the canonical default metadata filename compatible with rebuild.py."""
    csv_path = data_dir / f"{stem}.csv"
    meta_path = data_dir / ("run_meta.json" if stem == "retention" else f"{stem}_meta.json")
    return csv_path, meta_path


def with_literals(sql: str, params: dict) -> str:
    """Inline the parameters as literals (fallback if partition pruning ignores parameters)."""
    for k, v in params.items():
        sql = sql.replace("@" + k, str(v) if k == "max_weeks" else f"DATE '{v}'")
    return sql


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", help="your Google Cloud project id (or set GOOGLE_CLOUD_PROJECT)")
    ap.add_argument("--cohort-weeks", type=int, default=40, help="weekly cohorts to analyse (default 40)")
    ap.add_argument("--burn-in-weeks", type=int, default=12, help="weeks before the first cohort used to decide who is new")
    ap.add_argument("--max-weeks", type=int, default=12, help="largest k (weeks since first activity)")
    ap.add_argument("--max-gb", type=float, default=100.0, help="refuse to run, and cap billing, above this many GB")
    ap.add_argument("--dry-run", action="store_true", help="only estimate bytes scanned")
    ap.add_argument("--output-stem", default="retention", help="output filename stem, e.g. retention_26w (default retention)")
    ap.add_argument("--literal-dates", action="store_true",
                    help="inline dates instead of query parameters (use if the dry run scans far more than expected)")
    args = ap.parse_args()

    try:
        from google.cloud import bigquery
    except ImportError:
        print("error: pip install google-cloud-bigquery", file=sys.stderr)
        return 1

    try:
        params = window(datetime.now(timezone.utc).date(), args.cohort_weeks, args.burn_in_weeks, args.max_weeks)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    if not args.output_stem or not all(c.isalnum() or c in "_-" for c in args.output_stem):
        print("error: --output-stem may contain only letters, numbers, _ and -", file=sys.stderr)
        return 2
    template = SQL_PATH.read_text()
    sql = with_literals(template, params) if args.literal_dates else template
    qp = [bigquery.ScalarQueryParameter(k, "DATE", date.fromisoformat(v))
          for k, v in params.items() if k != "max_weeks"]
    qp.append(bigquery.ScalarQueryParameter("max_weeks", "INT64", params["max_weeks"]))
    if args.literal_dates:
        qp = []
    client = bigquery.Client(project=args.project)

    dry = client.query(sql, job_config=bigquery.QueryJobConfig(query_parameters=qp, dry_run=True, use_query_cache=False))
    gb = dry.total_bytes_processed / 1e9
    print(f"This query will process {gb:.1f} GB (window {params['scan_start']} to {params['end_date']}).")
    if args.dry_run:
        return 0
    if gb > args.max_gb:
        print(f"error: {gb:.1f} GB is above --max-gb {args.max_gb}. Lower --cohort-weeks or raise --max-gb.", file=sys.stderr)
        return 1

    cfg = bigquery.QueryJobConfig(query_parameters=qp, maximum_bytes_billed=int(args.max_gb * 1e9))
    job = client.query(sql, job_config=cfg)
    rows = list(job.result())
    DATA.mkdir(exist_ok=True)
    csv_path, meta_path = output_paths(DATA, args.output_stem)
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["variant", "cohort_week", "k", "accounts_active"])
        for r in rows:
            w.writerow([r["variant"], r["cohort_week"].isoformat(), r["k"], r["accounts_active"]])
    meta = {
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "bytes_processed": job.total_bytes_processed,
        "params": params,
        "sql_sha256": hashlib.sha256(template.encode()).hexdigest(),
        "source": "bigquery-public-data.crypto_near_mainnet_us.transactions",
        "rows": len(rows),
        "row_count": len(rows),
        "burn_in_weeks": args.burn_in_weeks,
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    print(f"wrote {len(rows)} rows to {csv_path} with metadata {meta_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
