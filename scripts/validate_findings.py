#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the published findings, and enforce the disclosure policy.

Only published findings may live in this repository, in findings/published/. A finding is published
when it is confirmed, with status open, and updated when the maintainers decide. Each one must:

- match findings/schema/finding.schema.json;
- be named after its id;
- have a status that matches its evidence: an "open" finding carries neither a fix nor a reason, a
  "fixed" finding carries a fix commit and a fix date, and an "accepted-risk" or "disputed"
  finding carries the maintainers' reason;
- be published on or after the day it was reported, and never in the future.

The validator reads the schema and checks the subset of JSON Schema that the schema uses, so
it needs nothing beyond the Python standard library.

usage: validate_findings.py
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "findings" / "schema" / "finding.schema.json"
PUBLISHED = ROOT / "findings" / "published"


def validate(value, schema, where="$"):
    errors = []
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: {value!r} is not one of {schema['enum']}")
        return errors
    kind = schema.get("type")
    checks = {"object": dict, "array": list, "string": str, "boolean": bool}
    if kind in checks and not isinstance(value, checks[kind]):
        errors.append(f"{where}: expected {kind}")
        return errors
    if kind == "string":
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: does not match {schema['pattern']}")
    if kind == "array":
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{where}: fewer than {schema['minItems']} items")
        for i, item in enumerate(value):
            errors += validate(item, schema.get("items", {}), f"{where}[{i}]")
    if kind == "object":
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}: missing '{key}'")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors += validate(value[key], sub, f"{where}.{key}")
    return errors


def policy(doc, today):
    errors = []
    dates = doc.get("dates", {})
    try:
        reported = datetime.date.fromisoformat(dates["reported"])
        published = datetime.date.fromisoformat(dates["published"])
    except (KeyError, ValueError):
        return ["dates: reported and published must be valid dates"]
    if published > today:
        errors.append("dates.published is in the future")
    if published < reported:
        errors.append("dates.published is before dates.reported")
    status = doc.get("status")
    if status == "open" and ("fix" in doc or "fixed" in dates or "reason" in doc):
        errors.append("an open finding carries no fix and no reason")
    if status == "fixed":
        if "fix" not in doc or "fixed" not in dates:
            errors.append("a fixed finding needs 'fix' and 'dates.fixed'")
    if status in ("accepted-risk", "disputed") and not str(doc.get("reason", "")).strip():
        errors.append(f"a {status} finding needs the maintainers' reason")
    if doc.get("confidence") == "confirmed" and not doc.get("evidence", {}).get("reproduced"):
        errors.append("confidence is 'confirmed' but evidence.reproduced is false")
    return errors


def check(root=ROOT, today=None):
    today = today or datetime.date.today()
    schema = json.loads((root / "findings" / "schema" / "finding.schema.json").read_text())
    problems, count = [], 0
    pub = root / "findings" / "published"
    for f in sorted(pub.glob("*.json")) if pub.is_dir() else []:
        count += 1
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: invalid JSON: {e}")
            continue
        errs = validate(doc, schema)
        if not errs:
            if doc["id"] + ".json" != f.name:
                errs.append(f"file name must be {doc['id']}.json")
            errs += policy(doc, today)
        problems += [f"{f.name}: {e}" for e in errs]
    return count, problems


def main():
    count, problems = check()
    for p in problems:
        print(p)
    print(f"findings: {count} published, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
