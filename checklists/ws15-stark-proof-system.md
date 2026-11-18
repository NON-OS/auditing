# WS15. The STARK proof system

The proof system behind capsule admission and the attestation path: `NON-OS/STARKs` at the commit the kernel pins in its lock files, `a41bb8bb0dacfea614acc6fb500d0b96abd78d2b`. The audit reads and tests exactly that commit.

## Look for

- [ ] Field arithmetic over Goldilocks and its extension: reduction, multiplication, inversion, and edge values near the modulus, tested against a big-integer reference.
- [ ] Fiat-Shamir: every public input, commitment and parameter is absorbed before the challenge that depends on it, with domain separation. A prover-controlled value the transcript does not bind is the weak Fiat-Shamir pattern.
- [ ] Merkle commitments: leaf and node separation, path length, index bounds.
- [ ] FRI: folding, the number of queries against the claimed security, grinding, the final degree check, out-of-domain sampling.
- [ ] Constraints: underconstrained columns, boundary and transition constraints that miss a row, public inputs bound to the trace. Start with the statement the kernel's attestation path checks.
- [ ] Verifier robustness: wrong lengths and counts, non-canonical field encodings, truncation and trailing bytes, under a fuzzer.
- [ ] The security level in the code against the proven and conjectured figures the documentation states.
- [ ] The Lean core: built, its axioms listed, and whether its statements describe what the Rust code does.

## Evidence to keep

- The parameters read from the code, beside the documented figures.
- Every harness and fuzz target written, with its run time and result.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
