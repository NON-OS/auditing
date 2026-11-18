# Published findings

Every finding of this audit is published here when it is confirmed, with its evidence, and updated when the maintainers fix it, accept the risk or dispute it. [docs/disclosure.md](../../docs/disclosure.md) has the rules.

5 published: 5 open.
By severity: 3 low, 2 informational.

| ID | Title | Severity | Status | Published |
|---|---|---|---|---|
| [NKA-2026-016](NKA-2026-016.md) | STARK chained query grind: a fresh query draw costs 2^(g-3), not 2^g, so published soundness figures are overstated by about 2 to 3 bits | informational | open | 2026-11-18 |
| [NKA-2026-015](NKA-2026-015.md) | vfs OP_SEARCH truncates to max_hits before removing guarded hits, giving any FileSystem holder a content oracle for /linux-home and /linux-private | low | open | 2026-11-18 |
| [NKA-2026-014](NKA-2026-014.md) | proof-corpus-root.sh axiom allowlist is vacuous: the corpus root forms with an added axiom | low | open | 2026-11-18 |
| [NKA-2026-012](NKA-2026-012.md) | Measured boot verdict takes the last PCR 4 application as the loader that ran, so an enrolled loader loaded and never started is admitted as MEASURED | informational | open | 2026-11-18 |
| [NKA-2026-006](NKA-2026-006.md) | Rollback floor counter and base are held with empty authorisation, so a local TPM user can raise it, reset it or squat the base | low | open | 2026-11-17 |
