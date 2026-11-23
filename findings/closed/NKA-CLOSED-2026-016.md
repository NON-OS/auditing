# NKA-CLOSED-2026-016: A known timing-safety advisory in a cryptographic dependency does not apply to the code path the kernel's key-decapsulation actually uses

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | post-quantum key-decapsulation dependency chain |
| Location | kernel's key-decapsulation code and its cryptographic dependency chain |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-20 |
| Closed | 2026-11-23 |

## The claim

A candidate found that a cryptographic utility library at the version pinned by the kernel's dependency tree is subject to a published timing-safety advisory, and that the kernel's hybrid key-decapsulation routine depends on it, raising a secret-dependent-timing concern.

## Why it is not a finding

The advisory and the affected version pin are both real, but the specific operations the advisory names are not the ones the kernel's decapsulation path actually exercises. Source-level tracing of the one constant-time operation on the decapsulation path showed it resolves to a different, unaffected implementation than the flagged functions, and a targeted disassembly of the compiled code for that exact operation shape showed no data-dependent branch, only a fixed-length loop whose only conditional jump is the loop counter. The advisory's other affected case applies only to 32-bit targets, and every target the kernel builds for is 64-bit.

## Routes tried

1. Traced the exact sequence of library calls the decapsulation routine's implicit-rejection step uses, down to the specific internal functions invoked for the array comparison and conditional-select operations involved.
2. Confirmed those specific internal functions resolve to a different, separately-versioned dependency not covered by the advisory, rather than to the flagged constant-time mask generators.
3. Checked the advisory's other affected case, certain comparisons on 32-bit targets: every build target in the kernel's tree is 64-bit, so this case does not apply.
4. Compiled the exact operation shape used on the decapsulation path in isolation and disassembled it, confirming the generated code is a fixed-length loop with no branch on secret data, only on the loop counter.

## Evidence

Checked independently of the original write-up: yes.

- Built a standalone, minimal reproduction of the exact call shape used on the decapsulation path, using the kernel's pinned dependency versions, and disassembled the resulting compiled code.
- Did not disassemble the entire decapsulation routine beyond this specific operation, and did not rerun statistical timing measurements beyond those already available.
