# Claims register

Every public claim the project makes about its security and privacy, copied word for word from
where it is made, with what the audit must establish before the claim can be called true.

The method is in [docs/claims.md](../docs/claims.md). The register is
[`claims.json`](claims.json), checked by `scripts/validate_claims.py`.

A claim starts as `unverified`. A verdict is recorded only with its evidence and the commit it
was checked at. A claim that turns out to be overstated or false is reported to the maintainers
first, and the verdict is published after the wording has been corrected or the maintainers have given their reason for keeping it.
