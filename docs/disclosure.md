# Disclosure

## For anyone reporting a kernel vulnerability

Follow the project's own policy: `kernel:docs/security/reporting-a-vulnerability.md` and `kernel:SECURITY.md`. Send the report to `team@nonos.systems`. Do not open a public issue or pull request about a security bug before it is fixed.

The project publishes no key for reports and commits to no response time and no disclosure deadline in the current release. If you plan to publish, say when in your report so that a fix can be ready first. If you need encryption, say so in a short first email without details, and agree a channel before you send them.

## How the audit's own findings move

1. A worker writes a candidate and labels it confirmed, supported or hypothesis.
2. A second reviewer tries to refute it ([method.md](method.md)).
3. A candidate that survives becomes a finding and is written up in the private repository.
4. The maintainers are told privately, with the evidence. A critical finding is reported the same day.
5. The maintainers fix it, accept the risk, or dispute it.
6. The finding is published here only after step 5, in the form the schema describes.

Nothing is published before step 5. [`scripts/publish_finding.py`](../scripts/publish_finding.py) is the only way a finding enters this repository: it needs the maintainers' outcome, validates the finding against the schema and the policy above, refuses anything the leak guard rejects, and makes one commit that a person then pushes. `scripts/validate_findings.py` and `scripts/leak_guard.py` fail a change that adds an unpublished finding.

## Statuses of a published finding

| Status | Meaning | Required |
|---|---|---|
| `fixed` | The maintainers fixed it | the fix commit and the date of the fix |
| `accepted-risk` | The maintainers decided not to fix it | their reason, in their words |
| `disputed` | The maintainers disagree that it is a finding | their reason, and the audit's reply |

The project sets no deadline, so the audit does not publish on a timer. That is a weakness of a first-party audit: the party that decides when to publish is the party being audited. An independent reviewer who reports to the project is free to apply the 90 day convention to their own report, and this repository will cite it.

## Documentation findings

A finding about the documentation, such as a citation to a file that does not exist, is not a vulnerability. It is reported and published without waiting.

## Problems in this repository

A script here that leaks something, mishandles a secret or can be abused is reported to the same address.
