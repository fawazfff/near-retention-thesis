"""Render docs/index.html and THESIS.md. Every number comes from metrics.analyse()."""
from __future__ import annotations

import re
from datetime import date
from html import escape
from pathlib import Path

from . import charts
from .metrics import HEADLINE_VARIANT, HEADLINE_WEEK, MIN_EFFECT, VARIANT_ORDER, last_complete_week

LABELS = {
    "all": "No filter",
    "filtered_200": "Drop accounts with more than 200 transactions in week 1",
    "filtered_50": "Drop accounts with more than 50 transactions in week 1 (headline)",
    "filtered_20": "Drop accounts with more than 20 transactions in week 1",
}


def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


def pp(x, d=1):
    return f"{x * 100:+.{d}f} pp"


def day(d):
    return d.strftime("%-d %b %Y")


def span(s):
    return f"{day(s[0])} to {day(s[1])}"



def verdict_sentence(h):
    v = h["verdict"]
    if v == "improving":
        return ("Week-4 retention is higher in the latest cohorts than in the earliest ones, "
                "and the gap is larger than normal week-to-week swings.")
    if v == "declining":
        return ("Week-4 retention is lower in the latest cohorts than in the earliest ones, "
                "and the gap is larger than normal week-to-week swings.")
    return ("I cannot show that week-4 retention changed: the difference is inside normal "
            "week-to-week swings or smaller than 1 percentage point.")


def evidence(a):
    """(for, against) bullet lists for the claim 'retention is improving'."""
    h, vs = a["headline"], a["variants"]
    good, bad = [], []
    k = HEADLINE_WEEK
    line = (f"Week-{k} retention went from {pct(h['early_mean'])} (earliest {h['group_size']} cohorts, "
            f"{span(h['early_span'])}) to {pct(h['recent_mean'])} (latest {h['group_size']} cohorts, "
            f"{span(h['recent_span'])}): {pp(h['diff'])}, 95% interval {pp(h['diff_lo'])} to {pp(h['diff_hi'])}.")
    (good if h["diff"] > 0 else bad).append(line)
    up = [v for v in VARIANT_ORDER if vs[v]["diff"] > 0]
    if len(up) == len(VARIANT_ORDER):
        good.append("The direction is positive under all four filter settings.")
    elif up:
        bad.append(f"The direction is positive under only {len(up)} of 4 filter settings ({', '.join(up)}).")
    else:
        bad.append("The direction is not positive under any of the four filter settings.")
    if h["kept_recent"] > h["kept_early"]:
        good.append(f"Accounts still active at week {k} per weekly cohort rose from "
                    f"{h['kept_early']:,.0f} to {h['kept_recent']:,.0f}, so the change is not only a smaller denominator.")
    else:
        bad.append(f"Accounts still active at week {k} per weekly cohort did not rise "
                   f"({h['kept_early']:,.0f} early, {h['kept_recent']:,.0f} recent).")
    if h["verdict"] == "no clear change":
        bad.append("The interval for the change includes zero or the change is under 1 percentage point, so it may be noise.")
    if not a["robust"]:
        bad.append("The verdict differs between filter settings: " +
                   ", ".join(f"{v}: {a['verdicts'][v]}" for v in VARIANT_ORDER) + ".")
    drift = a["farm_share_recent"] - a["farm_share_early"]
    if abs(drift) >= 0.05:
        bad.append(f"The share of first-week accounts removed by the high-activity filter moved from {pct(a['farm_share_early'], 0)} to "
                   f"{pct(a['farm_share_recent'], 0)}, so part of any change reflects who joins, not whether users stay.")
    if h["pooled_recent"][0] < 0.5:
        bad.append(f"Even in the latest cohorts only {pct(h['pooled_recent'][0], 2)} of accounts "
                   f"are active at week {k}; most new accounts never come back.")
    if h["new_accounts_recent"] > 1.25 * h["new_accounts_early"]:
        bad.append("New-account volume grew a lot over the same period, so raw account counts and retained accounts "
                   "can tell different stories.")
    if not good:
        good.append("No metric moved in the direction of the claim.")
    return good, bad


def bullets(items):
    return "\n".join(f"- {i}" for i in items)


