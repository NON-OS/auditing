# WS13. Claims and privacy verification

Whether what the project says about security and privacy is true, in the words it says it. Work from [claims/claims.json](../claims/claims.json) and [docs/claims.md](../docs/claims.md).

## Look for

- [ ] Run the project's own claim-checking tools on both targets and keep the output (the table in [docs/claims.md](../docs/claims.md)).
- [ ] Run `scripts/check_citations.py kernel` on both targets and list the citations that no longer resolve in the pages that carry security claims.
- [ ] Take each claim in the register and answer every question in its `to_establish` list before giving a verdict.
- [ ] Search the website, the README, the release notes, the documentation and the setup screens for claims that are not in the register, and add them word for word.
- [ ] For each claim, find the code, test or proof that backs it. If there is none, say so.
- [ ] Define each loaded word in the claim (proved, attested, private, wiped, every, no telemetry, reproducible) as the system uses it.
- [ ] Write a test for each behavioural claim and run it: no writes to disk in a live session, no telemetry from an idle machine, no traffic outside the chosen route including name lookups, memory cleared at shutdown, local inference with no network.
- [ ] Separate what happens on an orderly shutdown from a crash, a power cut and a cold-boot attack, for every claim about memory or data being gone.
- [ ] Check each count in a claim (functions, theorems, harnesses, drivers, programs) against the evidence file at a pinned commit.
- [ ] Check that the numbers and versions on the website, the README and the release notes agree with each other and with the release.
- [ ] Identify every outbound network path, by capsule and destination, and compare with the project's own list of egress.
- [ ] Identify metadata the system exposes even when content is protected: timing, packet sizes, addresses, the device model, the software version.
- [ ] Check each claim about what the system does not do, such as no telemetry, against the possibility that a later capsule or an update changes it.
- [ ] For every verdict short of verified, write a wording the evidence supports.

## Evidence to keep

- The filled register entry: verdict, evidence, commit, caveats, suggested wording.
- Each test, its command and its captured output.
- The list of outbound paths with the capsule behind each.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
