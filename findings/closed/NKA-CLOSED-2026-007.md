# NKA-CLOSED-2026-007: Non-reseeded randomness between draws gives a VM-snapshot adversary no capability beyond what the snapshot already provides

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | kernel-wide pseudorandom generator reseed interval |
| Location | kernel global randomness generator reseed logic; data-volume per-sector random nonce generation |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-18 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that the kernel's randomness generator, which reseeds only periodically rather than on every draw, would let an adversary who can snapshot, restore, and clone a virtual machine observe repeated random output across clones, and that this was a usable weakness.

## Why it is not a finding

The mechanism is real, two clones resumed from one snapshot do draw identical random bytes until the next reseed, but the adversary the candidate names already holds the full memory image at the moment of snapshot, which already includes the storage key that matters more than any random nonce. Reusing a nonce gives that adversary no capability beyond what possessing the snapshot already gives. The one case where nonce reuse would add real information, an adversary who sees two cloned disks but never the memory image, falls outside every adversary this project's own threat model defines.

## Routes tried

1. Checked what the stated adversary already has: full access to the virtual machine's memory at the point of snapshot, which already includes the long-lived storage key.
2. Checked whether the same weakness helps a different adversary who cannot snapshot another instance at all: that adversary has no way to reach two correlated outputs in the first place.
3. Checked whether a network observer of two cloned instances could exploit correlated randomness in session key material: the relevant cryptographic operations do not consume randomness in a way that would leak secrets from repeated values, and session establishment mixes the remote peer's own fresh randomness.
4. Identified the one adversary shape that would gain something, disk-only access to two clones without ever seeing the memory image, and confirmed it is not one of the adversaries this project's threat model defines.

## Evidence

Checked independently of the original write-up: yes.

- Independently traced the reseed interval and per-draw code path to confirm the described behavior.
- No virtual machine snapshot or clone was actually performed; this was a code-reading review.
