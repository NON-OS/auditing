# auditing

A public security audit of the [NØNOS microkernel](https://github.com/NON-OS/microkernel): the method, the tools, the claims under test and, once each is fixed, the findings.

**Status.** Phase 0. The method and tooling are published, no workstream has started, and there are no findings. [docs/status.md](docs/status.md) has the numbers.

This is a first-party audit, done by the project's own team. It is not independent and does not replace an independent audit. What it offers is that the method, the tools and the results are open to be checked.

## How it works

```
 14 checklists ──► candidate ──► refutation by a second ──► finding ──► maintainers ──► fix ──► published
                                  reviewer, from scratch                                        here

 26 public claims ──► the project's own checks, run on the release and on main ──► verdicts
```

- A candidate becomes a finding only by reproduction, or a complete chain from attacker to effect, and only after a second reviewer fails to break it.
- Nothing unfixed is published. [`scripts/leak_guard.py`](scripts/leak_guard.py) and [`scripts/validate_findings.py`](scripts/validate_findings.py) fail a change that adds it.
- Every statement about the code cites a source location, and [`scripts/check_citations.py`](scripts/check_citations.py) checks that it exists at the audited commit.
- No report says a component is secure. It says what was tested and what was not.

## Start here

| If you want to | Read |
|---|---|
| Know what is audited and how it is built | [docs/system-model.md](docs/system-model.md), [docs/scope.md](docs/scope.md) |
| See who the audit assumes attacks | [docs/threat-model.md](docs/threat-model.md) |
| Bring an audit, fuzzing or verification tool | [docs/pipeline.md](docs/pipeline.md), [docs/disclosure.md](docs/disclosure.md) |
| Check a public claim | [docs/claims.md](docs/claims.md), [`claims/`](claims/) |
| Report a vulnerability | [SECURITY.md](SECURITY.md) |
| See how the AI assistant is used | [docs/ai-use.md](docs/ai-use.md) |

## In the repository

| Path | What it holds |
|---|---|
| [`docs/`](docs/README.md) | Scope, method, system model, threat model, severity, disclosure, tools, claims, status |
| [`checklists/`](checklists/README.md) | One checklist per workstream: the bug classes to look for and the evidence to keep |
| [`claims/`](claims/README.md) | The claims register |
| [`findings/`](findings/README.md) | The finding schema, the template and the published findings |
| [`reports/`](reports/README.md) | Published reports |
| [`routines/`](routines/README.md) | The prompts that run the audit in cloud environments |
| [`scripts/`](scripts/) | The checks and measurements, with tests in [`tests/`](tests/) |
| [`targets/`](targets/targets.toml) | The audited tag and branch, and the commit the docs were last verified against |

## Checks

```bash
make check                                 # style, links, findings, claims, leaks, tests
make citations KERNEL_DIR=../microkernel   # every kernel: citation resolves in a kernel checkout
```

`make check` needs only Python 3. The citation check needs a checkout of the kernel at the commit in [`targets/verified-at.txt`](targets/verified-at.txt).

## Licenses

Code (`scripts/`, `tests/`, `routines/`, `.github/`, `Makefile`, the finding schema) is [Apache-2.0](LICENSE). Writing and data (`docs/`, `checklists/`, `claims/`, `findings/`, `reports/`, this file) are [CC BY 4.0](LICENSE-docs). Use any of it, in your own audits too, with attribution.
