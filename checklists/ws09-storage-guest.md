# WS9. Storage, the data volume and the Linux guest

Persistent state, and the compatibility layer that runs foreign programs.

## Look for

- [ ] Filesystem and store parsers.
- [ ] Integrity and rollback of stored data.
- [ ] Encryption at rest, and what is stored unencrypted.
- [ ] Permissions on stored objects.
- [ ] Guest syscall translation and the guest-to-host boundary.
- [ ] Graphics and input paths used by guests, and what a guest process can do to the host capsule.

## Evidence to keep

- Parser fuzz corpora.
- A list of guest-reachable host interfaces.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
