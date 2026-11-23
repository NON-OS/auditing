# NKA-CLOSED-2026-004: MkMunmap cannot free a page another process or the kernel still relies on

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | kernel memory management, user-space unmap syscall |
| Location | kernel syscall memory unmap path; kernel paging manager's mapping-removal and address-space-teardown code |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-17 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that MkMunmap could free a physical frame still aliased by another mapping, through a path outside its three explicit guards (clock page, device windows, and length bounds).

## Why it is not a finding

Every path that frees a frame goes through the same mapping-removal mechanism the process's own exit teardown uses, and every one of those paths traced back to a frame the calling process itself owns. The guards MkMunmap checks explicitly (the clock page and device windows) are the only two exceptions that actually exist in the live code; no other shared-frame path was found that MkMunmap could reach.

## Routes tried

1. Traced every code path that inserts a page into a process's address space to determine whose frame it maps: user heap mappings, loaded program segments, the user stack, and cross-process window mappings each allocate or own their own frames.
2. Checked the one shared case not already guarded, the clock page, and confirmed it is covered by an explicit check in the unmap syscall.
3. Cross-checked against the process exit path, which frees every present user page with the same three exclusions; since exit relies on no further exclusion existing, an unguarded alias would already be a double-free at every process exit, not only at unmap.
4. Searched for any copy-on-write or explicit frame-sharing mechanism between processes: none was found in the current tree.

## Evidence

Checked independently of the original write-up: yes.

- Ran the project's own kernel-proof test suite covering the device-window guard and the surface-unmap rules: all tests passed.
- No dynamic test of the unmap syscall on a booted kernel was performed.
