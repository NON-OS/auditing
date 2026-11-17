# Contributing

The most useful contributions are the ones the audit cannot produce alone.

- **A tool.** An auditing, fuzzing or verification tool that finds something in the kernel, or a harness for a parser the audit has not reached. [docs/pipeline.md](docs/pipeline.md) says what is covered.
- **A checklist item** for a bug class the checklists miss, with a reference to where it has occurred.
- **A reproduction** of a published finding on a different target, or a failed reproduction.
- **A correction** to a document where it overstates, understates or is wrong.

Reports of vulnerabilities do not belong here. They go to `team@nonos.systems`, as [SECURITY.md](SECURITY.md) explains. No unfixed vulnerability, key or real address goes in a pull request, in any form.

## Before a pull request

```bash
make check
```

A pull request that fails it is not reviewed. If you cite the kernel, write the path inside the kernel repository with a `kernel:` prefix, and line numbers where they matter, so that `make citations` can check it.

## Writing

State what is true and how it was checked. Give the commit a number or a location refers to. Use straight quotes, sentence-case headings and no em dashes, en dashes or ellipsis characters. Leave out words that claim importance without a fact behind them. `scripts/style_check.py` enforces the mechanical part, and review does the rest.

## Commits

One purpose per commit, with a message that says what changed and why. A commit that contains material written or edited by Claude ends with the trailer set out in [docs/ai-use.md](docs/ai-use.md).

Every change to a checklist, the severity table or a script is reviewed by someone other than its author. The reviewers are listed in `.github/CODEOWNERS`.
