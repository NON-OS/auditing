# WS1. Boot chain and trust anchor

The path from firmware to a running kernel, and every check on it.

## Look for

- [ ] Both signatures of the hybrid scheme are required. Show that neither can be skipped, truncated or replaced by the other.
- [ ] Trailer parsing: the shared parser has more than one format path. Look for downgrade from a newer required format to an older accepted one.
- [ ] Trailer parsing: length confusion, fields read before they are authenticated, offsets taken from the data being checked.
- [ ] Boot-root record: ECDSA input checks (point on curve, zero and out-of-range values), signature malleability, low-s handling.
- [ ] Boot-root record: what it binds to, and whether an older valid record can be replayed.
- [ ] Measured boot: behaviour when the TPM is absent, returns errors or answers wrongly. Record what each profile accepts.
- [ ] The loader check has a measured verdict and a self-reported one. Find what a self-reported boot may do, and what an attestation document says about it.
- [ ] Rollback floor in TPM NV storage: how it is read, raised and protected, and what happens on first boot and after a TPM reset.
- [ ] Loader-to-kernel handoff: validation of every structure passed across, and time-of-check to time-of-use gaps.
- [ ] Trust placed in firmware-supplied data (memory map, ACPI pointers, framebuffer).
- [ ] Secure Boot states: what the production policy enforces compared with the QEMU profile.

## Evidence to keep

- The exact check, with file and line at the commit.
- A fault-injection run for each TPM and trailer case, with the log.
- A table of profile against enforced property.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
