# WS7. Cryptography and secrets

Primitives, their use and the key hierarchy.

## Look for

- [ ] Implementations: Ed25519, ML-DSA-65 (version, patches, constant time), P-256, secp256k1, the hashes.
- [ ] Misuse: nonce handling, domain separation, key derivation inputs, key reuse across purposes.
- [ ] Randomness: sources, the kernel generator, early boot behaviour, reuse after a virtual machine snapshot.
- [ ] Key hierarchy: the data volume key and its policy binding, host keys, the keyring and the vault.
- [ ] Behaviour on TPM reset, key loss and recovery.
- [ ] Zeroisation, and the secret types that stop logging. Can a secret reach a serial log, a crash dump or disk in clear?
- [ ] Side channels in secret-dependent code.

## Evidence to keep

- Per primitive: version, source and test vectors run.
- The key hierarchy as a diagram, with what protects each key.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
