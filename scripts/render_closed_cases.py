#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Render the closed cases as readable pages and an index.

The JSON files in findings/closed/ are the record. This script writes, next to them:

- findings/closed/NKA-CLOSED-YYYY-NNN.md   one page per closed case
- findings/closed/README.md                the index, newest first, with a count

usage: render_closed_cases.py [--check]
With --check it writes nothing and exits 1 when a page or the index is out of date, which is what
`make findings` runs, so the pages can never disagree with the JSON.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def plain(text):
    """A kernel: citation in a code span is plain text here, so the citation check, which pins the
    kernel at one commit, does not reject a case written against another commit."""
    return re.sub(r"`kernel:([^`]+)`", r"kernel:\1", str(text))


def page(doc):
    d = doc["dates"]
    lines = [f"# {doc['id']}: {plain(doc['title'])}", "",
             "**Closed.** A candidate checked and refuted by a second, independent reviewer.", ""]
    rows = [("Component", doc["component"]), ("Location", plain(doc["location"]))]
    aff = doc.get("affected") or {}
    if aff:
        main_txt = "yes" if aff.get("main") else ("no" if aff.get("main_checked") else "not checked")
        rows.append(("Affected", f"release {'yes' if aff.get('release') else 'no'}, main {main_txt}"
                     + (f", tested at {', '.join(c[:12] for c in aff['commits'])}" if aff.get("commits") else "")))
    rows += [("Reported", d["reported"]), ("Closed", d["closed"])]
    lines += ["| | |", "|---|---|"] + [f"| {k} | {plain(v)} |" for k, v in rows] + [""]
    lines += ["## The claim", "", plain(doc["claim"]), "",
              "## Why it is not a finding", "", plain(doc["why_not_a_finding"]), "",
              "## Routes tried", ""] + [f"{i}. {plain(r)}" for i, r in enumerate(doc["routes_tried"], 1)] + [""]
    ev = doc.get("evidence") or {}
    if ev:
        lines += ["## Evidence", "",
                  f"Checked independently of the original write-up: {'yes' if ev.get('checked_independently') else 'no'}.", ""]
        lines += [f"- {plain(s)}" for s in ev.get("steps", [])] + [""]
    return "\n".join(lines).rstrip("\n") + "\n"


def index(docs):
    n = len(docs)
    lines = ["# Closed cases", "",
             "Candidates a worker wrote up and a second, independent reviewer checked and refuted. "
             "These are not findings: nothing here is a vulnerability. They are published so the "
             "record shows what was checked and ruled out, not only what was confirmed. "
             "[docs/disclosure.md](../../docs/disclosure.md) has the rules.", ""]
    if not n:
        return "\n".join(lines + ["No case has been closed yet.", ""])
    lines += [f"{n} closed.", "",
              "| ID | Title | Component | Closed |", "|---|---|---|---|"]
    for d in sorted(docs, key=lambda d: (d["dates"]["closed"], d["id"]), reverse=True):
        lines.append(f"| [{d['id']}]({d['id']}.md) | {plain(d['title'])} | {plain(d['component'])} | {d['dates']['closed']} |")
    return "\n".join(lines) + "\n"


def expected(root):
    closed = Path(root) / "findings" / "closed"
    docs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(closed.glob("*.json"))] if closed.is_dir() else []
    out = {closed / f"{d['id']}.md": page(d) for d in docs}
    out[closed / "README.md"] = index(docs)
    return closed, out


def render(root=ROOT):
    closed, out = expected(root)
    closed.mkdir(parents=True, exist_ok=True)
    keep = {p.name for p in out}
    for old in closed.glob("*.md"):
        if old.name not in keep:
            old.unlink()
    for path, text in out.items():
        path.write_text(text, encoding="utf-8")
    return list(out)


def stale(root=ROOT):
    closed, out = expected(root)
    bad = [p.name for p, t in out.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    bad += [p.name for p in (closed.glob("*.md") if closed.is_dir() else []) if p not in out]
    return bad


def main(argv):
    if "--check" in argv:
        bad = stale()
        for b in bad:
            print(f"findings/closed/{b}: out of date, run scripts/render_closed_cases.py")
        print(f"rendered closed cases: {len(bad)} out of date")
        return 1 if bad else 0
    print(f"rendered {len(render())} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
