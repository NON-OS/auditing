# WS19. Open-source tool sweep

The standard open-source security tools, run over the kernel, its capsules, the vendored C and the proofs. A tool hit is a lead, not a finding: each is confirmed in the code or dismissed with a reason.

## Look for

- [ ] Miri on every host-testable crate: undefined behaviour in `unsafe` code.
- [ ] AddressSanitizer and UndefinedBehaviorSanitizer on the host tests, and loom where the code has locks or atomics with a host model.
- [ ] Clippy with the pedantic, nursery and suspicious groups, and cargo-geiger for an inventory of `unsafe` per crate and dependency.
- [ ] cargo-mutants on the proof crates that guard security decisions: which mutants survive.
- [ ] Semgrep with its Rust and secrets rules, and CodeQL for Rust.
- [ ] cargo-audit, cargo-deny and OSV-Scanner over every lock file, and OpenSSF Scorecard for the public repositories.
- [ ] The vendored C and assembly: the Clang static analyzer and cppcheck, and a constant-time test of the ML-DSA-65 signing path.
- [ ] Crypto test vectors: Project Wycheproof for Ed25519, ChaCha20-Poly1305, P-256 and HKDF, and NIST ACVP vectors for ML-DSA-65.
- [ ] lean4checker over the Lean trees.

## Evidence to keep

- A table of every run: tool, version, target, exact command, hits, confirmed, dismissed with the reason.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
