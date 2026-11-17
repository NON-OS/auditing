# Tools and pipeline

The audit uses three groups of tools: checks the project already runs in CI, tools in the project's tree that the audit runs and extends, and tools the audit adds. Each row says which group it is in, so a reader can tell what was already true from what this audit brings.

## Already running in the project's CI

| Tool | What it covers | Workflow |
|---|---|---|
| Lean proofs, including the extraction of kernel functions | properties of kernel functions | `kernel:.github/workflows/verify.yml` |
| Verus | capability model theorems | `kernel:.github/workflows/verify.yml` |
| Kani | bounded model checking over 17 proof crates | `kernel:.github/workflows/verify.yml` |
| cargo-fuzz | nightly runs over the parsers of untrusted input, 30 minutes per target, with the targets listed in `kernel:fuzz/targets.json` | `kernel:.github/workflows/fuzz.yml` |
| cargo-audit and cargo-deny, run by `nonos-verify supply-chain` | dependency advisories, licence rules and the duplicate dependency surface | `kernel:.github/workflows/ci-supply-chain.yml` |
| Reproducibility | three machines build the compiled artifacts from one commit with no shared cache, and `nonos-verify reproducible` fails unless all name the same bytes. The sealed image is not compared, by design | `kernel:.github/workflows/ci-reproducible.yml` |
| Cross-capsule isolation | one capsule against another over the surface rules, guard pages, driver grant windows, the system-call capability table and user-copy bounds | `kernel:.github/workflows/ci-isolation.yml` |
| Adversarial tamper test | `nonos-verify adversarial` flips bits in a valid signed capsule, expires its windows, truncates it and cross-binds it, and asserts every one is rejected | `kernel:.github/workflows/ci-adversarial.yml` |
| SBOM | a CycloneDX bill of materials computed from the pins | `kernel:tools/nix/sbom.nix` |

## The project's own claim-checking tools, run by the audit

The project documents these in `kernel:docs/security/checking-the-claims.md`. The audit runs every one on both targets in phase 0, keeps the output, and extends them where a claim needs more than they test.

| Tool | Claim it tests |
|---|---|
| `kernel:tools/nonos-cap-audit`, `kernel:scripts/cap_audit.py`, `kernel:scripts/check_cap_parity.py`, `kernel:scripts/check_unenforced.py` | every capability and control is enforced |
| `kernel:tools/nonos-assumptions` | the assumption register is complete |
| `kernel:tools/nonos-mutant` | a removed control is noticed |
| `kernel:tools/nonos-pcap-egress`, `kernel:tools/nonos-egress-audit` | a boot sends nothing unexpected |
| `kernel:tools/nonos-amnesic-check` | an amnesic boot writes nothing |
| `kernel:tools/nonos-flip-byte` | a tampered artifact is refused |
| `kernel:tools/nonos-proof-coverage` | what the proofs cover |
| `kernel:tools/nonos_system_map.py` | the whole-image report and the authority map |

## Added by this audit

| Tool | What it does | Status |
|---|---|---|
| `scripts/check_citations.py` | Checks that cited source locations exist, in this repository's docs and in the kernel's | built, tested |
| `scripts/metrics.py` | Sizes the tree: lines, `unsafe`, inline assembly, allowances, lock-file packages | built, tested |
| `scripts/validate_claims.py` | Holds the claims register to its evidence rules | built, tested |
| `scripts/validate_findings.py` | Holds published findings to the disclosure rules | built, tested |
| `scripts/leak_guard.py` | Keeps unfixed findings, keys and real addresses out of this repository | built, tested |
| Structure-aware syscall and parser fuzzers | Reach the kernel's entry points from QEMU | to build in phase 3 |
| QEMU fault injection with a software TPM | TPM errors, truncated trailers, bad firmware tables | to build in phase 3 |
| Miri, cargo-geiger, cargo-vet | Undefined behaviour in host-portable logic, an unsafe inventory, dependency provenance | to add in phase 0 |
| Semgrep and CodeQL rules | The project's own unsafe and capability patterns | to write in phase 2 |
| Ghidra and objdump on the sealed bytes | That wipes survive the optimiser, and that secret-dependent code runs in constant time | to run in phase 3 |

## How the work is run

The audit is run by cloud routines, each working on one workstream and writing to a private repository. [`routines/`](../routines/README.md) has the prompts, the generator and the limits of that setup. Candidate findings go through the refutation step in [method.md](method.md) before anyone reads them as findings.

## Tools from outside

A project that builds audit, fuzzing or verification tools is invited to run them against the kernel. A report goes to the maintainers first, by the route in [disclosure.md](disclosure.md). The audit credits the tool and its author in the finding.
