# WS16. x86-64 architecture code

`kernel:src/arch` and `kernel:src/interrupts`, about a quarter of the kernel: the code closest to the hardware, where one mistake undoes every protection above it.

## Look for

- [ ] System-call and interrupt entry and exit: register save and restore, swapgs, the stack switch, what a user controls on entry, and kernel state left behind on return.
- [ ] The interrupt and descriptor tables, the TSS and IST stacks, double fault and NMI handling, nested interrupts.
- [ ] Page tables: user and kernel separation, W^X, the NX, SMEP and SMAP setup, TLB shootdown across CPUs, and mapping changes while another CPU runs.
- [ ] Speculation: the mitigations present, and whether the documentation states the gaps accurately.
- [ ] SMP: CPU bring-up, per-CPU data, locks taken in interrupt context.
- [ ] The IOMMU backends, VT-d and AMD-Vi, with WS6: the behaviour when remapping is off or faulty.
- [ ] Every inline assembly block: constraints, clobbers and what it assumes.

## Evidence to keep

- For each entry and exit path, the registers and state it saves, checks and restores, with citations.
- Which items were tested under QEMU, and on which image.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
