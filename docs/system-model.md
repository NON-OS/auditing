# System model

What the audit is looking at: the parts of the NØNOS kernel that carry its security claims, where each lives in the tree, and which of the project's own documents describe it. Every source location below is written as its path inside the kernel repository with a `kernel:` prefix, and with line numbers where a range matters. `scripts/check_citations.py` checks each one against the audited commit. The commit is in `targets/verified-at.txt`.

This page describes the target. It does not say the target works. The audit tests that, and the results go in the reports.

## Shape and size

The kernel is a Rust `no_std` microkernel. Everything that is not the kernel runs as a capsule: a user-space process with a signed manifest and a list of capabilities. Drivers, the network stack, the desktop, the browser and the wallet are capsules.

`scripts/metrics.py` measured the tree at the verified commit. The counts are crude: `unsafe` is counted as the word, including in comments, so read them as places to look first, not as a tally of unsafe blocks.

| Directory | Rust lines | `unsafe` | Inline asm |
|---|---|---|---|
| `src` (the kernel) | 212,062 | 2,090 | 505 |
| `userland` (capsules, drivers, host proof crates) | 1,038,806 | 2,378 | 53 |
| `nonos-bootloader` | 25,446 | 194 | 39 |

`third_party` holds vendored code: 295,943 lines of C and 279,429 lines of assembly, including the post-quantum cryptography reference implementation.

`userland` includes the host-side proof crates, which never ship in an image. The size of the code that does ship is tracked by the project in `kernel:nonos-ci/baselines/tcb-x86_64-capsules.txt`.

## The chain of trust

| Step | What checks it | Where |
|---|---|---|
| Firmware starts the loader | Secure Boot, when it is on | `kernel:docs/security/boot-chain-and-signatures.md` |
| Loader admits the kernel | Two signatures, Ed25519 and ML-DSA-65, then the kernel's STARK trailer against a root baked into the loader | `kernel:nonos-bootloader/src/boot/attestation/kernel_gate.rs`, `kernel:nonos-bootloader/src/boot/crypto/signature/error.rs` |
| Kernel checks the loader that started it | The TPM's measurements when there is a TPM, or the loader's own record when there is not | `kernel:src/security/boot/loader_check/run.rs`, `kernel:nonos-boot-measure/src/gate/verdict.rs` |
| Older images are refused | A signed floor held in the TPM | `kernel:nonos-bootloader/src/boot/crypto/rollback/floor.rs`, `kernel:src/security/tpm/boot_reads/floor.rs` |
| Kernel admits a capsule | An attestation trailer checked against the enrolled policy root, before any process exists | `kernel:src/kernel_core/process_spawn/capsule_spawn/runner/preflight.rs`, `kernel:nonos-attest-path/src/trailer.rs`, `kernel:nonos-stark-enroll/src/policy.rs` |
| Boot profile limits what the capsule keeps | The profile removes the Network capability from every capsule when the boot has no network | `kernel:src/kernel_core/process_spawn/capsule_spawn/runner/profile_gate.rs` |

The project's description of each step is in `kernel:docs/security/stark-attestation.md`, `kernel:docs/security/measured-boot-and-tpm.md` and `kernel:docs/security/rollback-protection.md`.

## Authority

Every system call passes one function. Its own comment says no other path runs the capability check, which is a property the audit tests rather than accepts: `kernel:src/syscall/contract/dispatch.rs:25-40`.

| Question | Where it is decided |
|---|---|
| May this process make this call? | `kernel:src/syscall/contract/dispatch.rs` |
| Which capabilities exist, and what does each bit mean? | `kernel:src/capabilities/types/defs.rs` |
| Who can grant a capability, and how far? | `kernel:src/syscall/microkernel/capability/handlers.rs` |
| Which services may carry traffic off the machine? | `kernel:src/services/registry/policy.rs` |
| Which capsule may ask the keyring to open the wallet's records? | `kernel:userland/capsule_keyring/src/server/vault_gate/mod.rs` |

