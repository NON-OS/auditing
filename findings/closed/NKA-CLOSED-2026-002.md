# NKA-CLOSED-2026-002: nonos-stark default 24-byte digest build is not reachable through the kernel's verifier dependency

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | STARK proof system, digest width parameterization |
| Location | STARKs:nonos-stark/src/merkle/hash.rs:32-35, STARKs:nonos-stark/Cargo.toml, STARKs:nox_verify/Cargo.toml:17 |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-21 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that nonos-stark's default 24-byte-digest, v1-transcript build could reach the kernel's gate verifier, creating a width mismatch against the 32-byte builds the kernel otherwise expects.

## Why it is not a finding

The default 24-byte width is real and is a documented design choice bound into the parameter identity, but no kernel path reaches it. The kernel's gate verifier depends on the STARK crate with default features disabled and the 32-byte-digest feature explicitly enabled, and every kernel-side dependent of the STARK crate sets that same feature. Cargo features are additive, so any build graph containing one of these crates is built with the 32-byte digest regardless of the library's own default.

## Routes tried

1. Checked whether the 24-byte default is reachable by any crate the kernel actually builds: every kernel-side Cargo manifest that depends on the STARK verifier enables the 32-byte-digest feature explicitly.
2. Checked whether a second crate with the same name could be the one reached instead: a different, unrelated crate of the same name exists but is used only by host-side proof tooling outside the kernel, not by any kernel-built target.
3. Checked whether a build that mixed the two widths would be silently accepted: the proof header carries its own digest width and headers of different widths refuse each other, so a mixed build fails closed rather than silently matching.

## Evidence

Checked independently of the original write-up: yes.

- An independent read of every kernel-side manifest that depends on the STARK verifier crate confirmed the 32-byte-digest feature is enabled in each, not relied upon as a library default.
- A feature-closure computation over the relevant manifests was performed to confirm the 32-byte feature is additive and present in every build graph that includes the verifier.
