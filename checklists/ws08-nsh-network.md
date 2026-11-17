# WS8. nsh/1 and the network stack

The attested login protocol and every parser of network data.

## Look for

- [ ] Read the specification, then the server and client code. Handshake, hybrid key exchange, binding of the attestation document to the challenge.
- [ ] Replay, downgrade, the role table and revocation list, enrolment.
- [ ] What an unauthenticated peer can reach.
- [ ] Resource limits: one connection at a time. Can one idle or slow client hold the slot, and what are the time bounds?
- [ ] TLS and HTTP implementations, the TCP and IP stack, and the DHCP, DNS and NTP clients as parsers of attacker data.
- [ ] The mixnet client: parsing, and the anonymity assumptions it makes.
- [ ] Capabilities held by the network-facing capsule and the blast radius of its compromise.

## Evidence to keep

- The protocol attack tree.
- Fuzz corpora per parser.
- A table of capsule against capabilities.

## Notes

Candidates for this workstream stay private until they are confirmed. A confirmed finding is published in `findings/published`, not in this file.
