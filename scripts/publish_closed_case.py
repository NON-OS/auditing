#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Publish a closed case: a candidate a second, independent reviewer checked and refuted.

usage: publish_closed_case.py DRAFT.json [--commit]

DRAFT.json is the case in the form of findings/schema/closed-case.schema.json, without the
fields this script sets: dates.closed. The script refuses to write a case unless it:

- passes the schema and the disclosure policy of scripts/validate_closed_cases.py;
- contains nothing the leak guard rejects (identifiers, tokens, keys, real hosts);
- follows the writing rules, with no forbidden punctuation;
- is a new id.

With --commit it makes one commit, through the repository's hooks, and does not push. A person pushes.
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import leak_guard  # noqa: E402
import render_closed_cases as rc  # noqa: E402
import style_check  # noqa: E402
import validate_closed_cases as vc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CREDIT = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"


class Refused(Exception):
    pass


def build(draft, today=None):
    today = today or datetime.date.today()
    doc = dict(draft)
    dates = dict(doc.get("dates", {}))
    dates["closed"] = today.isoformat()
    doc["dates"] = dates
    errors = vc.validate(doc, json.loads(vc.SCHEMA.read_text()))
    errors += vc.policy(doc, today)
    if errors:
        raise Refused("; ".join(errors))
    text = json.dumps(doc, indent=2, ensure_ascii=False)
    for ch, name in style_check.FORBIDDEN_CHARS.items():
        if ch in text:
            raise Refused(f"the case contains a {name}, which the writing rules forbid")
    for label, pat in leak_guard.PATTERNS:
        if pat.search(text):
            raise Refused(f"the case contains a {label}")
    for m in leak_guard.IPV4.finditer(text):
        if leak_guard.public_ip(m.group(0), set()):
            raise Refused(f"the case contains a public IPv4 address {m.group(0)}")
    return doc


def write(doc, root=ROOT):
    path = Path(root) / "findings" / "closed" / f"{doc['id']}.json"
    if path.exists():
        raise Refused(f"{doc['id']} is already published")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rc.render(Path(root))
    return path


def message(doc):
    import textwrap
    subject = f"Close {doc['id']}"
    lines = [subject, ""] + textwrap.wrap(doc["title"], 72) + ["",
             "Checked and refuted by a second, independent reviewer. Not a finding.",
             "The disclosure rules say what gets closed and published here.", "", CREDIT, ""]
    return "\n".join(lines)


def commit(doc, path, root=ROOT):
    subprocess.run(["git", "-C", str(root), "add", "-A", str(Path(path).parent)], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-F", "-"], input=message(doc), text=True, check=True)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", help="a draft closed case in JSON")
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args(argv)
    try:
        draft = json.loads(Path(a.draft).read_text(encoding="utf-8"))
        doc = build(draft)
        path = write(doc)
    except (Refused, json.JSONDecodeError, OSError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 1
    print(f"wrote {path.relative_to(ROOT)}")
    if a.commit:
        commit(doc, path)
        print("committed. Review it, then push.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