def variant_table_md(a):
    rows = []
    for v in VARIANT_ORDER:
        r = a["variants"][v]
        rows.append(f"| {LABELS[v]} | {pct(r['early_mean'])} | {pct(r['recent_mean'])} | {pp(r['diff'])} | "
                    f"{pp(r['diff_lo'])} to {pp(r['diff_hi'])} | {r['verdict']} |")
    return "\n".join(rows)


def build_thesis(a, meta, template_path: Path, demo: bool) -> str:
    h = a["headline"]
    good, bad = evidence(a)
    p = meta["params"]
    values = {
        "banner": ("> **SYNTHETIC DEMO DATA. This file was generated from fake transactions to preview the layout. "
                   "It says nothing about NEAR.**\n\n") if demo else "",
        "headline_rate_pct": pct(h["pooled_recent"][0], 2),
        "headline_ci_pct": f"{pct(h['pooled_recent'][1], 2)} to {pct(h['pooled_recent'][2], 2)}",
        "week": str(HEADLINE_WEEK),
        "group": str(h["group_size"]),
        "early_span": span(h["early_span"]),
        "recent_span": span(h["recent_span"]),
        "early_mean": pct(h["early_mean"]),
        "recent_mean": pct(h["recent_mean"]),
        "diff": pp(h["diff"]),
        "diff_ci": f"{pp(h['diff_lo'])} to {pp(h['diff_hi'])}",
        "verdict": h["verdict"],
        "verdict_sentence": verdict_sentence(h),
        "robust_sentence": ("The verdict is the same under all four filter settings." if a["robust"]
                            else "The verdict is not the same under all four filter settings (see the table)."),
        "min_effect": f"{MIN_EFFECT * 100:.0f}",
        "variant_table_rows": variant_table_md(a),
        "evidence_for": bullets(good),
        "evidence_against": bullets(bad),
        "window": f"{day(date.fromisoformat(p['start_date']))} to {day(last_complete_week(meta))}",
        "burn_in": f"{p['scan_start']} to {p['start_date']}",
        "fetched": str(meta.get("fetched_at_utc") or "not supplied with the CSV export"),
        "bytes": (f"{int(meta['bytes_processed']) / 1e9:.1f} GB" if meta.get("bytes_processed") is not None else "not supplied"),
        "sql_hash": str(meta.get("sql_sha256") or "not supplied")[:12],
        "headline_variant": HEADLINE_VARIANT,
        "pooled_rate": pct(a["cohort_diagnostics"]["pooled_rate"], 2),
        "mean_cohort_rate": pct(a["cohort_diagnostics"]["mean_cohort_rate"], 2),
        "median_cohort_size": f"{a['cohort_diagnostics']['median_cohort_size']:,.0f}",
        "max_cohort_size": f"{a['cohort_diagnostics']['max_cohort_size']:,.0f}",
        "top_five_share": pct(a["cohort_diagnostics"]["top_five_share"]),
        "top_five_return_share": pct(a["cohort_diagnostics"]["top_five_return_share"]),
        "median_cohort_rate": pct(a["cohort_diagnostics"]["median_cohort_rate"], 2),
        "top_five_rate": pct(a["cohort_diagnostics"]["top_five_pooled_rate"], 2),
        "other_cohorts_rate": pct(a["cohort_diagnostics"]["other_cohorts_pooled_rate"], 2),
        "diagnostic_accounts": f"{a['cohort_diagnostics']['total_accounts']:,}",
    }
    text = template_path.read_text()
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    left = re.findall(r"\{\{[a-z_]+\}\}", text)
    if left:
        raise ValueError(f"Unfilled placeholders in THESIS template: {sorted(set(left))}")
    return text


