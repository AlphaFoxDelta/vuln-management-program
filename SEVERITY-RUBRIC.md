# Severity Rubric

Every finding gets one severity. The severity sets the SLA clock. No
negotiating the clock after the fact.

## Ratings

Ratings start from the CVSS v3.1 base score, then get adjusted for business
context. The base score is the floor, not the verdict.

| Severity | CVSS base score | SLA: fix or mitigate within |
|----------|-----------------|------------------------------|
| Critical | 9.0 - 10.0      | 15 days                      |
| High     | 7.0 - 8.9       | 30 days                      |
| Medium   | 4.0 - 6.9       | 90 days                      |
| Low      | 0.1 - 3.9       | 180 days                     |
| None     | 0.0             | Track only, no SLA           |

## CIA triad impact

Severity is about exploitability and impact together. For each finding, name
which leg of the CIA triad breaks if it is exploited. This is what turns a
technical score into a business conversation.

- Confidentiality: the finding exposes data. Example: SQL injection on a customer database, missing encryption on backups, overly broad S3 permissions.
- Integrity: the finding lets someone change data or behavior. Example: remote code execution, privilege escalation, unsigned firmware updates.
- Availability: the finding can take systems down. Example: unauthenticated denial of service, ransomware-prone unpatched services, single points of failure with known exploits.

Most critical findings break more than one leg. Remote code execution on a
payment server is a confidentiality, integrity, and availability problem at
once. Say so in the ticket. It is harder to deprioritize a finding when all
three are named.

## Escalation rules

Raise the severity one level when any of these are true:

- The vulnerability is in CISA's Known Exploited Vulnerabilities (KEV) catalog. If attackers are using it in the wild, the theoretical score understates the real risk.
- A public exploit exists and the asset is internet-facing.
- The asset holds regulated or crown-jewel data (cardholder data, PHI, core financials). Asset criticality is a multiplier, per NIST SP 800-40 Rev. 4.

Lower the severity one level only with evidence: compensating controls that
are actually in place and tested, not assumed. "We have a firewall" is not
evidence. A firewall rule you can show me is.

## What severity is not

It is not a measure of how hard the fix is. A critical finding with an easy
patch is still critical. It is not a negotiation between the scanner team
and the system owner. And it is never set by the person who owns the
deadline. See the charter for who decides.

## Worked example

Finding: unpatched VPN gateway, CVE with CVSS 8.1, public exploit
available, in CISA KEV, internet-facing.

Base rating: High (8.1). KEV plus public exploit plus internet-facing:
escalate to Critical. SLA: 15 days. CIA impact: confidentiality (tunnel
traffic exposed), integrity (attacker inside the trusted network),
availability (gateway can be knocked offline). Owner assigned at triage,
exception requires executive sign-off if the patch cannot land in time.
