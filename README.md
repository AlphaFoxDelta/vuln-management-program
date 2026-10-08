# vuln-management-program

A complete, ready-to-run vulnerability management program kit. Scanning
tools find vulnerabilities. This is the part most teams skip: the program
that decides what gets fixed, by whom, by when, and how leadership stays
informed.

I built this as the management layer that sits on top of tools like the
scanners in my other repos. The code finds the problems. This kit runs the
program that fixes them.

## What is in here

- PROGRAM-CHARTER.md: the program's purpose, scope, roles, and operating cadence
- SEVERITY-RUBRIC.md: how findings get rated, with CVSS ranges, SLA timeframes, and CIA triad impact
- THREAT-ANALYSIS.md: how findings map to real threats, actors, and attack paths
- WORKFLOW.md: the finding lifecycle, from intake to closure, plus the exception process
- METRICS.md: the KPIs that tell you whether the program is working
- templates/: finding intake form, remediation ticket, exception request, executive summary
- sla_tracker.py: reads a findings CSV and flags SLA breaches (standard library only)
- gantt.py: builds a remediation timeline chart as a self-contained HTML file (standard library only)
- sample-findings.csv and remediation-plan.csv: sample data so both scripts run out of the box

## Quick start

Check SLA status of the sample findings:

```bash
python3 sla_tracker.py sample-findings.csv
```

That prints a status table and writes sla_report.md.

Build the sample remediation timeline:

```bash
python3 gantt.py remediation-plan.csv
```

That writes gantt_chart.html. Open it in a browser.

## The standards this follows

The kit is aligned to real frameworks, not invented ones:

- NIST Cybersecurity Framework 2.0: Govern (GV.OC, GV.RM), Protect, Detect (DE.CM), Respond
- NIST SP 800-40 Rev. 4: Guide to Enterprise Patch Management Technology
- ISO/IEC 27001:2022, control A.8.8: management of technical vulnerabilities
- CVSS v3.1 for severity scoring, with CISA's Known Exploited Vulnerabilities catalog as an escalation trigger
- CIS Controls v8, Control 7: Continuous Vulnerability Management

Each document names the specific control or section it maps to, so an
auditor or a hiring manager can trace the thinking.

## Who this is for

Security leaders standing up a program, managers inheriting one, and teams
that have scanners running but no process around them. If your vulnerability
program is a spreadsheet nobody opens, start here.
