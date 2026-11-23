# NKA-CLOSED-2026-012: Formally unproved copies of the write-execute-exclusion rule exist only in dead code on the architecture the kernel ships

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | memory-permission encoding and the kernel's machine-checked write-execute-exclusion proof |
| Location | kernel memory-paging permission encoder covered by the proof; three other, structurally similar but unproved permission encoders elsewhere in the tree |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-19 |
| Closed | 2026-11-23 |

## The claim

A candidate found that the kernel's machine-checked proof of write-execute exclusion for page permissions covers one permission-encoding type, while three other, textually similar encoders elsewhere in the tree carry the same rule without the same proof coverage.

## Why it is not a finding

The project's own documentation already states the proof's exact scope and does not claim wider coverage, so there is no overstated guarantee to report. Of the three unproved encoders, none was found to have a live caller anywhere in the tree on the architecture the kernel actually ships; the project's own documentation independently states the same about one of them. The one route that could in principle reach an unproved encoder, resolving a copy-on-write fault, calls into the proved encoder instead and already fails closed rather than producing a writable-and-executable page.

## Routes tried

1. Compared the project's documented proof scope against the candidate's claim and found no overstatement: the documentation already states the narrower scope plainly in multiple places.
2. Searched for any live caller of each of the three unproved encoders outside their own modules, and found none; the project's own documentation independently confirms this for one of them.
3. Traced the live copy-on-write fault path, the one plausible route to an unproved encoder, and confirmed it calls the proved encoder, which itself refuses to produce a writable-and-executable page.
4. Did not examine other processor architectures the project may support, or every raw low-level permission write outside the paths already covered.

## Evidence

Checked independently of the original write-up: yes.

- Code reading only; the machine-checked proof itself was not rerun as part of this review.
- Independently re-ran the caller search in a separate clone of the repository: no call to the unproved encoder outside the paging and mmio modules was found, and the process/address_space fork module's own copy-on-write helpers have no caller outside that module.