CSS = """
:root{--bg:#F3F5F7;--ink:#1C2733;--muted:#566272;--rule:#D3D9E0;--recent:#0B6E8A;--early:#7F8B9A;--all:#A8691A;--band:rgba(11,110,138,.16);--warn:#8A2D1F}
@media (prefers-color-scheme:dark){:root{--bg:#12181F;--ink:#E6EBF0;--muted:#9AA6B3;--rule:#2B3541;--recent:#52BAD8;--early:#8D99A8;--all:#E3AE55;--band:rgba(82,186,216,.2);--warn:#FF9D8A}}
*{box-sizing:border-box}html{background:var(--bg);color:var(--ink)}
body{margin:0;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:760px;margin:0 auto;padding:40px 20px 80px}
h1,h2,.num{font-family:Charter,"Iowan Old Style","Palatino Linotype",Georgia,serif;font-weight:600;letter-spacing:-.01em}
h1{font-size:2.1rem;line-height:1.15;margin:.2rem 0 1.6rem}
h2{font-size:1.35rem;margin:3rem 0 .6rem;padding-top:1.2rem;border-top:1px solid var(--rule)}
p{margin:.5rem 0;max-width:68ch}.muted{color:var(--muted)}
.hero{display:flex;gap:1.4rem;align-items:baseline;flex-wrap:wrap}
.num{font-size:6.2rem;line-height:.9;color:var(--recent)}
.hero-text{font-size:1.25rem;max-width:22ch;line-height:1.3}
.verdict{font-size:1.1rem;margin-top:1.2rem}
.banner{background:var(--warn);color:#fff;padding:10px 20px;font-weight:600;text-align:center}
svg{width:100%;height:auto;display:block;margin:.8rem 0 .2rem}
.grid{stroke:var(--rule);stroke-width:1}.tick,.axis{fill:var(--muted);font-size:12px}
.line{fill:none;stroke-width:2.4;stroke-linejoin:round}.line.recent{stroke:var(--recent)}.line.early{stroke:var(--early)}.line.all{stroke:var(--all);stroke-width:1.6;stroke-dasharray:5 4}
.dot.recent{fill:var(--recent)}.dot.early{fill:var(--early)}.band{fill:var(--band);stroke:none}
.lab{font-size:12.5px;font-weight:600}.lab.recent{fill:var(--recent)}.lab.early{fill:var(--early)}.lab.all{fill:var(--all)}
figcaption{font-size:.95rem;color:var(--muted);max-width:68ch}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:.8rem 0}
th,td{text-align:left;padding:.45rem .5rem;border-bottom:1px solid var(--rule);vertical-align:top}th{font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}tr.head td{font-weight:600}
details{margin:.4rem 0}summary{cursor:pointer;color:var(--muted);font-size:.9rem}summary:focus-visible,a:focus-visible{outline:2px solid var(--recent);outline-offset:2px}
pre{overflow-x:auto;background:rgba(127,140,155,.12);padding:12px;font-size:.78rem;line-height:1.45;border-radius:4px}
code{font-size:.9em}a{color:var(--recent)}ul{padding-left:1.2rem;max-width:68ch}li{margin:.3rem 0}
@media (max-width:560px){.num{font-size:4.6rem}h1{font-size:1.7rem}}
"""


def build_html(a, meta, sql_text: str, demo: bool) -> str:
    h = a["headline"]
    p = meta["params"]
    k = HEADLINE_WEEK
    e = [(kk, pp_) for kk, pp_ in a["curve_early"]]
    r = [(kk, pp_) for kk, pp_ in a["curve_recent"]]
    c1 = charts.curves_chart(e, r, f"earliest {h['group_size']} cohorts", f"latest {h['group_size']} cohorts",
                             "Share of new accounts still active, by weeks since first activity")
    c2 = charts.cohort_chart(a["series_headline"], a["series_all"], "filtered", "no filter",
                             f"Week-{k} retention for every weekly cohort")
    rows = []
    for v in VARIANT_ORDER:
        r_ = a["variants"][v]
        cls = ' class="head"' if v == HEADLINE_VARIANT else ""
        rows.append(f"<tr{cls}><td>{escape(LABELS[v])}</td><td class='n'>{pct(r_['early_mean'])}</td>"
                    f"<td class='n'>{pct(r_['recent_mean'])}</td><td class='n'>{pp(r_['diff'])}</td>"
                    f"<td class='n'>{pp(r_['diff_lo'])} to {pp(r_['diff_hi'])}</td><td>{r_['verdict']}</td></tr>")
    good, bad = evidence(a)
    lis = lambda items: "".join(f"<li>{escape(i)}</li>" for i in items)
    banner = ('<div class="banner">SYNTHETIC DEMO DATA. Generated from fake transactions to preview the layout. '
              'It says nothing about NEAR.</div>') if demo else ""
    title = "Does NEAR keep its users?" + (" (synthetic demo)" if demo else "")
    fetched = ("provided" if meta.get("fetched_at_utc") else "not provided with the supplied CSV export")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><style>{CSS}</style></head>
