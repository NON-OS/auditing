# Threat model

The project's threat model is `kernel:docs/overview/threat-model.md`. It says what NØNOS protects, from whom, what it relies on and what it leaves out. This page does not replace it. It fixes the five adversaries the audit ranks every finding against, and the starting position of each, so that a severity means the same thing in every report.

## Assets

These are the project's own (`kernel:docs/overview/threat-model-assets.md`), reduced to what the audit tests:

| Asset | Guard the project describes |
|---|---|
| What runs: the kernel image and every capsule | signatures, attestation and the capability word |
| The device secret and the machine key | derived from the TPM, held by one capsule |
| The data volume | every sector sealed under a TPM-derived key |
| The wallet's key | the keyring capsule's vault gate |
| What a live boot holds in RAM | the shutdown wipe |
| Where the machine is on the network | the chosen anonymity network and a fresh station address at each bring-up |
| The package store | nothing: the project states it is not encrypted |

## Adversaries

Every finding names one and the preconditions it needs.

| ID | Adversary | Starting position | The project's matching section |
|---|---|---|---|
| A1 | A hostile or compromised capsule | Runs in user space with the capabilities its manifest grants and no others | A hostile app or capsule, in `kernel:docs/overview/threat-model-assets.md` |
| A2 | A remote network attacker | Can send arbitrary data to any service the machine exposes | Reaching a service that carries traffic off the machine, same page |
| A3 | A hostile or faulty device, or someone with physical access | Can attach a device, replace storage or firmware, or roll back stored state | `kernel:docs/overview/threat-model-a-hostile-or.md` |
| A4 | A supply-chain attacker | Controls a dependency, a build script, a toolchain, a firmware blob, a CI step or a published capsule | `kernel:docs/overview/threat-model-a-tampered-image.md` |
| A5 | A tenant or operator in a hosted deployment | Another tenant on the same machine, or an operator with access to the host | none |

A1 is the central adversary of a capability kernel. A weakness that only a trusted capsule can reach ranks below a logic error that any capsule can reach.

A5 is not in the project's threat model, because the project does not yet ship a hosted deployment. The audit includes it so that the work for hosted use is done and recorded, and every A5 finding says it lies outside the project's current model.

## Trust boundaries

1. Firmware and the loader, to the kernel.
2. The kernel, to user-space capsules.
3. One capsule, to another, across IPC.
4. A capsule, to a device, across MMIO and DMA.
5. The machine, to the network.
6. The build, to the release.

## Assumptions the audit does not test

- The CPU and the TPM behave as their specifications say. Where a project claim depends on one specific behaviour, the report names it.
- The cryptographic primitives are sound as designed. The audit tests their implementation and their use.
- The compiler is correct. The audit notes where a proof depends on that.

## How a flaw is placed in the model

A flaw is in the model if an adversary above, from the listed starting position, can change an asset's state or learn something it should not. A flaw that needs a stronger starting position is recorded with that precondition and scored lower. A reviewer who changes the model writes down the change and the reason in the engagement baseline.
