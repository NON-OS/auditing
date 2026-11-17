# WS3. Syscall layer and capabilities

Every entry point from userland into the kernel, and the capability model behind it.

## Look for

- [ ] Per syscall: argument validation, user pointer handling, lengths, alignment, integer overflow, double fetch from user memory.
- [ ] Error paths that leave state partly changed.
- [ ] User copy: bounds, overflow of address plus length, wrap, zero length, non-canonical and kernel addresses, copies that straddle pages.
- [ ] The registry index uses open addressing with a probe loop. Confirm lookup always terminates, that table construction cannot collide or overflow, and that no attacker-chosen id causes a long probe in ring 0.
- [ ] Where a proof bounds the probe loop, confirm the bound is real for every build profile.
- [ ] Capability derivation, attenuation, transfer over IPC and revocation.
- [ ] Caller identity: how a service learns who called it, and whether that binding can be forged by name squatting or a restarted process.
- [ ] Special capabilities (debug, attestation read, device and DMA, the admin split): what holds them and what follows if one is granted by mistake.
- [ ] A structure-aware syscall fuzzer running in QEMU.

## Evidence to keep

- Per syscall: the validation, quoted, with file and line.
- Fuzzer configuration and the corpus.
- A table of capability against holders.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
