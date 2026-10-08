#!/usr/bin/env python3
"""Gantt chart generator for remediation planning.

Reads a remediation plan CSV and writes a self-contained HTML Gantt chart.
No dependencies beyond the standard library. Open the output in a browser.

CSV columns: task,owner,start,end,phase
  start/end: YYYY-MM-DD

Usage:
    python3 gantt.py remediation-plan.csv
    python3 gantt.py remediation-plan.csv --output plan.html
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta

PHASE_COLORS = {
    "Discover": "#4C9AFF",
    "Remediate": "#FF5630",
    "Verify": "#36B37E",
    "Report": "#FFAB00",
}
DEFAULT_COLOR = "#8B8B8B"


def parse_args():
    p = argparse.ArgumentParser(description="Build an HTML Gantt chart from a plan CSV.")
    p.add_argument("csv_file", help="remediation plan CSV")
    p.add_argument("--output", default="gantt_chart.html", help="HTML file to write")
    return p.parse_args()


def load_plan(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"task", "owner", "start", "end", "phase"}
    if not required.issubset(rows[0].keys()):
        missing = required - set(rows[0].keys())
        sys.exit(f"CSV is missing columns: {', '.join(sorted(missing))}")
    plan = []
    for r in rows:
        try:
            start = datetime.strptime(r["start"].strip(), "%Y-%m-%d").date()
            end = datetime.strptime(r["end"].strip(), "%Y-%m-%d").date()
        except ValueError:
            sys.exit(f"Bad date on task '{r['task']}'. Use YYYY-MM-DD.")
        if end < start:
            sys.exit(f"Task '{r['task']}' ends before it starts.")
        plan.append({**r, "start": start, "end": end})
    plan.sort(key=lambda r: r["start"])
    return plan


def build_html(plan):
    first = min(r["start"] for r in plan)
    last = max(r["end"] for r in plan)
    # Pad to full weeks for a clean axis.
    first -= timedelta(days=first.weekday())
    last += timedelta(days=6 - last.weekday())
    total_days = (last - first).days + 1

    # Week axis labels.
    ticks = []
    d = first
    while d <= last:
        left = (d - first).days / total_days * 100
        ticks.append((left, d.strftime("%b %d")))
        d += timedelta(days=7)

    today = datetime.now().date()
    today_left = None
    if first <= today <= last:
        today_left = (today - first).days / total_days * 100

    rows_html = []
    for r in plan:
        left = (r["start"] - first).days / total_days * 100
        width = max((r["end"] - r["start"]).days + 1, 1) / total_days * 100
        color = PHASE_COLORS.get(r["phase"].strip(), DEFAULT_COLOR)
        rows_html.append(
            f'<div class="row"><div class="label">{r["task"]} '
            f'<span class="owner">{r["owner"]}</span></div>'
            f'<div class="track"><div class="bar" style="left:{left:.2f}%;width:{width:.2f}%;'
            f'background:{color};" title="{r["phase"]}: {r["start"]} to {r["end"]}"></div>'
            + (f'<div class="today" style="left:{today_left:.2f}%;"></div>' if today_left is not None else "")
            + "</div></div>"
        )

    legend = "".join(
        f'<span class="key"><span class="swatch" style="background:{c};"></span>{p}</span>'
        for p, c in PHASE_COLORS.items() if any(r["phase"].strip() == p for r in plan)
    )
    axis = "".join(f'<span class="tick" style="left:{left:.2f}%;">{label}</span>' for left, label in ticks)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Remediation Plan</title>
<style>
body {{ font-family: -apple-system, "Segoe UI", Arial, sans-serif; margin: 32px; color: #222; }}
h1 {{ font-size: 22px; }}
.legend {{ margin: 12px 0 20px; }}
.key {{ margin-right: 18px; font-size: 14px; }}
.swatch {{ display: inline-block; width: 14px; height: 14px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}
.axis {{ position: relative; height: 22px; margin-left: 280px; border-bottom: 1px solid #ccc; font-size: 12px; color: #666; }}
.tick {{ position: absolute; transform: translateX(-50%); white-space: nowrap; }}
.row {{ display: flex; align-items: center; margin: 8px 0; }}
.label {{ width: 280px; font-size: 14px; padding-right: 12px; box-sizing: border-box; }}
.owner {{ color: #777; font-size: 12px; }}
.track {{ position: relative; flex: 1; height: 26px; background: #f4f4f4; border-radius: 4px; }}
.bar {{ position: absolute; top: 4px; height: 18px; border-radius: 4px; min-width: 4px; }}
.today {{ position: absolute; top: -4px; bottom: -4px; width: 2px; background: #111; }}
.footer {{ margin-top: 24px; font-size: 12px; color: #888; }}
</style>
</head>
<body>
<h1>Remediation Plan</h1>
<div class="legend">{legend}</div>
<div class="axis">{axis}</div>
{"".join(rows_html)}
<div class="footer">Black line marks today. Hover a bar for phase and dates.</div>
</body>
</html>
"""


def main():
    args = parse_args()
    plan = load_plan(args.csv_file)
    html = build_html(plan)
    with open(args.output, "w") as f:
        f.write(html)
    print(f"Wrote {args.output} ({len(plan)} tasks)")


if __name__ == "__main__":
    main()
