# Vulnerability Management Program Charter

## Purpose

Find vulnerabilities before attackers do, fix them in priority order, and
prove it with data. This program exists so that no known vulnerability sits
unaddressed past its deadline without a named owner and a documented reason.

This maps to NIST CSF 2.0 Govern (GV.OC: organizational cybersecurity risk
management strategy) and ISO 27001:2022 control A.8.8, which requires
information about technical vulnerabilities to be obtained, evaluated, and
acted on.

## Scope

In scope:

- All internet-facing systems, servers, workstations, and network devices the organization owns or operates
- Cloud workloads and the configurations that expose them
- Third-party software and libraries in production use

Out of scope (handled by other programs):

- Physical security findings
- Policy and compliance gaps with no technical vulnerability behind them
- Penetration test findings already tracked under a separate engagement (they feed this program as intake, they are not run by it)

## Roles

Program Owner: owns the program end to end. Sets the cadence, runs triage,
reports metrics to leadership, and approves exceptions. This is the one
throat to choke.

Remediation Owners: the system, application, or infrastructure owners who
actually fix things. Every open finding has exactly one. "The team" is not
an owner.

Executive Sponsor: a director or VP who backs the program when a deadline
conflicts with a ship date. Without this role, SLAs are suggestions.

Scanner Operators: run the scans, keep coverage complete, and feed results
into intake. They do not decide severity or deadlines. Separation of duties
keeps the data honest.

## Operating cadence

- Continuous: automated scanning on all in-scope assets, at least weekly for external attack surface
- Weekly: triage meeting. New findings rated, assigned, and given deadlines. Thirty minutes, standing agenda, no exceptions.
- Monthly: metrics review with remediation owners. SLA compliance, aging findings, repeat offenders.
- Quarterly: executive briefing using the executive summary template. Trends, risk posture, program needs.

This cadence maps to CIS Controls v8, Control 7 (Continuous Vulnerability
Management): run automated scans, remediate based on a risk-based process,
and measure.

## Decision rights

The Program Owner sets severity and deadlines. Remediation Owners can
dispute a rating within 5 business days with evidence, and the Program Owner
decides. Deadline extensions require the exception process in WORKFLOW.md,
signed by the Executive Sponsor. Nobody extends their own deadline.

## Success looks like

- 100 percent of in-scope assets scanned on schedule
- Zero critical findings past SLA without a signed exception
- SLA compliance trending up quarter over quarter
- Leadership can state the organization's vulnerability risk posture in one page (see templates/executive-summary.md)

Review this charter annually, or after any significant incident. A program
that never changes is a program nobody is running.
