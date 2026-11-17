# WS11. Review of the formal verification

What the proofs establish, and where the documentation says more.

## Look for

- [ ] For each Lean theorem, Verus theorem and Kani harness: the statement, the code it covers, and what it assumes.
- [ ] The gap between model and shipping code: files mounted into proof crates by path, and code that is tested but not proved.
- [ ] Extraction: what is extracted and what is only modelled.
- [ ] Axioms: every one is stated and justified. Search for `sorry`, vacuous specifications and trivially true statements.
- [ ] Kani bounds: each unwind bound is backed by an unwinding assertion, and holds for every profile.
- [ ] Trust in the checkers: the compiler, the Lean kernel, the solver.
- [ ] Compare each proof claim in the documentation with the table you built.

## Evidence to keep

- A table: claim, proof, code covered, assumptions, gaps.
- A list of documentation claims the proofs do not support.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
