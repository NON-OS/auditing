# Security policy

## A vulnerability in the NØNOS kernel

Report it to `team@nonos.systems`, as the project's own policy asks (`kernel:SECURITY.md`, `kernel:docs/security/reporting-a-vulnerability.md`). Do not open a public issue or pull request about it before it is fixed, here or in the kernel repository.

The project publishes no key for reports, commits to no response time and sets no disclosure deadline in the current release. If you need encryption, say so in a short first email without the details and agree a channel first. If you plan to publish, say when in the report.

Include the commit or tag, the build profile, the machine or QEMU command line, the steps from a fresh boot, what you expected and what happened, and the serial console lines around it. The project's page lists what counts as a security bug and what to put in a report.

## A problem in this repository

A script here that leaks something, mishandles a secret or can be abused goes to the same address.

## How the audit handles its own findings

[docs/disclosure.md](docs/disclosure.md) sets out how a finding moves from candidate to publication. Nothing unfixed is published here.
