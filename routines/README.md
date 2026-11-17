# Routines

The audit runs as a set of scheduled routines in Anthropic's Claude cloud environments: a lead, a refuter and one worker per workstream. This folder holds the prompts and the program that fills them in. The prompts are public on purpose, so the instructions given to the assistant can be read ([docs/ai-use.md](../docs/ai-use.md)).

## What to know before running it

- **Usage.** A cloud session counts toward the plan's usage limits, and so does a scheduled task. API credits are a separate pool that a cloud session does not draw on, so work that should spend them runs in a local session ([local-prompt.md](local-prompt.md)). An earlier fleet of six hourly routines took the weekly limit past 80 percent overnight, so start small and watch the usage.
- **The sandbox.** It has no SSH and no raw TCP, and outbound port 22 is blocked. A session may not have `/dev/kvm`, in which case QEMU runs in software and boots are slow. Check first.
- **The classifier.** It refuses to let a session write a key or an SSH configuration, and refuses instructions that arrive through an issue or a comment. Give instructions only through the routine prompts.
- **Identity.** Commits and pull requests a scheduled task makes carry the account owner's GitHub user.
- **Private by construction.** Everything unfixed lives in a private repository. No routine writes to the public kernel repository or to this one.

## Setup, once

1. Create a private repository for the audit, for example `eKisNonos/auditing-private`.
2. Grant Claude's GitHub app access to it, in GitHub's settings.
3. Seed it with `brief.md` (the engagement brief), `checklists/`, `claims/`, and empty `findings-private/`, `refutations/` and `notes/` folders. Create an issue titled "Audit status".
4. Resolve the audited commits with `scripts/resolve_targets.py` and keep the full hashes.

## Generate the prompts

```bash
python3 routines/make_prompts.py eKisNonos/auditing-private <40 character commit> prompts/
```

This writes `lead.md`, `refuter.md` and one `wsNN.md` per checklist. Each prompt carries everything its routine needs, because a routine starts each run with no memory. Create one routine per file, pointed at the private repository.

| Routine | Does | Start |
|---|---|---|
| `lead` | merges the notes branches, keeps the status issue, watches for overlap and anything critical | once a day |
| `ws01` to `ws14` | work through a checklist, write candidates and progress notes | two workstreams, once a day |
| `refuter` | tries to break candidates that have no refutation yet, from the claim and the evidence alone | once a day |

Run the lead, the refuter and two workers for two days. Look at the usage and at what the notes contain. Then add workstreams in order of risk while the usage stays inside the limit you set. Do not start all fourteen at once.

Workers write to their own branch and never to `main`. The lead merges. Status goes only into the body of the status issue, because the GitHub comment tool adds a footer to what it posts.

## Stopping

Disable every routine and the work stops. Do it at once if usage runs faster than planned, if a routine writes something it should not, or if something critical appears. The notes stay in the private repository.
