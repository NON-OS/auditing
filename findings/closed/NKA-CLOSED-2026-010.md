# NKA-CLOSED-2026-010: A best-effort clear of a handover record gives no adversary in the threat model anything beyond what an already-documented exposure window provides

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | encrypted data-volume ownership handover record clearing |
| Location | encrypted data-volume handover record clearing and reopening code; related documentation |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-20 |
| Closed | 2026-11-23 |

## The claim

A candidate found that clearing a one-time ownership-handover record after a successful handover is best-effort: if the clearing write itself fails, the record can persist past the single boot the project's own documentation says it lasts, widening a documented exposure window.

## Why it is not a finding

The code behavior is exactly as the candidate describes, and the documentation's wording is narrower than the code's actual behavior, which is a residual documentation point kept separately. As a security candidate it does not hold: no ordinary boot path can trigger the failing write with no fault present, no reachable code path lets a sandboxed process trigger the failure, and the one adversary who could benefit from a stretched window already has, by the project's own threat model and its own documentation, everything they would gain from a forced failure the moment they have physical access to the storage during that window.

## Routes tried

1. Checked whether an ordinary boot that does not persist state can trigger the failing write with no attacker present: it cannot, because the volume in question is never opened at all on such a boot.
2. Checked whether a sandboxed process could cause the clearing write to fail: the write goes through the kernel's own block-device layer outside any sandboxed process's reach on every path examined.
3. Checked what the adversary who already has physical access during the documented window could gain from a forced write failure: nothing beyond what that same access already gives them, which the project's own documentation already states explicitly.
4. Identified the documentation wording gap directly and recorded it separately as a non-security residual.

## Evidence

Checked independently of the original write-up: yes.

- Independently re-derived the control flow from the relevant source files rather than relying on the original write-up's line references, which had drifted from the current commit.
- No fault-injected disk test or booted-kernel test was performed; this was a code-reading review.
