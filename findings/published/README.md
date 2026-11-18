# Published findings

Every finding of this audit is published here when it is confirmed, with its evidence, and updated when the maintainers fix it, accept the risk or dispute it. [docs/disclosure.md](../../docs/disclosure.md) has the rules.

9 published: 9 open.
By severity: 1 medium, 4 low, 4 informational.

| ID | Title | Severity | Status | Published |
|---|---|---|---|---|
| [NKA-2026-023](NKA-2026-023.md) | Committed image capability ceiling disagrees with the capsule catalogue; the project's own check fails at the tag | informational | open | 2026-11-18 |
| [NKA-2026-021](NKA-2026-021.md) | PIE ELF with e_entry near 2^64 panics the kernel after mapping; RELRO page walk is unbounded under the global loader lock | low | open | 2026-11-18 |
| [NKA-2026-020](NKA-2026-020.md) | ELF loader RELATIVE relocation stores 8 bytes through one frame; an unaligned r_offset writes into the physically next frame | medium | open | 2026-11-18 |
| [NKA-2026-017](NKA-2026-017.md) | PQClean tamper gate (check-pqclean-pin.sh) fails at the release commit and no CI step runs it | informational | open | 2026-11-18 |
| [NKA-2026-016](NKA-2026-016.md) | STARK chained query grind: a fresh query draw costs 2^(g-3), not 2^g, so published soundness figures are overstated by about 2 to 3 bits | informational | open | 2026-11-18 |
| [NKA-2026-015](NKA-2026-015.md) | vfs OP_SEARCH truncates to max_hits before removing guarded hits, giving any FileSystem holder a content oracle for /linux-home and /linux-private | low | open | 2026-11-18 |
| [NKA-2026-014](NKA-2026-014.md) | proof-corpus-root.sh axiom allowlist is vacuous: the corpus root forms with an added axiom | low | open | 2026-11-18 |
| [NKA-2026-012](NKA-2026-012.md) | Measured boot verdict takes the last PCR 4 application as the loader that ran, so an enrolled loader loaded and never started is admitted as MEASURED | informational | open | 2026-11-18 |
| [NKA-2026-006](NKA-2026-006.md) | Rollback floor counter and base are held with empty authorisation, so a local TPM user can raise it, reset it or squat the base | low | open | 2026-11-17 |
