"""Small dependency-free SVG line charts (so the dashboard works offline)."""
from __future__ import annotations

from html import escape

W, H = 720, 300
ML, MR, MT, MB = 46, 118, 14, 46


def _scale(lo, hi, a, b):
    span = (hi - lo) or 1
    return lambda v: a + (v - lo) / span * (b - a)


def _ticks(vmax):
    """Percent ticks (0..vmax) with at most ~6 labels. vmax is a fraction."""
    top = vmax * 100
    for step in (1, 2, 5, 10, 20, 25):
        if top / step <= 6:
            break
    top_r = -(-top // step) * step
    return top_r / 100, [i * step / 100 for i in range(int(top_r // step) + 1)]


def _axes(parts, y, ymax, ticks):
    for t in ticks:
        yy = y(t)
        parts.append(f'<line class="grid" x1="{ML}" x2="{W - MR}" y1="{yy:.1f}" y2="{yy:.1f}"/>')
        parts.append(f'<text class="tick" x="{ML - 8}" y="{yy + 4:.1f}" text-anchor="end">{t * 100:.0f}%</text>')


def _spread(ys, gap=15):
    """Push label y-positions apart so end-of-line labels never overlap."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(order, order[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out


def _path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def curves_chart(early, recent, name_early, name_recent, title):
    """Retention by weeks since first activity, for two groups of cohorts.

    early / recent: lists of (k, p). Week 0 is 100% by definition so it is not drawn.
    """
    e = [(k, p) for k, p in early if k >= 1]
    r = [(k, p) for k, p in recent if k >= 1]
    kmax = max(k for k, _ in e + r)
    ymax, ticks = _ticks(max(p for _, p in e + r))
    x = _scale(1, kmax, ML, W - MR)
    y = _scale(0, ymax, H - MB, MT)
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">']
    _axes(parts, y, ymax, ticks)
    for k in range(1, kmax + 1):
        parts.append(f'<text class="tick" x="{x(k):.1f}" y="{H - MB + 18}" text-anchor="middle">{k}</text>')
    parts.append(f'<text class="axis" x="{(ML + W - MR) / 2:.0f}" y="{H - 6}" text-anchor="middle">weeks since first activity</text>')
    drawn = []
    for pts, cls, name in ((e, "early", name_early), (r, "recent", name_recent)):
        xy = [(x(k), y(p)) for k, p in pts]
        parts.append(f'<path class="line {cls}" d="{_path(xy)}"/>')
        for px, py in xy:
            parts.append(f'<circle class="dot {cls}" cx="{px:.1f}" cy="{py:.1f}" r="3"/>')
        drawn.append((xy[-1], cls, name))
    ys = _spread([d[0][1] for d in drawn])
    for (end, cls, name), ly in zip(drawn, ys):
        parts.append(f'<text class="lab {cls}" x="{end[0] + 8:.1f}" y="{ly + 4:.1f}">{escape(name)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def cohort_chart(series_head, series_all, name_head, name_all, title):
    """Week-4 retention for every weekly cohort, with a 95% interval band.

    series_*: lists of (week, p, lo, hi).
    """
    n = len(series_head)
    ymax, ticks = _ticks(max(max(h for *_, h in series_head), max(p for _, p, *_ in series_all)))
    x = _scale(0, n - 1, ML, W - MR)
    y = _scale(0, ymax, H - MB, MT)
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">']
    _axes(parts, y, ymax, ticks)
    last_month, last_i = None, -99
    for i, (wk, *_rest) in enumerate(series_head):
        if wk.month != last_month:
            last_month = wk.month
            if i - last_i < 3:  # too close to the previous label
                continue
            last_i = i
            parts.append(f'<text class="tick" x="{x(i):.1f}" y="{H - MB + 18}" text-anchor="middle">{wk.strftime("%b")}</text>')
            parts.append(f'<line class="grid" x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{H - MB}" y2="{H - MB + 4}"/>')
    upper = [(x(i), y(hi)) for i, (_, _, _, hi) in enumerate(series_head)]
    lower = [(x(i), y(lo)) for i, (_, _, lo, _) in enumerate(series_head)]
    band = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in upper + lower[::-1]) + " Z"
    parts.append(f'<path class="band" d="{band}"/>')
    by_week = {wk: p for wk, p, *_r in series_all}
    all_xy = [(x(i), y(by_week[wk])) for i, (wk, *_r) in enumerate(series_head)]
    parts.append(f'<path class="line all" d="{_path(all_xy)}"/>')
    head_xy = [(x(i), y(p)) for i, (_, p, *_r) in enumerate(series_head)]
    parts.append(f'<path class="line recent" d="{_path(head_xy)}"/>')
    ys = _spread([head_xy[-1][1], all_xy[-1][1]])
    parts.append(f'<text class="lab recent" x="{head_xy[-1][0] + 8:.1f}" y="{ys[0] + 4:.1f}">{escape(name_head)}</text>')
    parts.append(f'<text class="lab all" x="{all_xy[-1][0] + 8:.1f}" y="{ys[1] + 4:.1f}">{escape(name_all)}</text>')
    parts.append(f'<text class="axis" x="{(ML + W - MR) / 2:.0f}" y="{H - 6}" text-anchor="middle">week the accounts first appeared</text>')
    parts.append("</svg>")
    return "".join(parts)
