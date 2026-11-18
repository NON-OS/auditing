# WS18. Fuzzing campaign

Every fuzz target the kernel ships, in `kernel:fuzz/fuzz_targets` and in the fuzz directories of the attestation path, the proof verifier, the boot measurement code and the userland proof crates, run as a campaign that grows across runs.

## Look for

- [ ] Every target builds. A target that does not is recorded with its error.
- [ ] Rounds over every target, the parsers of untrusted input first: ELF headers, attestation documents and quotes, TCG event logs, boot records, ACPI tables, device trees, certificates, DNS, image formats.
- [ ] A corpus kept per target between runs, so each run starts where the last stopped.
- [ ] Every crash minimised, rerun to confirm, and traced to its source line.
- [ ] Coverage per target, to show which parsers the fuzzers reach and which they do not.

## Evidence to keep

- Per target: total run time, executions, coverage where available, crashes.
- For each crash: the input as hex, the stack trace and the line.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
