# NKA-CLOSED-2026-009: The in-kernel path that forwards names to the data volume unfiltered has no reachable caller with attacker-controlled input

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | kernel virtual filesystem, internal data-forwarding code path |
| Location | kernel virtual filesystem internal path-stripping and file-operation forwarding code |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-18 |
| Closed | 2026-11-23 |

## The claim

A candidate found that an internal filesystem code path strips a fixed prefix from a path and forwards the remainder to the underlying encrypted volume with no name-policy checks, unlike the syscall-level data path which does apply such checks.

## Why it is not a finding

The code-level fact is accurate: this internal path genuinely has no name-policy check of its own. But an exhaustive search for every caller of the functions on this path, and of similarly-named legacy syscall handlers in the same area, found no route by which an attacker-controlled name reaches it. Every actual caller is either a fixed, trusted, build-time path or goes through the separate syscall-level data path that does apply the proper checks before reaching the volume.

## Routes tried

1. Searched every caller of the filesystem module from outside it, and found none that reaches the unfiltered functions with an externally-controlled name.
2. Checked a set of similarly-named legacy filesystem syscall handler functions in the same area of the tree, and confirmed none of them are wired to the syscall dispatcher.
3. Searched directly for any other call site of the specific unfiltered operations outside the module that defines them: none found.
4. Checked the capsule-load path, which takes user-supplied data but does not read from the filesystem despite a similarly-suggestive name.

## Evidence

Checked independently of the original write-up: yes.

- An independent grep-based call-graph search across the full source tree, outside the filesystem module itself, found no attacker-reachable caller.
- No dynamic or booted test was performed; this was a static call-graph review.
