#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Publish one finding that the maintainers have fixed, accepted or disputed.

usage:
  publish_finding.py DRAFT.json --status fixed --fix-commit HASH --fixed YYYY-MM-DD [--commit]
  publish_finding.py DRAFT.json --status accepted-risk --reason "their words" [--commit]
  publish_finding.py DRAFT.json --status disputed --reason "their words" [--commit]

DRAFT.json is the private finding in the form of findings/schema/finding.schema.json, without the
fields this script sets: status, fix, reason and dates.published. It is read from outside the
repository. This script refuses to write the finding unless it:

- passes the schema and the disclosure policy of scripts/validate_findings.py;
- contains nothing the leak guard rejects (identifiers, tokens, keys, hosts);
- carries the fix commit and fix date when the status is fixed, or the maintainers' reason otherwise;
- has an id that is not already published.

With --commit it makes one commit for the finding, through the repository's hooks, and does not push.
A person pushes. Nothing here publishes a finding that is still open.
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import leak_guard  # noqa: E402
import validate_findings as vf  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CREDIT = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
OWN = {"status", "fix", "reason"}


class Refused(Exception):
    pass


def build(draft, status, fix_commit=None, fixed=None, reason=None, today=None):
    """Return the document to publish, or raise Refused with the reason."""
    today = today or datetime.date.today()
    doc = {k: v for k, v in draft.items() if k not in OWN}
    dates = dict(doc.get("dates", {}))
    dates["published"] = today.isoformat()
    doc["status"] = status
    if status == "fixed":
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
    for label, pat in leak_guard.PATTERNS:
        if pat.search(text):
            raise Refused(f"the finding contains a {label}")
    for m in leak_guard.IPV4.finditer(text):
        if leak_guard.public_ip(m.group(0), set()):
            raise Refused(f"the finding contains a public IPv4 address {m.group(0)}")
    return doc


def write(doc, root=ROOT):
    path = Path(root) / "findings" / "published" / f"{doc['id']}.json"
    if path.exists():
        raise Refused(f"{doc['id']} is already published")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def message(doc):
    title = f"Publish {doc['id']}: {doc['title']}"
    if len(title) > 72:
        title = title[:71].rstrip() + "."
        title = title.rstrip(".")
    lines = [title, "", f"Severity {doc['severity']}, status {doc['status']}."]
    if doc["status"] == "fixed":
        lines.append(f"Fixed in kernel commit {doc['fix']['commit']}.")
    else:
        lines.append("The maintainers' reason is recorded in the finding.")
    lines += ["The finding is published after the maintainers' decision, as the disclosure", "rules require.", "", CREDIT, ""]
    return "\n".join(lines)


def commit(doc, path, root=ROOT):
    subprocess.run(["git", "-C", str(root), "add", str(path)], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-F", "-"], input=message(doc), text=True, check=True)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--status", required=True, choices=["fixed", "accepted-risk", "disputed"])
    ap.add_argument("--fix-commit")
    ap.add_argument("--fixed")
    ap.add_argument("--reason")
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args(argv)
    try:
        draft = json.loads(Path(a.draft).read_text(encoding="utf-8"))
        doc = build(draft, a.status, a.fix_commit, a.fixed, a.reason)
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
