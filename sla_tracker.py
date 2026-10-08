#!/usr/bin/env python3
"""SLA tracker for the vulnerability management program.

Reads a findings CSV and reports which findings are breached, at risk, or
on track against the severity SLAs from SEVERITY-RUBRIC.md. Writes a
Markdown report next to it.

CSV columns: id,title,severity,discovered,owner,status
  severity: Critical, High, Medium, Low
  discovered: YYYY-MM-DD
  status: Open, In Progress, Closed, Exception

Usage:
    python3 sla_tracker.py findings.csv
    python3 sla_tracker.py findings.csv --today 2026-10-08
"""

import argparse
import csv
import sys
from collections import Counter
from datetime import date, datetime

SLA_DAYS = {"Critical": 15, "High": 30, "Medium": 90, "Low": 180}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
ACTIVE_STATUSES = {"Open", "In Progress"}


def parse_args():
    p = argparse.ArgumentParser(description="Flag SLA breaches in a findings CSV.")
    p.add_argument("csv_file", help="findings CSV to evaluate")
    p.add_argument("--today", default=None, help="override today as YYYY-MM-DD (for demos)")
    p.add_argument("--report", default="sla_report.md", help="Markdown report to write")
    return p.parse_args()


def load_findings(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"id", "title", "severity", "discovered", "owner", "status"}
    if not required.issubset(rows[0].keys()):
        missing = required - set(rows[0].keys())
        sys.exit(f"CSV is missing columns: {', '.join(sorted(missing))}")
    return rows


def evaluate(rows, today):
    """Attach age, SLA, and verdict to each finding."""
    results = []
    for r in rows:
        severity = r["severity"].strip()
        if severity not in SLA_DAYS:
            sys.exit(f"Unknown severity '{severity}' on finding {r['id']}.")
        try:
            discovered = datetime.strptime(r["discovered"].strip(), "%Y-%m-%d").date()
        except ValueError:
            sys.exit(f"Bad date '{r['discovered']}' on finding {r['id']}. Use YYYY-MM-DD.")
        sla = SLA_DAYS[severity]
        age = (today - discovered).days
        remaining = sla - age
        status = r["status"].strip()
        if status in ACTIVE_STATUSES:
            if remaining < 0:
                verdict = "BREACHED"
            elif remaining <= max(3, int(sla * 0.2)):
                verdict = "AT RISK"
            else:
                verdict = "ON TRACK"
        else:
            verdict = status.upper()  # Closed or Exception: not on the clock
        results.append({**r, "age": age, "sla": sla, "remaining": remaining, "verdict": verdict})
    return results


def print_table(results):
    active = [r for r in results if r["verdict"] in ("BREACHED", "AT RISK", "ON TRACK")]
    active.sort(key=lambda r: (SEVERITY_ORDER[r["severity"]], r["remaining"]))
    print(f"{'ID':<10}{'Severity':<10}{'Age':<6}{'SLA':<6}{'Left':<10}{'Verdict':<10} Title")
    print("-" * 90)
    for r in active:
        left = f"{r['remaining']}d" if r["remaining"] >= 0 else f"{-r['remaining']}d over"
        print(f"{r['id']:<10}{r['severity']:<10}{r['age']:<6}{r['sla']:<6}{left:<10}{r['verdict']:<10} {r['title'][:45]}")


def print_summary(results):
    counts = Counter(r["verdict"] for r in results)
    print()
    print("Summary:")
    for verdict in ("BREACHED", "AT RISK", "ON TRACK", "CLOSED", "EXCEPTION"):
        if counts[verdict]:
            print(f"  {verdict}: {counts[verdict]}")
    breached_critical = [r for r in results if r["verdict"] == "BREACHED" and r["severity"] == "Critical"]
    if breached_critical:
        print(f"\n  WARNING: {len(breached_critical)} breached Critical finding(s) need immediate attention.")


def write_report(results, today, path):
    counts = Counter(r["verdict"] for r in results)
    lines = [
        "# SLA Report",
        "",
        f"Generated: {today.isoformat()}",
        "",
        "## Summary",
        "",
    ]
    for verdict in ("BREACHED", "AT RISK", "ON TRACK", "CLOSED", "EXCEPTION"):
        if counts[verdict]:
            lines.append(f"- {verdict}: {counts[verdict]}")
    lines += ["", "## Findings needing attention", ""]
    flagged = [r for r in results if r["verdict"] in ("BREACHED", "AT RISK")]
    flagged.sort(key=lambda r: (SEVERITY_ORDER[r["severity"]], r["remaining"]))
    if not flagged:
        lines.append("None. Everything is on track.")
    for r in flagged:
        left = f"{r['remaining']} days left" if r["remaining"] >= 0 else f"{-r['remaining']} days overdue"
        lines.append(f"- {r['id']} ({r['severity']}, {r['verdict']}, {left}): {r['title']} -- owner: {r['owner']}")
    lines += ["", "## Exceptions on file", ""]
    exceptions = [r for r in results if r["verdict"] == "EXCEPTION"]
    if not exceptions:
        lines.append("None.")
    for r in exceptions:
        lines.append(f"- {r['id']} ({r['severity']}): {r['title']} -- owner: {r['owner']}")
    lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nReport written to {path}")


def main():
    args = parse_args()
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    results = evaluate(load_findings(args.csv_file), today)
    print_table(results)
    print_summary(results)
    write_report(results, today, args.report)


if __name__ == "__main__":
    main()
