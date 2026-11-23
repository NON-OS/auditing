#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the closed cases, and enforce the disclosure policy for them.

Only closed cases may live in this repository, in findings/closed/. A case is closed when a worker's
candidate was checked and refuted by a second, independent reviewer. Each one must:

- match findings/schema/closed-case.schema.json;
- be named after its id;
- be closed on or after the day it was reported, and never in the future.

The validator reads the schema and checks the subset of JSON Schema that the schema uses, so
it needs nothing beyond the Python standard library.

usage: validate_closed_cases.py
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "findings" / "schema" / "closed-case.schema.json"
CLOSED = ROOT / "findings" / "closed"


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
        closed = datetime.date.fromisoformat(dates["closed"])
    except (KeyError, ValueError):
        return ["dates: reported and closed must be valid dates"]
    if closed > today:
        errors.append("dates.closed is in the future")
    if closed < reported:
        errors.append("dates.closed is before dates.reported")
    if not doc.get("evidence", {}).get("checked_independently"):
        errors.append("a closed case must be checked independently of the original worker's write-up")
    return errors


def check(root=ROOT, today=None):
    today = today or datetime.date.today()
    schema = json.loads((root / "findings" / "schema" / "closed-case.schema.json").read_text())
    problems, count = [], 0
    closed = root / "findings" / "closed"
    for f in sorted(closed.glob("*.json")) if closed.is_dir() else []:
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
    print(f"closed cases: {count}, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
