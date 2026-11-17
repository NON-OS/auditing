# WS12. Unsafe code, panics and hygiene

The places where the language stops helping.

## Look for

- [ ] Inventory every unsafe block and every lint allowance that suppresses a safety lint. Grade the safety comments.
- [ ] Sample the highest-risk blocks for soundness.
- [ ] Panics and unwraps in ring 0 reachable from capsule input: a panic is a denial of service.
- [ ] Overflow behaviour (checked or wrapping) in kernel and capsule profiles.
- [ ] Allocation failure handling.
- [ ] Inline assembly and foreign function boundaries.

## Evidence to keep

- The inventory as a table, by crate.
- A reproduction for each reachable panic.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
