# Findings

The finding schema, the template and, once the maintainers have responded, the published findings. This directory never holds a finding that is still open. See [docs/disclosure.md](../docs/disclosure.md).

| Path | What it is |
|---|---|
| [`schema/finding.schema.json`](schema/finding.schema.json) | The schema every published finding matches |
| [`TEMPLATE.md`](TEMPLATE.md) | The write-up used privately, from candidate to finding |
| `published/NKA-YYYY-NNN.json` | One published finding. The file name is its id |

## Rules the checks enforce

- Only the paths above may exist in this directory.
- A published finding matches the schema.
- A `fixed` finding names the fix commit and the date of the fix.
- An `accepted-risk` or `disputed` finding carries the maintainers' reason.
- A `confirmed` finding was reproduced.
- A finding is never dated in the future, and never published before it was reported.

`make check` applies them.

## Identifiers

`NKA-<year>-<number>`, for example `NKA-2026-001`. The number is allocated when a candidate becomes a finding and is never reused, including for a finding that is later withdrawn.
