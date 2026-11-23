# NKA-CLOSED-2026-001: Measured-boot gate falling back to the loader's own word on a TPM error is documented, intended behavior

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | kernel measured boot and loader-check gate |
| Location | kernel:src/security/boot/loader_check/run.rs:34-55, kernel:nonos-boot-measure/src/gate/verdict.rs:66-75, kernel:src/kernel_core/init/entry/loader_refusal.rs:27-29 |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-17 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that when the kernel cannot read a TPM measurement log or the TPM returns an error on PCR 4 or the rollback floor, the loader-check gate silently falls back to trusting the loader's own self-reported word about which kernel ran, and that this fallback was an undocumented weakness a replaced-loader adversary could use.

## Why it is not a finding

The fallback is real and reproduces, but it is documented, not a gap. The project's own measured-boot documentation states plainly that without a log, or when the kernel cannot read PCR 4 or the rollback floor, the kernel falls back to the loader's self-reported word, checked only against a floor of zero, and that this self-reported path is taken on a Hardened boot too when a project option lets that verdict through. The adversary the candidate named, a replaced loader, gains nothing beyond what it already has: with secure boot off and its own loader in place, the attacker already controls which kernel runs, since the loader is what checks the kernel's signature. Against the genuine kernel it receives an honest self-reported verdict and a changed measurement that a dependent key schedule already treats as a different machine.

## Routes tried

1. Is the TPM-error fallback undocumented, as the candidate claims? No. The project's own measured-boot and rollback-protection documentation describes the exact fallback and its floor-of-zero behavior, including the Hardened-boot case.
2. Does a replaced-loader adversary gain anything from this fallback it does not already have? No. That adversary already controls which kernel boots; the fallback changes nothing about what it can do to the genuine kernel, and its own replaced kernel can already report anything.
3. Does a TPM-bus adversary who can fail only the measurement reads, while a genuine loader and kernel run, gain anything? No route was found: the kernel then admits an older signed record at the floor, but booting an older loader changes the measurement that a dependent key schedule already uses, so the keys differ. A full dynamic test of this path was not run.
4. Is a related, informational-level wording question (certain status text implying more certainty than the gate actually provides) in scope for this candidate? Treated as a separate, minor documentation point, not re-examined further here.

## Evidence

Checked independently of the original write-up: yes.

- An independent test, not derived from the original candidate write-up, was added to a local copy of the kernel's own boot-measurement and attestation-path crates, using their own existing test fixtures.
- The test exercised the gate's measured path with a stale record (expected failure) and the self-reported path with the same record (expected success), against the real gate code at the audited commit.
- Both outcomes matched the behavior the project's documentation already describes, confirming the fallback is real but intended, not an undocumented gap.
