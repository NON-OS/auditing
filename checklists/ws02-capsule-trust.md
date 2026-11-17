# WS2. Capsule trust, enrolment and the spawn gate

How the kernel decides that a capsule may run, and with which capabilities.

## Look for

- [ ] The spawn gate checks the capsule's bytes and its capability word. Can a changed capsule or a wider capability word start?
- [ ] Can a capsule be swapped between the check and the start?
- [ ] Enrolment under one policy root: how it commits to capsule hashes and capability masks (domain separation, second-preimage resistance, ordering, duplicates).
- [ ] Verifier soundness parameters (rounds, queries, field size, blowup) against the claimed security level.
- [ ] Proof malleability, and what the kernel verifies at boot compared with what the seal tool verifies offline.
- [ ] The seal tool keeps an enrolment when a check on the built bytes passes. Show that a changed capability word or a changed byte always fails that check.
- [ ] What the recorded enrolment commit binds and what it does not.
- [ ] Manifests, identity certificates, namespaces and globs, publisher keys.
- [ ] Revocation: is there a working path, and is it enforced at spawn?
- [ ] The image capability ceiling: confirm no capsule can exceed it by any route, and check it against every capsule's declared capabilities.
- [ ] Parity between declared capability bits, the manifest and the kernel's meaning of each bit.

## Evidence to keep

- A negative test for each way a capsule might change.
- The soundness parameters with their source.
- A table of capsule against declared and permitted capabilities.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
