# NKA-CLOSED-2026-003: Release-signing script re-signs the committed boot record on every completed run, so a stale epoch cannot survive

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | release signing and boot-root enrollment tooling |
| Location | tools for release signing (boot-root enrollment and record re-signing steps), kernel's boot-measurement record check |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-21 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that the release-signing script could keep an old-epoch boot-root record when only a version counter changed and the loader root stayed the same, which the kernel would later refuse as stale.

## Why it is not a finding

The precondition the candidate needed, an unchanged loader root across a release, cannot hold in the signing script as written. Every signing run re-enrolls the loader's boot root unconditionally, before re-signing the record, and that enrollment draws a fresh random seed on every invocation, so the loader root is new (with overwhelming probability) on every completed run. The record and the version counter it carries always agree once a run completes.

## Routes tried

1. Traced the signing script's own step order: the loader-root enrollment step always runs before the record re-signing step, with no conditional skip.
2. Traced the enrollment command itself: it draws a fresh random seed from the operating system's own randomness source on every call and writes a new root built from that seed.
3. Checked whether any other path in the tooling could write the boot-root file without going through this enrollment step: none was found.

## Evidence

Checked independently of the original write-up: yes.

- Confirmed by reading the signing script's control flow and the enrollment tool's own self-test, which asserts that two different seeds produce two different roots.
- The signing process itself was not run end to end, since it requires release signing keys not available to this review.
- The core mechanism was re-derived directly from the signing script and the enrollment tool source in an independent clone of the repository: pad_seed is drawn from the operating system randomness source on every enrollment call, and the loader-root enrollment step runs unconditionally before the record re-signing step in the script.
