# AI assistance

Parts of this audit are done by Claude, an AI model made by Anthropic. This page says what it does, what it never decides, where it runs and what it costs, so that a reader can weigh the work.

## What the assistant does

- Reads source and proposes where to look, and why.
- Writes test harnesses, fuzz targets and reproduction code.
- Runs builds, tools and tests, and reports what they print.
- Drafts documents, which a person edits.
- Proposes candidate findings with its reasoning.

## What it never decides

- Whether something is a finding. A candidate becomes a finding by reproduction or a complete chain, and only after a second reviewer fails to refute it ([method.md](method.md)).
- A severity. A person sets it against [severity.md](severity.md).
- What is published, and when.
- Anything involving a key, a secret, a production system or a real account. The assistant has access to none of them.

## How its output is checked

- Code it writes is run, and a person reviews each harness before it is trusted.
- Every statement in a report is labelled confirmed, supported or hypothesis. The assistant's reasoning alone is never enough for confirmed.
- Every code reference is a citation that `scripts/check_citations.py` resolves against the audited commit, which catches the assistant naming a file or line that does not exist.
- The refutation step is a separate run that sees only the claim, the commit and the evidence, so it cannot be anchored by the first run's reasoning.
- Each report states how many candidates were dropped.

## Where it runs and who pays

NØNOS is a member of Anthropic's Claude Startups program. The audit uses Claude in two ways:

- Local sessions on the auditor's machine, billed through the Claude API against the program's API credits.
- Scheduled cloud routines, which count against the usage limits of NØNOS's Claude Team plan. The prompts they run are in [`routines/`](../routines/README.md), so the instructions given to the assistant are public.

Anthropic has no say in what the audit examines, finds or publishes, and has not reviewed or endorsed it. A provider that also funds part of the work is a relationship a reader should know about, so it is stated here.

## Known limits

- It can state something false with confidence, including a file, a line or a function that does not exist. That is the reason for the citation check.
- It leans toward the likely answer and can miss an unusual bug that a person with a specific idea would find.
- It can be wrong about what code does at run time. A claim without a reproduction stays "supported".
- A routine starts each run with no memory. Continuity lives in the private notes, so a gap in the notes is a gap in the work.

## Credit

A commit that contains material the assistant wrote or edited ends with this trailer:

```text
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
```

Responsibility for every claim in a published report belongs to the people named in it.
