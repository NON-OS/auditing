# Claims

A security product is trusted for what it says it does. The audit checks the saying as well as the doing. Each public claim is tied to the code, the test or the proof behind it, and the meaning of each word in it is written down.

## The register

[`claims/claims.json`](../claims/claims.json) holds one record per claim, copied word for word from where it is made:

| Field | Meaning |
|---|---|
| `id` | `C-NNN`, never reused |
| `category` | boot-trust, capsule-isolation, proofs, privacy, network, ai, hardware or build |
| `text` | The claim as published |
| `source` | A page and the date retrieved, or a file and the commit |
| `to_establish` | The questions that must be answered before a verdict |
| `verdict` | `unverified`, `verified`, `verified-with-caveats`, `overstated`, `false` or `unverifiable` |
| `evidence`, `checked_at`, `reviewed_at` | What backs the verdict, the commit it was checked at, and the date |
| `caveats`, `suggested_wording`, `reason` | What the claim does not cover, a wording the evidence supports, and why a claim cannot be checked |

`scripts/validate_claims.py` enforces the rules: a verdict needs evidence and a commit, a verdict short of `verified` needs a wording the evidence supports, and an `overstated` or `false` verdict is published only after the maintainers have corrected the wording or have been told and have chosen to keep it.

## Verdicts

- **verified.** The claim holds as worded, and the evidence reproduces.
- **verified-with-caveats.** It holds, but a reader would assume more than is true. The caveat and a more precise wording are recorded.
- **overstated.** Part of it holds, and the wording promises more than the evidence supports.
- **false.** The evidence contradicts it.
- **unverifiable.** No test or review can settle it as worded. The reason is recorded and a checkable wording is suggested.

## What gets run

A claim about behaviour is tested by running the behaviour. The project already ships most of the tools, and the audit runs them on both targets and keeps the output (`kernel:docs/security/checking-the-claims.md`):

| Claim | Command, as the project documents it |
|---|---|
| A boot sends nothing unexpected | `python3 tools/nonos-pcap-egress EGRESS --ingress INGRESS --json report.json`, then `python3 tools/nonos-egress-audit` |
| An amnesic boot writes nothing | `python3 tools/nonos-amnesic-check target/qemu-virtio-blk.img --record target/amnesic-before.txt`, then `--against` the same file after the boot |
| Every capability is enforced | `python3 scripts/cap_audit.py --strict`, `python3 scripts/check_cap_parity.py`, `python3 scripts/check_unenforced.py` |
| A removed control is noticed | `python3 tools/nonos-mutant --check` |
| The assumption register is complete | `python3 tools/nonos-assumptions` |
| A tampered artifact is refused | `python3 tools/nonos-flip-byte` and `make nonos-mk-tamper-run` |
| The whole-image authority map | `python3 tools/nonos_system_map.py --fast` |

The audit extends them where a claim needs more: idle egress over a full day, memory after an orderly shutdown against a crash and a power cut, and local inference with the network capsule absent.

## Words that need a definition

Some words carry more than the evidence does. For each one used in a claim, the audit writes down what it means in this system and what it does not:

| Word | Question |
|---|---|
| proved | What statement, proved by what, about which artefact, under which assumptions? |
| attested | By whom, over what, and what does a verifier learn? |
| private | Against whom, and what is still visible to them? |
| wiped | What is cleared, by what mechanism, and in which events? |
| every | Is there any path that is not covered, including development and recovery paths? |
| no telemetry | No traffic, no stored identifier, or no setting for it? Measured how? |
| reproducible | Which artifacts, on which machines, and what differs when they disagree? The project's lane compares the compiled artifacts and not the sealed image, because signing draws fresh randomness (`kernel:.github/workflows/ci-reproducible.yml`) |

## Documentation drift

A citation in a doc that points at a file that no longer exists is a claim the reader cannot check. `scripts/check_citations.py kernel` counts them in the project's own docs. The current count is in [status.md](status.md).

## Publication

A verdict of `overstated` or `false` goes to the maintainers first. It is published once the wording has been corrected, or once the maintainers have said in writing that they will keep it. The register records the correcting commit, or the maintainers' reason.
