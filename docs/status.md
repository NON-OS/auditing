# Status

As of 2026-11-17, against the kernel at `551bbd3470fe8f3334b1381f4ffbc096e229a08d` (`main`).

## Where the audit stands

Phase 0 is under way. The method, the tooling and the claims register are published. No workstream has started, and there are no findings.

| Done | Not started |
|---|---|
| Scope, method, threat model, severity and disclosure rules | Review of any workstream |
| System model with every citation checked | Dynamic testing and fuzzing |
| 14 workstream checklists | Refutation of any candidate |
| Claims register seeded with 26 public claims, none yet verified | Verdicts on the claims |
| Tooling: citation, claims, finding and leak checks, code metrics | Explainers |
| Routine prompts for the lead, the refuter and 14 workers | Running the project's own claim-checking tools on both targets |

## First measured result: the project's docs drift from its code

`scripts/check_citations.py kernel` checked every source location cited in the kernel's documentation against the tree at this commit:

| | Count |
|---|---|
| Citations checked | 6,855 |
| Citations that no longer resolve | 496 (7%) |
| of which the file does not exist | 268 |
| of which the cited lines lie outside the file | 228 |

Of the 496, 124 are in the security, kernel and overview pages that carry the project's security claims. The capabilities pages cite `src/process/caps.rs` many times and that file does not exist at this commit.

What this does and does not show. It is a documentation result, not a vulnerability: a stale citation does not make the code wrong. It does mean a reader following the docs cannot always find the code a claim rests on. Some citations may have been correct against an earlier commit. The check is mechanical, so a citation that resolves can still be wrong about what is at that line.

## What is next

1. Resolve the release tag and `main` to hashes and record them.
2. Run the project's claim-checking tools on both targets and keep the output.
3. Start the lead, the refuter and two workstreams, and read what they produce before starting more.