<body>{banner}<main>
<p class="muted">Investment thesis on NEAR, built for NEAR HACKATHON</p>
<h1>Does NEAR keep its users?</h1>
<div class="hero"><span class="num">{pct(h['pooled_recent'][0], 2)}</span>
<span class="hero-text">pooled return rate at week {k}</span></div>
<p class="muted">Latest {h['group_size']} weekly cohorts ({escape(span(h['recent_span']))}), accounts above the 50-transaction first-week threshold excluded. 95% interval: {pct(h['pooled_recent'][1], 2)} to {pct(h['pooled_recent'][2], 2)}.</p>
<p class="verdict"><strong>Retention: {escape(h['verdict'])}.</strong> In the earliest {h['group_size']} cohorts ({escape(span(h['early_span']))}) it was {pct(h['early_mean'])}; in the latest it is {pct(h['recent_mean'])} ({pp(h['diff'])}, 95% interval {pp(h['diff_lo'])} to {pp(h['diff_hi'])}). {escape(verdict_sentence(h))}</p>

<h2>How retention decays</h2>
<figure>{c1}<figcaption>Of the accounts that first appeared in each group of cohorts, the share that signed a transaction again N weeks later. Week 0 is 100% by definition and is not drawn. The latest cohorts are shorter because they have had less time to be observed.</figcaption></figure>
<details><summary>Query behind this chart</summary><p class="muted">One query, <code>sql/retention.sql</code> (full text below). Rows where variant = <code>{HEADLINE_VARIANT}</code>, grouped into the earliest and latest cohorts.</p></details>

<h2>Is it getting better week by week?</h2>
<figure>{c2}<figcaption>Week-{k} retention for each weekly cohort. The shaded band is the 95% sampling interval for the filtered line. The dashed line keeps every account.</figcaption></figure>
<details><summary>Query behind this chart</summary><p class="muted">Same query. Filtered line: variant = <code>{HEADLINE_VARIANT}</code>. Dashed line: variant = <code>all</code>.</p></details>

<h2>Does the answer depend on the bot filter?</h2>
<p>I fixed the headline filter before pulling any data and report all four.</p>
<div style="overflow-x:auto"><table><thead><tr><th>Filter</th><th class="n">Early</th><th class="n">Recent</th><th class="n">Change</th><th class="n">95% interval</th><th>Verdict</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="muted">The test compares the {h['group_size']} earliest and {h['group_size']} latest cohorts using one number per weekly cohort, because week-to-week swings are larger than sampling error. A change counts only if its interval excludes zero and it is at least {MIN_EFFECT * 100:.0f} percentage point.</p>

<h2>Evidence for and against</h2>
<p><strong>For the claim that retention is improving</strong></p><ul>{lis(good)}</ul>
<p><strong>Against it, or limiting it</strong></p><ul>{lis(bad)}</ul>

<h2>What this cannot tell you</h2>
<ul>
<li>Active means "signed a transaction". Users who only act through a relayer (meta-transactions) or only receive tokens are not counted.</li>
<li>"New" means no signed transaction in the {escape(p['scan_start'])} to {escape(p['start_date'])} burn-in. Accounts dormant for longer look new.</li>
<li>The filter is a proxy. A heavy first week does not prove an account is a bot, and a quiet bot passes.</li>
<li>Retention is not value. This does not measure price, fees paid, or what users do.</li>
</ul>

<h2>Reproduce</h2>
<pre>python rebuild.py     # rebuilds this page and THESIS.md from data/retention.csv
python -m unittest    # runs the tests</pre>
<p class="muted">The aggregate CSV was supplied from <code>bigquery-public-data.crypto_near_mainnet_us.transactions</code>. Its query execution timestamp was {fetched}; the BigQuery job ID and bytes processed were not supplied. This page reproduces calculations from the CSV and does not claim to rerun BigQuery.</p>
<details><summary>Full SQL (sql/retention.sql)</summary><pre>{escape(sql_text)}</pre></details>
</main></body></html>"""
