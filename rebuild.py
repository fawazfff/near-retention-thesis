#!/usr/bin/env python3
"""Rebuild every number, chart and THESIS.md from data/retention.csv.

    python rebuild.py          # real data in data/  -> docs/index.html + THESIS.md
    python rebuild.py --demo   # SYNTHETIC preview   -> demo/index.html + demo/THESIS.md

Standard library only. No Google account needed.
"""
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from nearret import metrics, render, synthetic

ROOT = Path(__file__).parent


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true", help="use clearly labelled SYNTHETIC data (never NEAR data)")
    args = ap.parse_args(argv)

    if args.demo:
        data_dir, out_dir = ROOT / "demo" / "data", ROOT / "demo"
        today = date.today()
        synthetic.write_demo(data_dir, synthetic.monday(today) - timedelta(weeks=1))
    else:
        data_dir, out_dir = ROOT / "data", ROOT / "docs"

    try:
        data, meta = metrics.load(data_dir / "retention.csv", data_dir / "run_meta.json")
        analysis = metrics.analyse(data)
    except (FileNotFoundError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    demo = bool(meta.get("synthetic")) or args.demo
    sql_text = (ROOT / "sql" / "retention.sql").read_text()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render.build_html(analysis, meta, sql_text, demo), encoding="utf-8")
    thesis = render.build_thesis(analysis, meta, ROOT / "templates" / "THESIS.template.md", demo)
    thesis_path = out_dir / "THESIS.md" if demo else ROOT / "THESIS.md"
    thesis_path.write_text(thesis, encoding="utf-8")

    h = analysis["headline"]
    print(("SYNTHETIC DEMO. " if demo else "") +
          f"{render.per100(h['pooled_recent'][0])} of every 100 new accounts still active at week "
          f"{metrics.HEADLINE_WEEK} (latest {h['group_size']} cohorts). Retention: {h['verdict']} "
          f"({render.pp(h['diff'])}, 95% interval {render.pp(h['diff_lo'])} to {render.pp(h['diff_hi'])}).")
    print(f"wrote {out_dir / 'index.html'} and {thesis_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
