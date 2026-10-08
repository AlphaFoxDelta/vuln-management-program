# Finding Workflow

Every finding moves through the same six stages. No shortcuts, no shadow
queues. If it is not in the tracker, it does not exist.

## 1. Intake

Scanner output lands here, from any source: scheduled scans, ad-hoc scans,
penetration tests, bug bounty reports, vendor advisories. Deduplicate
against open findings before creating anything new. A finding that already
has a ticket does not get a second ticket. It gets a comment on the first
one.

Use templates/finding-intake.md for anything that does not come from an
automated scanner.

## 2. Triage

Weekly, run by the Program Owner, with Remediation Owners present. For each
new finding:

- Confirm it is real. False positives get closed here with a note, not carried for months.
- Set severity using SEVERITY-RUBRIC.md, including escalation rules and CIA impact.
- Name exactly one Remediation Owner.
- Set the SLA deadline from the severity. The clock starts at triage, not at discovery, because the clock you can enforce is the one everyone agrees on.

Triage output is a ticket per finding, using templates/remediation-ticket.md.

## 3. Assignment

The ticket goes to the Remediation Owner with the severity, the deadline,
and the CIA impact spelled out. The owner acknowledges within 2 business
days. Silence is escalation to their manager, not patience.

## 4. Remediation

Fix, mitigate, or accept. Patching is preferred. When patching is not
possible on time, mitigations count if they genuinely reduce exposure:
isolating the asset, restricting access, disabling the vulnerable feature.
Document what was done, not what was intended.

## 5. Verification

The Scanner Operators rescan and confirm the fix. The Remediation Owner
does not close their own ticket. This is the separation of duties from the
charter, and it is what makes the metrics trustworthy. A finding closed
without verification gets reopened automatically at the next scan cycle.

## 6. Closure

Ticket closed with evidence: what was fixed, when, how it was verified.
Metrics in METRICS.md are computed from closed tickets, so closure quality
is program quality.

## The exception process

Sometimes a deadline cannot be met: a patch breaks production, a vendor has
no fix, a legacy system cannot be touched. That is what exceptions are for.
They are not deadline extensions by another name.

- The Remediation Owner files templates/exception-request.md before the SLA expires, not after.
- It names the compensating controls in place, the residual risk, and an expiry date. Exceptions expire. Permanent exceptions do not exist.
- The Program Owner reviews, the Executive Sponsor signs. Both signatures, no exceptions to the exception process.
- Expired exceptions become breached findings again, at their original severity.

An exception is a documented business decision to accept risk. That is a
legitimate outcome. An undocumented missed deadline is not.

## Reopened findings

If a finding reappears within 90 days of closure, it reopens at one
severity higher. Recurrence means the fix did not address the root cause,
and the program should treat it as a process failure, not bad luck.
