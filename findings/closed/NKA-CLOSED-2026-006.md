# NKA-CLOSED-2026-006: A guest process cannot acquire a device-broker grant to exploit missing window or clock-page checks

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | kernel cross-process memory mapping for sandboxed guest processes |
| Location | kernel cross-process guest memory mapping and unmapping syscalls |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-20 |
| Closed | 2026-11-23 |

## The claim

A candidate suspected that the syscalls for mapping and unmapping memory into a guest process lacked checks for device-broker memory windows and the shared clock page, so a guest holding such a grant could have its memory wrongly freed or exposed.

## Why it is not a finding

A guest process cannot hold a device-broker grant or share an address space with a process that does. Guest processes are created with an empty capability set, and every syscall that could request a device-broker grant is refused before it reaches the capability table for any process the kernel marks as a guest; unknown syscall numbers from a guest are routed to its supervisor instead of executed. No path was found by which a guest could obtain or share such a grant, so the precondition for the window and clock-page half of this candidate cannot hold. A separate, related finding about a different leak path through the same mapping syscall was already tracked on its own, independently.

## Routes tried

1. Checked whether a guest process can itself request a device-broker memory grant: every such syscall is refused for a guest before capability checks run.
2. Checked whether a guest could share an address space or holder group with a process that does hold a grant: guest processes and their threads are created and enrolled under their own identity, with no sharing path found.
3. Checked the shared clock page specifically: it is mapped only through an installation path that guest processes are not created through.

## Evidence

Checked independently of the original write-up: yes.

- Code reading only; not every possible caller of device-broker grant creation for a process other than the caller itself was enumerated.
- Independently confirmed in a separate clone of the repository that guest processes are created with an empty capability set via the exact call the original review cited, and that no live caller of device-broker grant creation for another process was found outside the already-reviewed paths.
