# Program Metrics

If you cannot measure it, you cannot manage it, and you definitely cannot
explain it to an executive. These are the KPIs for the program. Compute them
monthly, brief them quarterly.

## The core five

1. SLA compliance rate: percentage of findings remediated within SLA, by severity. Track criticals separately and target 100 percent. Anything less than 100 on criticals is the first slide of the briefing.
2. Mean time to remediate (MTTR): average days from triage to verified closure, by severity. Trending down is the program working. Flat is the program coasting.
3. Aging findings: count of open findings past SLA, and count within 20 percent of SLA (at risk). sla_tracker.py computes both. Past-SLA criticals without signed exceptions should be zero.
4. Scan coverage: percentage of in-scope assets scanned on schedule. A vulnerability program that cannot see its assets is guessing. Target 100 percent, report the gaps by asset owner.
5. Exception inventory: count of active exceptions, and count expired. Exceptions are healthy when they are current, signed, and few. A growing exception list is deferred risk with paperwork.

## Supporting metrics

- Reopen rate: findings that recur within 90 days of closure. High reopen rates mean fixes are cosmetic.
- Repeat-offender assets: systems that appear in findings quarter after quarter. Usually a patching process problem, not a vulnerability problem.
- Time to triage: days from discovery to triage assignment. If intake is slow, SLAs are fiction.

## How to present them

Executives need posture, not tickets. The quarterly briefing answers four questions:

- Are we getting better or worse? (trends on the core five)
- What is our biggest exposure right now? (top criticals and highs, in plain language, with CIA impact)
- What do you need from me? (resources, decisions, exception sign-offs)
- What changed since last quarter? (new threats, coverage changes, program improvements)

Use templates/executive-summary.md. One page. If it does not fit on one
page, it is not a summary.

## Metric hygiene

- Closed means verified by rescan, per WORKFLOW.md. Owner-closed tickets do not count.
- Restate baselines when scope changes. Adding a thousand new assets will move every number. Say so upfront.
- Never average severity. Averages hide the criticals. Report by severity, always.
