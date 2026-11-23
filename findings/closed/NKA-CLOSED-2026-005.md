# NKA-CLOSED-2026-005: Unauthenticated time-sync capsule is not present in any image profile the project builds

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | network time synchronization capsule and its inclusion in build profiles |
| Location | build-profile feature configuration; kernel clock-adjustment syscall; certificate-validity check code |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-17 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that an unauthenticated network time-sync capsule, fed by an unauthenticated protocol, could move the kernel's trusted clock within its allowed range and that a network attacker could exploit this to affect certificate-validity checks that read the clock.

## Why it is not a finding

The network attacker the candidate needs has no server to attack in any image the project actually builds. A full feature-closure computation over every shipped build profile shows the time-sync capsule is absent from every GUI, server, and capsule-only profile; it exists only in a narrow developer smoke-test configuration that nothing in the build tooling actually produces as a shippable image. The underlying kernel mechanism (a clock that can move anywhere within a wide, multi-decade range with no step bound) is real and is kept as a separate hardening observation, not scored as this candidate's finding, since it needs a different, non-network precondition (control of an already-trusted clock-setting capability).

## Routes tried

1. Computed the full feature closure for every build profile the project's own build configuration defines and confirmed the time-sync capsule is excluded from all of them.
2. Checked whether the capsule could be spawned even if compiled in: its spawn path is compiled out entirely whenever the standard network stack feature is present, which every real profile has.
3. Searched for any other source of trusted time in a shipped image: none besides the excluded capsule and a user-facing clock-setting capsule with no network input.
4. Reviewed how the kernel's clock-adjustment syscall and certificate-validity checks actually use the clock, to state the residual accurately.

## Evidence

Checked independently of the original write-up: yes.

- An independent feature-closure computation was run over the project's own build-profile configuration file to confirm the capsule's exclusion from every shipped profile.
- Searched the full source tree for any other caller of the clock-adjustment syscall besides the excluded capsule and the user clock-setting capsule.