The project's account is in `kernel:docs/kernel/capabilities.md` and `kernel:docs/security/capsule-isolation.md`.

## Devices and memory

A device driver is a capsule. The kernel's hardware broker decides what it may map and which devices it may reach. DMA containment depends on an IOMMU being in service.

| Concern | Where |
|---|---|
| IOMMU posture and what happens when remapping is off | `kernel:src/memory/iommu/posture.rs`, `kernel:src/memory/iommu/no_iommu.rs` |
| Which device a driver may claim and confine | `kernel:src/hardware/broker/confine/decide.rs` |
| Remapping backend selection (VT-d, AMD-Vi) | `kernel:src/arch/x86_64/iommu/backend/select.rs` |
| System-call entry on x86-64 | `kernel:src/arch/x86_64/syscall/manager/entry.rs` |

The project states plainly that on a machine whose firmware left remapping off, a standard boot goes on with device DMA unconfined (`kernel:docs/release/0.9.3-security-limits.md`).

## Secrets

| What | Where |
|---|---|
| The key the TPM derives for this machine and boot state | `kernel:src/security/tpm/machine_key/consts.rs` |
| The data volume, its key and the handover between boots | `kernel:src/fs/blockfs_volume/session.rs`, `kernel:src/fs/blockfs_volume/handover/sector.rs` |
| What the shutdown wipe covers, and the panic wipe | `kernel:src/security/zerostate/panic_wipe.rs`, `kernel:docs/security/device-secrets-and-keys.md` |

A Lean model of the wipe is in `kernel:verification/lean/Nonos/ZeroState.lean`.

## What faces the network

| Part | Where |
|---|---|
| The Nym mixnet client and the Anyone client, both first-party capsules | `kernel:userland/capsule_net_nym/Cargo.toml`, `kernel:userland/capsule_net_anon/Cargo.toml` |
| The nsh attested login: a front capsule with the network and no attestation read, and an attest capsule with the keys and no network | `kernel:userland/capsule_nsh_front/README.md`, `kernel:userland/capsule_nsh_attest/README.md` |
| Every way off the machine, and the check that holds the list to the code | `kernel:docs/security/privacy-guarantees.md`, `kernel:tools/nonos-egress-audit` |

## Build and release

| Part | Where |
|---|---|
| The seal that signs, enrols and produces the release image | `kernel:tools/nonos_seal/chain.py` |
| The bill of materials, computed from the pinned lock files | `kernel:tools/nix/sbom.nix` |
| The project's account of reproducible builds | `kernel:docs/build/reproducible-builds.md` |

## Verification the project already ships

| Method | Where it runs |
|---|---|
| Lean proofs, including the extraction of kernel functions | `kernel:.github/workflows/verify.yml` |
| Verus theorems on the capability model | `kernel:verification/verus/src/lib.rs` |
| Kani harnesses over 17 proof crates | `kernel:.github/workflows/verify.yml` |
| Fuzz targets | `kernel:.github/workflows/fuzz.yml` |
| Dependency advisories and licence rules | `kernel:.github/workflows/ci-supply-chain.yml` |
| Reproducible build, isolation and adversarial lanes | `kernel:.github/workflows/ci-reproducible.yml`, `kernel:.github/workflows/ci-isolation.yml`, `kernel:.github/workflows/ci-adversarial.yml` |

## What the project already says it does not do

The project publishes its own list of known gaps with the file behind each: `kernel:docs/release/0.9.3-security-limits.md` and `kernel:docs/security/protections-and-limits.md`. The audit starts from that list. It checks that each entry is accurate for the audited commit, that the control behind each protection works as written, and whether anything is missing from it.

Its threat model is in `kernel:docs/overview/threat-model.md`. The audit's own adversaries and how they map to it are in [threat-model.md](threat-model.md).
