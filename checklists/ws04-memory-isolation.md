# WS4. Memory management and isolation

Paging, the kernel and user split, and everything that can break it.

## Look for

- [ ] W^X end to end: every mapping path, including remapping, shared memory, copy on write and any call that changes permissions.
- [ ] Kernel mapped into user tables, guard pages, stack and heap placement, address randomisation if any.
- [ ] Physical memory and MMIO exposed to user space.
- [ ] SMEP, SMAP and UMIP set on every CPU including application processors, and kept set across every path that touches the relevant registers.
- [ ] SMP bring-up races, TLB shootdown (a stale writable mapping after an unmap), IPI handling, per-CPU data, lock order and deadlock.
- [ ] Allocator and ring 0 unsafe code: use after free, double free, uninitialised memory, pointer provenance, mutable statics, aliasing.
- [ ] Inline assembly and foreign code: clobbers and calling conventions.
- [ ] Speculative execution: what is mitigated, and what the documentation claims.

## Evidence to keep

- A map of address spaces.
- Per mitigation: where it is enabled, quoted.
- Race reproductions where found.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
