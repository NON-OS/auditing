# Status

As of 2026-11-17. The audit started today. Targets: the release `v0.9.3.5` at `b3dd1fa37ce2e32e3cb2f6a462081fefede4df40` and `main` at `551bbd3470fe8f3334b1381f4ffbc096e229a08d`.

## What happened on 2026-11-17

The audit moved from preparation to running on this date. In order:

1. This repository was made public, with a clean history and its checks passing in CI.
2. The commit checks were added. Hooks and CI now refuse chat and session identifiers, keys, tokens, the addresses of real hosts and commit messages that break the rules, over the whole history.
3. The two targets were resolved to full commit hashes and recorded.
4. The first measurements were taken: the code metrics and the citation check on the kernel's own documentation (the result is below).
5. The cloud environment was set up. Claude runs in sandboxes that hold no keys and cannot push. Every run has a cost cap, the account has a monthly limit, and an alert goes out at half of it. Notes go to a private store.
6. A lead, a refuter and a worker were deployed, each as its own agent. The lead and the refuter ran once, against an empty store, and behaved as designed.
7. The first workstream, WS3 (syscall layer and capabilities), ran twice against the release. It read the syscall layer, cross-checked the 196 syscall numbers against the registry, built a table of which capsule holds which capability, and ran the project's own host tests, 2,167 of them, which all passed. That pass is a baseline and not a result of this audit.
8. The workers wrote candidates. Every one is a hypothesis and none is a finding. They stay private until they are fixed.
9. The refuter completed its first review of a WS3 candidate, working only from the claim and the evidence.
10. All 14 workstreams were put on a schedule. Each worker runs every fourth day, the lead and the refuter run daily, and WS1 (the boot chain) was started the same day.

## Where the audit stands

| Done | In progress | Not started |
|---|---|---|
| Scope, method, threat model, severity and disclosure rules | WS3, syscall layer and capabilities. WS1, the boot chain, started | The other 12 workstreams, which are scheduled |
| System model with every citation checked | Refutation of the WS3 candidates, one reviewed so far | Refutation of candidates from other workstreams |
| 14 workstream checklists | Running the project's own claim-checking tools on both targets | Verdicts on the claims |
| Claims register seeded with 26 public claims, none yet verified | | Explainers |
| Tooling: citation, claims, finding, leak and commit checks, code metrics | | Dynamic testing and fuzzing |
| The cloud environment, the lead, the refuter and the worker | | |

No finding has been published.

## First measured result: the project's docs drift from its code

`scripts/check_citations.py kernel` checked every source location cited in the kernel's documentation:

| | `main` | Release `v0.9.3.5` |
|---|---|---|
| Citations checked | 6,855 | 6,842 |
| Citations that no longer resolve | 496 (7%) | 496 (7%) |
| of which the file does not exist | 268 | 268 |
| of which the cited lines lie outside the file | 228 | 228 |

Of the 496, 124 are in the security, kernel and overview pages that carry the project's security claims. The capabilities pages cite `src/process/caps.rs` many times and that file does not exist at either commit.

What this does and does not show. It is a documentation result, not a vulnerability: a stale citation does not make the code wrong. It does mean a reader following the docs cannot always find the code a claim rests on. Some citations may have been correct against an earlier commit. The check is mechanical, so a citation that resolves can still be wrong about what is at that line.

## What is next

1. Finish refuting the WS3 candidates.
2. Read what each newly started workstream produces before changing the schedule.
3. Run the project's claim-checking tools on both targets and keep the output.
4. Fix the stale citations in the project's documentation.
