# WS14. Explainability

Whether a reader who is not a kernel engineer can learn what the system does and how to check it. Follow [docs/explainers.md](../docs/explainers.md).

## Look for

- [ ] Write one explainer for each mechanism the audit examines, in the fixed order of the explainer format.
- [ ] Every step in an explainer names the code that does it, with file and line at the audited commit.
- [ ] Write the protects-against and does-not-protect-against sections with equal care.
- [ ] Give commands a reader can run to check the mechanism, and the output they should see. Run them.
- [ ] State the status of each part as proved, tested, reviewed or assumed, with links.
- [ ] Say where the audit could not establish something, and do not fill the gap.
- [ ] Have a person who did not write the explainer read it and report what was unclear. Revise until they can explain it back.
- [ ] Start with the mechanisms that most claims depend on: the boot chain, capsule spawn and its checks, capabilities, the enrolment proof, nsh attestation, the network routes, memory clearing and the data volume.
- [ ] Keep a glossary of every term used, in plain words.

## Evidence to keep

- The explainer, with each code reference verified at the commit.
- The reader's notes from the review.
- The output of each check command.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
