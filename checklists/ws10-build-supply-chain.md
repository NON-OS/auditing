# WS10. Build, supply chain and release

Whether the thing that ships is the thing that was reviewed.

## Look for

- [ ] Reproducibility: rebuild the sealed bytes independently and record what differs.
- [ ] Dependencies: audit every lockfile for known advisories, and review build scripts, procedural macros and git or path dependencies.
- [ ] Vendored and third-party code: provenance and patches.
- [ ] Toolchain and nix pins, and how they are fetched.
- [ ] CI workflows: injection through untrusted input, token permissions, secrets, actions pinned by hash.
- [ ] Scratch-key lanes: confirm no production path can accept a scratch trust chain.
- [ ] Development-only features and capsules: confirm none can reach a release image.
- [ ] Seal and key flows: where key material is read and written, and whether any step can leak or mis-sign.

## Evidence to keep

- The rebuild log and a diff of outputs.
- The dependency report.
- A table of workflow against permissions.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
