# Findings

The finding schema, the template and every published finding. A finding is published the day it is confirmed, with status `open`, and updated when the maintainers decide. See [docs/disclosure.md](../docs/disclosure.md).

| Path | What it is |
|---|---|
| [`schema/finding.schema.json`](schema/finding.schema.json) | The schema every published finding matches |
| [`TEMPLATE.md`](TEMPLATE.md) | The write-up used privately, from candidate to finding |
| `published/NKA-YYYY-NNN.json` | One published finding. The file name is its id |
| `published/NKA-YYYY-NNN.md` | The readable page for it, generated from the JSON |
| [`published/README.md`](published/README.md) | The index, generated from the JSON |

## Rules the checks enforce

- Only the paths above may exist in this directory.
- A published finding matches the schema.
- An `open` finding carries no fix and no reason.
- A `fixed` finding names the fix commit and the date of the fix.
- An `accepted-risk` or `disputed` finding carries the maintainers' reason.
- A `confirmed` finding was reproduced.
- A finding is never dated in the future, and never published before it was reported.
- The pages and the index match the JSON.

`make check` applies them.

Finding ids are assigned when a finding is written. A gap in the published ids is a finding that is held back until it has been reproduced, and it is published with its own id when it is.

## Identifiers

`NKA-<year>-<number>`, for example `NKA-2026-001`. The number is allocated when a candidate becomes a finding and is never reused, including for a finding that is later withdrawn.
