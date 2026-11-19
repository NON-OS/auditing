# WS20: Performance and worst-case cost

How fast the kernel is on its hot paths, and how much an attacker can make it spend. Slow paths that an unprivileged capsule can trigger are availability bugs, so this workstream is security work as well as performance work.

The cloud sandbox has no hardware virtualisation. QEMU runs under software emulation there, so wall-clock timings from it are not evidence. Measure what does not depend on speed: instructions retired (QEMU's `insn` plugin, `-plugin libinsn.so`), memory, allocations, binary size, and host benchmarks of code that runs the same on the host.

## Look for

- [ ] Instructions retired for the hot paths on a running development build, per call: syscall entry and exit, a round-trip IPC message, a context switch, a page fault, `mmap` and `munmap`, capsule spawn. Record the method so later runs compare like with like.
- [ ] Every loop whose bound an unprivileged capsule controls, in the syscall, IPC, memory, loader and file-system paths. For each, the worst case in instructions and whether a global lock is held across it.
- [ ] Locks held across work that grows with input: the ELF loader lock, the page-table locks, the scheduler, the capsule store. Who waits, and for how long in the worst case.
- [ ] Capsule admission cost: STARK verification and signature checks, on the host with Criterion and in the kernel by instruction count. The largest proof and manifest the verifier accepts, and its cost.
- [ ] Boot cost by phase, from the serial log and instruction counts: loader, measurement, attestation, kernel init, first capsule.
- [ ] Memory: kernel heap use at idle and under load, per-process and per-thread overhead, page-table overhead, and how close a single capsule can push the heap to its limit.
- [ ] Binary size and composition of the kernel and loader (`cargo bloat`, `size`), and anything that grew without reason.
- [ ] Cryptography throughput on the host: SHA-2, BLAKE3, Ed25519, ML-DSA-65, ChaCha20-Poly1305, against an independent library as a reference.
- [ ] Scheduler fairness and starvation: whether one capsule can deny CPU time to others within its budget.

## Evidence to keep

The exact build, QEMU command and plugin, the numbers, and the script that produced them, so a later run can repeat the measurement on another commit.

## Notes

A result is a baseline unless it shows an attacker-triggered cost or a regression. Those become candidates like any other, with a reproduction.
