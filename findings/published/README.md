# Published findings

Every finding of this audit is published here when it is confirmed, with its evidence, and updated when the maintainers fix it, accept the risk or dispute it. [docs/disclosure.md](../../docs/disclosure.md) has the rules.

20 published: 20 open.
By severity: 1 high, 1 medium, 8 low, 10 informational.

| ID | Title | Severity | Status | Published |
|---|---|---|---|---|
| [NKA-2026-030](NKA-2026-030.md) | With no IOMMU unit in service, standard and server images let a claimed PCI device DMA to all RAM | informational | open | 2026-11-23 |
| [NKA-2026-009](NKA-2026-009.md) | MkKill and MkExit end one task only: sibling threads of a killed capsule keep running with its capabilities and its parent cannot kill them | low | open | 2026-11-23 |
| [NKA-2026-008](NKA-2026-008.md) | IPC TOTAL_BYTES_MAX (96 MiB) is not tied to free heap and one capsule can fill it using its own threads, refusing all IPC system-wide | medium | open | 2026-11-23 |
| [NKA-2026-007](NKA-2026-007.md) | IPC inbox count limit has no sender term: one sender can fill all 1024 slots of any inbox it may message, contradicting the documented half-inbox bound | low | open | 2026-11-23 |
| [NKA-2026-049](NKA-2026-049.md) | vfs OP_DIRSTAT on an ancestor directory counts the guarded /linux-home and /linux-private trees for a caller without ForeignExec | low | open | 2026-11-22 |
| [NKA-2026-046](NKA-2026-046.md) | stark-attest aggregate verifier: a header depth of 65 or more makes a shift overflow and panics in overflow-checked builds | informational | open | 2026-11-21 |
| [NKA-2026-043](NKA-2026-043.md) | JPEG DHT with a 255-entry length class aborts the image codec capsule (u8 loop counter overflow) | low | open | 2026-11-20 |
| [NKA-2026-039](NKA-2026-039.md) | Counts and release state disagree across README, release notes, EVIDENCE.json and security pages | informational | open | 2026-11-20 |
| [NKA-2026-038](NKA-2026-038.md) | sys::sync::SeqLock is a data race as written (Miri reports it); no caller | informational | open | 2026-11-20 |
| [NKA-2026-031](NKA-2026-031.md) | Syscall-return signal hook captures rbx and r12-r15 from live registers three Rust frames deep (latent) | informational | open | 2026-11-19 |
| [NKA-2026-026](NKA-2026-026.md) | nonos-dev-attest is accepted beside nonos-production although three comments say it is refused | informational | open | 2026-11-19 |
| [NKA-2026-023](NKA-2026-023.md) | Committed image capability ceiling disagrees with the capsule catalogue; the project's own check fails at the tag | informational | open | 2026-11-18 |
| [NKA-2026-021](NKA-2026-021.md) | PIE ELF with e_entry near 2^64 panics the kernel after mapping; RELRO page walk is unbounded under the global loader lock | low | open | 2026-11-18 |
| [NKA-2026-020](NKA-2026-020.md) | ELF loader RELATIVE relocation stores 8 bytes through one frame; an unaligned r_offset writes into the physically next frame | high | open | 2026-11-18 |
| [NKA-2026-017](NKA-2026-017.md) | PQClean tamper gate (check-pqclean-pin.sh) fails at the release commit and no CI step runs it | informational | open | 2026-11-18 |
| [NKA-2026-016](NKA-2026-016.md) | STARK chained query grind: a fresh query draw costs 2^(g-3), not 2^g, so published soundness figures are overstated by about 2 to 3 bits | informational | open | 2026-11-18 |
| [NKA-2026-015](NKA-2026-015.md) | vfs OP_SEARCH truncates to max_hits before removing guarded hits, giving any FileSystem holder a content oracle for /linux-home and /linux-private | low | open | 2026-11-18 |
| [NKA-2026-014](NKA-2026-014.md) | proof-corpus-root.sh axiom allowlist is vacuous: the corpus root forms with an added axiom | low | open | 2026-11-18 |
| [NKA-2026-012](NKA-2026-012.md) | Measured boot verdict takes the last PCR 4 application as the loader that ran, so an enrolled loader loaded and never started is admitted as MEASURED | informational | open | 2026-11-18 |
| [NKA-2026-006](NKA-2026-006.md) | Rollback floor counter and base are held with empty authorisation, so a local TPM user can raise it, reset it or squat the base | low | open | 2026-11-17 |
