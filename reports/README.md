# Reports

Each published report lives in its own directory, `reports/<id>/`, for example
`reports/2026-q4-v1/`, and contains:

| File | What it is |
|---|---|
| `REPORT.md` | The report |
| `targets.lock.json` | The commit hashes the work was done against, from `scripts/resolve_targets.py` |
| `baseline.md` | The measurements from `scripts/metrics.py` |
| `SHA256SUMS` | The hash of every file in the directory |

A report is published only after every finding in it has been fixed, accepted as a risk or disputed. See [docs/disclosure.md](../docs/disclosure.md).
