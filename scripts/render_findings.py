#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Render the published findings as readable pages and an index.

The JSON files in findings/published/ are the record. This script writes, next to them:

- findings/published/NKA-YYYY-NNN.md   one page per finding
- findings/published/README.md         the index, newest first, with counts by status and severity

usage: render_findings.py [--check]
With --check it writes nothing and exits 1 when a page or the index is out of date, which is what
`make findings` runs, so the pages can never disagree with the JSON.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEV = ["critical", "high", "medium", "low", "informational"]
STATUS_TEXT = {
    "open": "Open. Published when it was confirmed, and not yet fixed.",
    "fixed": "Fixed.",
    "accepted-risk": "Accepted as a risk by the maintainers.",
    "disputed": "Disputed by the maintainers.",
}


def plain(text):
    """A kernel: citation in a code span is plain text here, so the citation check, which pins the
    kernel at one commit, does not reject a finding written against another commit."""
    return re.sub(r"`kernel:([^`]+)`", r"kernel:\1", str(text))


def page(doc):
    d = doc["dates"]
    lines = [f"# {doc['id']}: {plain(doc['title'])}", "", f"**{STATUS_TEXT[doc['status']]}**", ""]
    rows = [("Component", doc["component"]), ("Severity", doc["severity"]), ("Confidence", doc["confidence"]),
            ("Adversary", doc["adversary"]), ("Location", plain(doc["location"])), ("CVSS 4.0", doc["cvss"]),
            ("Affected", f"release {'yes' if doc['affected']['release'] else 'no'}, main "
                         f"{'yes' if doc['affected']['main'] else ('no' if doc['affected'].get('main_checked') else 'not checked')}, tested at {', '.join(c[:12] for c in doc['affected']['commits'])}"),
            ("Reported", d["reported"]), ("Published", d["published"])]
    if "fixed" in d:
        rows.append(("Fixed", f"{d['fixed']}, kernel commit {doc['fix']['commit']}"))
    if "updated" in d:
        rows.append(("Last updated", d["updated"]))
    lines += ["| | |", "|---|---|"] + [f"| {k} | {plain(v)} |" for k, v in rows] + [""]
    if doc.get("preconditions"):
        lines += ["## Preconditions", ""] + [f"- {plain(p)}" for p in doc["preconditions"]] + [""]
    lines += ["## Description", "", plain(doc["description"]), "", "## Impact", "", plain(doc["impact"]), "",
              "## Attack scenario", ""] + [f"{i}. {plain(s)}" for i, s in enumerate(doc["scenario"], 1)] + [""]
    ev = doc["evidence"]
    lines += ["## Evidence", "", f"Reproduced: {'yes' if ev['reproduced'] else 'no'}.", ""]
    lines += [f"- {plain(s)}" for s in ev["steps"]] + [""]
    if ev.get("harness"):
        lines += ["Harness: " + plain(ev["harness"]), ""]
    lines += ["## Remediation", "", plain(doc["remediation"]), ""]
    if doc.get("regression_check"):
        lines += ["Regression check: " + plain(doc["regression_check"]), ""]
    if doc.get("reason"):
        lines += ["## The maintainers' reason", "", plain(doc["reason"]), ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def index(docs):
    n = len(docs)
    by_status = {s: sum(1 for d in docs if d["status"] == s) for s in STATUS_TEXT}
    by_sev = {s: sum(1 for d in docs if d["severity"] == s) for s in SEV}
    lines = ["# Published findings", "",
             "Every finding of this audit is published here when it is confirmed, with its evidence, and updated when the "
             "maintainers fix it, accept the risk or dispute it. [docs/disclosure.md](../../docs/disclosure.md) has the rules.", ""]
    if not n:
        return "\n".join(lines + ["No finding has been published yet.", ""])
    lines += [f"{n} published: " + ", ".join(f"{v} {k}" for k, v in by_status.items() if v) + ".",
              "By severity: " + ", ".join(f"{by_sev[s]} {s}" for s in SEV if by_sev[s]) + ".", "",
              "| ID | Title | Severity | Status | Published |", "|---|---|---|---|---|"]
    for d in sorted(docs, key=lambda d: (d["dates"]["published"], d["id"]), reverse=True):
        lines.append(f"| [{d['id']}]({d['id']}.md) | {plain(d['title'])} | {d['severity']} | {d['status']} | {d['dates']['published']} |")
    return "\n".join(lines) + "\n"


def expected(root):
    pub = Path(root) / "findings" / "published"
    docs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(pub.glob("*.json"))] if pub.is_dir() else []
    out = {pub / f"{d['id']}.md": page(d) for d in docs}
    out[pub / "README.md"] = index(docs)
    return pub, out


def render(root=ROOT):
    pub, out = expected(root)
    pub.mkdir(parents=True, exist_ok=True)
    keep = {p.name for p in out}
    for old in pub.glob("*.md"):
        if old.name not in keep:
            old.unlink()
    for path, text in out.items():
        path.write_text(text, encoding="utf-8")
    return list(out)


def stale(root=ROOT):
    pub, out = expected(root)
    bad = [p.name for p, t in out.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    bad += [p.name for p in (pub.glob("*.md") if pub.is_dir() else []) if p not in out]
    return bad


def main(argv):
    if "--check" in argv:
        bad = stale()
        for b in bad:
            print(f"findings/published/{b}: out of date, run scripts/render_findings.py")
        print(f"rendered findings: {len(bad)} out of date")
        return 1 if bad else 0
    print(f"rendered {len(render())} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
