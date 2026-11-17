# WS5. IPC, scheduling and process lifecycle

How capsules talk to each other, and how they start, run and die.

## Look for

- [ ] Endpoint and reply lifecycle, ownership, use after close.
- [ ] Message size and queue limits. Unbounded kernel allocation driven by a capsule.
- [ ] Starvation, and priority inversion.
- [ ] The service registry and naming: squatting, impersonation and restart races.
- [ ] Spawn bounds and resource accounting: can one capsule exhaust kernel memory, handles or process slots?
- [ ] Kill and reap paths, and resources orphaned by them.

## Evidence to keep

- Limits table: resource against the cap that bounds it.
- A reproduction for each exhaustion that works.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
