# WS21: Verification engineering

The formal methods the project ships are re-checked in WS11. This workstream adds new ones where the audit found weaknesses or where the existing proofs stop, so that each confirmed finding ends with a check that would have caught it.

## Look for

- [ ] For every confirmed finding, a regression check that fails on the audited commit and passes once the proposed fix is applied: a Kani harness, a property test or a fuzz target. Write it, run it against the audited code, and record that it fails for the right reason.
- [ ] Kani harnesses for the attacker-facing arithmetic and bounds: ELF relocation and segment checks, page-table index math, IPC message sizes, syscall argument decoding, capsule manifest parsing. Prove the absence of overflow and out-of-bounds access, with the bounds stated.
- [ ] A structure-aware syscall fuzzer that runs inside the development build under QEMU: generated capsules that issue sequences of syscalls with valid and invalid capability words, with coverage feedback from the guest where possible. Keep the corpus between runs.
- [ ] Concurrency: model the IPC, scheduler and TLB shootdown protocols with loom or shuttle on host builds of the real code, and say which interleavings were explored.
- [ ] A protocol model (TLA+ or a small state machine checked exhaustively) of capsule admission and the rollback floor, with the properties the documentation claims, and any counterexample found.
- [ ] Gaps between the proofs and the code: properties the Verus and Lean proofs assume, checked against what the compiled code does, including at the binary level with objdump where the property is about the machine code.
- [ ] Differential testing of the kernel's parsers and the STARK verifier against independent implementations, with generated inputs.
- [ ] Fault injection on a running development build: failing allocations, TPM errors, IOMMU errors and corrupted capsule storage, and whether each one fails closed.

## Evidence to keep

Every harness, model and fuzzer as source, the exact command, the tool version and the result, so the maintainers can add them to the project's own CI.

## Notes

A harness that proves a property is a result even when nothing is broken. A counterexample is a candidate, with the trace as its reproduction.
