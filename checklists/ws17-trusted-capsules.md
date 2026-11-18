# WS17. Trusted capsules

The user-space capsules that hold keys, secrets or the network: the keyring, the vault, the wallet, the file system and its gate, the nsh login, the network stack, the Nym and Anyone clients, the crypto service and the NVMe driver.

## Look for

- [ ] Who may ask each capsule for what. The check must use the sender the kernel stamps, never a value the caller sends.
- [ ] Secrets: where keys are derived, held, zeroised and written, and whether any reach a log, a file another capsule reads, or the network.
- [ ] Parsing of everything that arrives from another capsule or the network: lengths, counts, nesting, integer overflow, panics.
- [ ] The file gate: which paths each capsule may read, write and delete, and whether records that carry security state are guarded.
- [ ] The network capsules: what leaves the machine, whether a request can reach a host outside the documented list, DNS and TLS handling.
- [ ] The wallet: key storage, signing confirmation, and what a malicious request can make it do.

## Evidence to keep

- Per capsule, the requests it serves and the check each one makes, with citations.
- Host tests and fuzz runs, with their results.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
