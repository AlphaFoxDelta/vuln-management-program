# Threat Analysis Guide

A vulnerability is a fact. A threat is what someone does with it. This
document connects the two, so triage decisions are based on how findings
get exploited, not just how they score.

## Who is coming

Think in three tiers. Most organizations face all three.

- Opportunistic attackers: automated scanning, botnets, script kiddies. They exploit whatever is internet-facing and unpatched. Volume business. They are the reason internet-facing highs and criticals have short SLAs.
- Ransomware crews and organized crime: they buy initial access, then move laterally. They love unpatched VPNs, RDP exposed to the internet, and privilege escalation chains. One medium finding becomes their foothold; the next one becomes domain admin.
- Insiders and targeted actors: slower, quieter, harder. They abuse excessive permissions and unmonitored access. This is where integrity and confidentiality findings matter most, even at lower CVSS scores.

## How findings become incidents

Almost every breach follows the same path:

1. Initial access through an unpatched internet-facing vulnerability or misconfiguration
2. Privilege escalation using a local vulnerability the scanner flagged months ago
3. Lateral movement across flat network segments
4. Impact: encryption, exfiltration, or both

When you triage a finding, ask where it sits on that path. A medium
privilege escalation on a domain controller matters more than a high
information disclosure on a marketing site, because of what it enables
next. The rubric's escalation rules exist for exactly this reason.

## MITRE ATT&CK mapping

Map each finding type to the tactic it enables. This gives remediation
owners and executives a shared language.

- Remote code execution: Initial Access (T1190, exploit public-facing application), then Execution
- Privilege escalation: Privilege Escalation (T1068, exploitation for privilege escalation)
- Credential exposure: Credential Access (T1552, unsecured credentials)
- Missing patches on edge devices: Initial Access, and check CISA KEV for in-the-wild use
- Overly broad permissions: Persistence and Defense Evasion territory; an insider does not need an exploit

You do not need to map every finding to ATT&CK. Map the criticals and
highs, and map anything that forms a chain. Chains are what kill you.

## The CIA triad in practice

Use the triad to explain impact to people who do not read CVE descriptions.

- When confidentiality breaks, you are notifying customers and regulators. Breach disclosure laws do not care about your CVSS score.
- When integrity breaks, you cannot trust your own data or systems. Backups, logs, and binaries are all suspect until verified.
- When availability breaks, the business stops. Ransomware turned availability into the most expensive leg of the triad for most companies.

A finding that threatens availability on a revenue system can outrank a
confidentiality finding on an internal wiki, even at the same CVSS. The
score starts the conversation. Business impact finishes it.

## What to do with this

- At triage, note the threat tier and the ATT&CK tactic for criticals and highs
- When a finding is in CISA KEV, treat it as actively exploited, because it is
- Review this guide quarterly alongside threat intel. The actors change. The path mostly does not.
