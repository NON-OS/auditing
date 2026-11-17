#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Publish a confirmed finding, and record what the maintainers decide about it.

usage:
  publish_finding.py DRAFT.json [--commit]                       publish a new finding as open
  publish_finding.py NKA-YYYY-NNN --status fixed --fix-commit HASH --fixed YYYY-MM-DD [--commit]
  publish_finding.py NKA-YYYY-NNN --status accepted-risk --reason "their words" [--commit]
  publish_finding.py NKA-YYYY-NNN --status disputed --reason "their words" [--commit]

A new finding is published the day it is confirmed, with status open and in full. DRAFT.json is the
private finding in the form of findings/schema/finding.schema.json, without the fields this script
sets: status, fix, reason and dates.published. The second form updates a published finding when the
maintainers fix it, accept the risk or dispute it. The script refuses to write a finding unless it:

- passes the schema and the disclosure policy of scripts/validate_findings.py;
- contains nothing the leak guard rejects (identifiers, tokens, keys, real hosts);
- follows the writing rules, with no forbidden punctuation;
- carries the fix commit and fix date when it is fixed, or the maintainers' reason otherwise;
- is a new id when it is published, and an existing one when it is updated.

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
import render_findings as rf  # noqa: E402
import style_check  # noqa: E402
import validate_findings as vf  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CREDIT = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
OWN = {"status", "fix", "reason"}


class Refused(Exception):
    pass


def build(draft, status="open", fix_commit=None, fixed=None, reason=None, today=None, update=False):
    """Return the document to publish, or raise Refused with the reason.

    With update=True the draft is a finding that is already published, and its published date stays.
    """
    today = today or datetime.date.today()
    doc = {k: v for k, v in draft.items() if k not in OWN}
    dates = dict(doc.get("dates", {}))
    if update:
        dates["updated"] = today.isoformat()
    else:
        dates["published"] = today.isoformat()
    doc["status"] = status
    if status == "open":
        dates.pop("fixed", None)
    elif status == "fixed":
        if not fix_commit or not fixed:
            raise Refused("a fixed finding needs --fix-commit and --fixed")
        doc["fix"] = {"commit": fix_commit}
        dates["fixed"] = fixed
    else:
        dates.pop("fixed", None)
        if not (reason and reason.strip()):
            raise Refused(f"a {status} finding needs the maintainers' reason in --reason")
        doc["reason"] = reason.strip()
    doc["dates"] = dates
    errors = vf.validate(doc, json.loads(vf.SCHEMA.read_text()))
    errors += vf.policy(doc, today)
    if errors:
        raise Refused("; ".join(errors))
    text = json.dumps(doc, indent=2, ensure_ascii=False)
    for ch, name in style_check.FORBIDDEN_CHARS.items():
        if ch in text:
            raise Refused(f"the finding contains a {name}, which the writing rules forbid")
    for label, pat in leak_guard.PATTERNS:
        if pat.search(text):
            raise Refused(f"the finding contains a {label}")
    for m in leak_guard.IPV4.finditer(text):
        if leak_guard.public_ip(m.group(0), set()):
            raise Refused(f"the finding contains a public IPv4 address {m.group(0)}")
    return doc


def write(doc, root=ROOT, update=False):
    path = Path(root) / "findings" / "published" / f"{doc['id']}.json"
    if update and not path.exists():
        raise Refused(f"{doc['id']} is not published, so it cannot be updated")
    if not update and path.exists():
        raise Refused(f"{doc['id']} is already published")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rf.render(Path(root))
    return path


def message(doc, update=False):
    verb = "Update" if update else "Publish"
    title = f"{verb} {doc['id']}: {doc['title']}"
    if len(title) > 72:
        title = title[:71].rstrip().rstrip(".")
    lines = [title, "", f"Severity {doc['severity']}, status {doc['status']}."]
    if doc["status"] == "fixed":
        lines.append(f"Fixed in kernel commit {doc['fix']['commit']}.")
    elif doc["status"] == "open":
        lines.append("Published when it was confirmed. The fix is not made yet.")
    else:
        lines.append("The maintainers' reason is recorded in the finding.")
    lines += ["The disclosure rules say when and why a finding is published.", "", CREDIT, ""]
    return "\n".join(lines)


def commit(doc, path, root=ROOT, update=False):
    subprocess.run(["git", "-C", str(root), "add", "-A", str(Path(path).parent)], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-F", "-"], input=message(doc, update), text=True, check=True)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", help="a draft finding in JSON, or the id of a published finding to update")
    ap.add_argument("--status", choices=["open", "fixed", "accepted-risk", "disputed"])
    ap.add_argument("--fix-commit")
    ap.add_argument("--fixed")
    ap.add_argument("--reason")
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args(argv)
    update = a.draft.startswith("NKA-") and not a.draft.endswith(".json")
    try:
        if update:
            if a.status in (None, "open"):
                raise Refused("an update needs --status fixed, accepted-risk or disputed")
            existing = ROOT / "findings" / "published" / f"{a.draft}.json"
            if not existing.exists():
                raise Refused(f"{a.draft} is not published")
            draft = json.loads(existing.read_text(encoding="utf-8"))
            for k in ("fix",):
                draft.pop(k, None)
            doc = build(draft, a.status, a.fix_commit, a.fixed, a.reason, update=True)
            doc["dates"]["published"] = json.loads(existing.read_text(encoding="utf-8"))["dates"]["published"]
        else:
            draft = json.loads(Path(a.draft).read_text(encoding="utf-8"))
            doc = build(draft, a.status or "open", a.fix_commit, a.fixed, a.reason)
        path = write(doc, update=update)
    except (Refused, json.JSONDecodeError, OSError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 1
    print(f"wrote {path.relative_to(ROOT)}")
    if a.commit:
        commit(doc, path, update=update)
        print("committed. Review it, then push.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
