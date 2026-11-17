# Severity

Severity follows the effect on an asset, for the adversary with the weakest starting position who can reach the flaw. It does not follow the bug class, and it is never raised to make a finding sound more important. Adversaries and assets are in [threat-model.md](threat-model.md).

| Severity | Definition |
|---|---|
| Critical | An A1 or A2 adversary with no special precondition gains kernel code execution, defeats the trust chain, or extracts sealed keys |
| High | A capsule escapes its capability set or its isolation. A trust check is bypassed under a realistic precondition. A remote unauthenticated attacker causes a persistent denial of service or compromises a capsule |
| Medium | A weakness that needs an unusual precondition, a limited information leak, or a denial of service by a privileged capsule |
| Low | A defence-in-depth gap with no direct path to an asset |
| Informational | A hardening suggestion, or a documentation claim that overstates or no longer matches the code |

Each finding also carries a CVSS 4.0 vector. When the vector and this table disagree, the report says why and which it uses.

## Confidence

Separate from severity, and never merged with it.

| Confidence | Meaning |
|---|---|
| Confirmed | Reproduced, with the steps |
| Supported | Traced through the code with file and line, not reproduced |
| Hypothesis | A lead. Not a finding and not scored |

## How the table is applied

- A user pointer in a system call that is not range-checked, reachable by any capsule: High, or Critical if it gives a write into kernel memory.
- A trailer parser that accepts an old format where a newer one is required: High if an unsigned capsule can start, Medium if it only weakens a check that something else repeats.
- A panic in ring 0 reachable only by a capsule that holds the device capability it needs: Low or Medium, depending on what the documentation promises.
- A limit the project already documents (`kernel:docs/release/0.9.3-security-limits.md`) is not a new finding. If the audit shows it is worse than documented, that difference is the finding.
- A documentation claim that does not match the code: Informational.
