# Disclosure

There are two paths, and they are different on purpose.

## For anyone reporting a kernel vulnerability

Follow the project's own policy: `kernel:docs/security/reporting-a-vulnerability.md` and `kernel:SECURITY.md`. Send the report to `team@nonos.systems`. Do not open a public issue or pull request about a security bug before it is fixed.

The project publishes no key for reports and commits to no response time and no disclosure deadline in the current release. If you plan to publish, say when in your report so that a fix can be ready first. If you need encryption, say so in a short first email without details, and agree a channel before you send them.

A report from outside the audit follows the project's policy, and the maintainers decide when it is published. The rules below are about the audit's own findings.

## How the audit publishes its own findings

The audit publishes every finding it confirms, in full, on the day it is confirmed. It does not wait for the fix.

1. A worker writes a candidate and labels it confirmed, supported or hypothesis.
2. A second reviewer tries to refute it ([method.md](method.md)).
3. A candidate that survives becomes a finding. It is written in the form of [the schema](../findings/schema/finding.schema.json).
4. The maintainers are told at once, with the evidence. A critical finding is reported the same day.
5. The finding is published in [findings/published](../findings/published/README.md) with status `open`, in full.
6. When the maintainers fix it, accept the risk or dispute it, the finding is updated in a new commit: a fix names the kernel commit, and the other two carry the maintainers' reason.

### Why

The audit is first-party, so the party that decides what is published is the party being audited. Publishing at confirmation takes that decision out of the maintainers' hands. No finding can be delayed, softened or dropped, and the public record shows how long each one stayed open. [`scripts/publish_finding.py`](../scripts/publish_finding.py) is the only way a finding enters this repository, and [`scripts/render_findings.py`](../scripts/render_findings.py) writes the readable pages and the index from the JSON.

### What it costs

An open finding is readable by anyone, including people who would use it. The audit publishes anyway and accepts that cost knowingly. It is the reason steps 2 and 3 exist: a candidate that has not been reproduced and has not survived a second reviewer is not published, so the record holds findings and not guesses.

### What stays private

- Candidates that are not yet findings: hypotheses, and candidates the second reviewer refuted. The audit reports how many there were and why they were dropped.
- Anything the leak guard rejects: keys, tokens, identifiers of an account, a chat or a session, and the addresses of real hosts.

### Statuses of a published finding

| Status | Meaning | Required |
|---|---|---|
| `open` | Confirmed and published, not yet decided by the maintainers | nothing more |
| `fixed` | The maintainers fixed it | the fix commit and the date of the fix |
| `accepted-risk` | The maintainers decided not to fix it | their reason, in their words |
| `disputed` | The maintainers disagree that it is a finding | their reason, and the audit's reply |

`scripts/validate_findings.py` and `scripts/render_findings.py --check` fail a change that breaks these rules or leaves a page out of date.

The project sets no deadline for fixes. The record makes a long delay visible, because each finding shows the date it was published and the date it was fixed.

## Documentation findings

A finding about the documentation, such as a citation to a file that does not exist, is not a vulnerability. It is published the same way.

## Problems in this repository

A script here that leaks something, mishandles a secret or can be abused is reported to the same address.
