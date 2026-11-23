# Closed cases

Candidates a worker wrote up and a second, independent reviewer checked and refuted. These are not findings: nothing here is a vulnerability. They are published so the record shows what was checked and ruled out, not only what was confirmed. [docs/disclosure.md](../../docs/disclosure.md) has the rules.

16 closed.

| ID | Title | Component | Closed |
|---|---|---|---|
| [NKA-CLOSED-2026-016](NKA-CLOSED-2026-016.md) | A known timing-safety advisory in a cryptographic dependency does not apply to the code path the kernel's key-decapsulation actually uses | post-quantum key-decapsulation dependency chain | 2026-11-23 |
| [NKA-CLOSED-2026-015](NKA-CLOSED-2026-015.md) | A package format's internal page-digest table is not checked by parsing alone, but the format's actual production reader never trusts parsing alone either | userspace package format used to deliver Linux-compatible application content | 2026-11-23 |
| [NKA-CLOSED-2026-014](NKA-CLOSED-2026-014.md) | A crafted image that decodes faster than it should does not amplify cost beyond what a normal image of the same size already costs | image-decoding capsule, JPEG decoder | 2026-11-23 |
| [NKA-CLOSED-2026-013](NKA-CLOSED-2026-013.md) | No route was found for a debug exception to interrupt the kernel's syscall entry on the hardware tested | kernel syscall-entry assembly and processor debug-exception handling | 2026-11-23 |
| [NKA-CLOSED-2026-012](NKA-CLOSED-2026-012.md) | Formally unproved copies of the write-execute-exclusion rule exist only in dead code on the architecture the kernel ships | memory-permission encoding and the kernel's machine-checked write-execute-exclusion proof | 2026-11-23 |
| [NKA-CLOSED-2026-011](NKA-CLOSED-2026-011.md) | The premise that a development-capsule build guard only covers release kernels does not hold: the development profile that carries the capsule is itself the guarded configuration | build-time feature guards for development-only attack-simulation capsules | 2026-11-23 |
| [NKA-CLOSED-2026-010](NKA-CLOSED-2026-010.md) | A best-effort clear of a handover record gives no adversary in the threat model anything beyond what an already-documented exposure window provides | encrypted data-volume ownership handover record clearing | 2026-11-23 |
| [NKA-CLOSED-2026-009](NKA-CLOSED-2026-009.md) | The in-kernel path that forwards names to the data volume unfiltered has no reachable caller with attacker-controlled input | kernel virtual filesystem, internal data-forwarding code path | 2026-11-23 |
| [NKA-CLOSED-2026-008](NKA-CLOSED-2026-008.md) | A predictable time-sync nonce and weak server check are real but unreachable in every shipped build profile | network time synchronization capsule protocol handling | 2026-11-23 |
| [NKA-CLOSED-2026-007](NKA-CLOSED-2026-007.md) | Non-reseeded randomness between draws gives a VM-snapshot adversary no capability beyond what the snapshot already provides | kernel-wide pseudorandom generator reseed interval | 2026-11-23 |
| [NKA-CLOSED-2026-006](NKA-CLOSED-2026-006.md) | A guest process cannot acquire a device-broker grant to exploit missing window or clock-page checks | kernel cross-process memory mapping for sandboxed guest processes | 2026-11-23 |
| [NKA-CLOSED-2026-005](NKA-CLOSED-2026-005.md) | Unauthenticated time-sync capsule is not present in any image profile the project builds | network time synchronization capsule and its inclusion in build profiles | 2026-11-23 |
| [NKA-CLOSED-2026-004](NKA-CLOSED-2026-004.md) | MkMunmap cannot free a page another process or the kernel still relies on | kernel memory management, user-space unmap syscall | 2026-11-23 |
| [NKA-CLOSED-2026-003](NKA-CLOSED-2026-003.md) | Release-signing script re-signs the committed boot record on every completed run, so a stale epoch cannot survive | release signing and boot-root enrollment tooling | 2026-11-23 |
| [NKA-CLOSED-2026-002](NKA-CLOSED-2026-002.md) | nonos-stark default 24-byte digest build is not reachable through the kernel's verifier dependency | STARK proof system, digest width parameterization | 2026-11-23 |
| [NKA-CLOSED-2026-001](NKA-CLOSED-2026-001.md) | Measured-boot gate falling back to the loader's own word on a TPM error is documented, intended behavior | kernel measured boot and loader-check gate | 2026-11-23 |
