#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the claims register.

Checks that every claim has the fields it needs, that ids are unique and in order, and that a
verdict never outruns its evidence:

- an unverified claim lists what must be established;
- any other verdict has evidence, a commit and a review date;
- a verdict short of "verified" suggests a wording the evidence supports;
- "unverifiable" says why;
- an "overstated" or "false" verdict is published only after the wording was corrected, or with
  the maintainers' reason for keeping it.

usage: validate_claims.py
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {"boot-trust", "capsule-isolation", "proofs", "privacy", "network", "ai", "hardware", "build"}
VERDICTS = {"unverified", "verified", "verified-with-caveats", "overstated", "false", "unverifiable"}
HASH = re.compile(r"^[0-9a-f]{40}$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def problems_for(claim, today):
    cid = claim.get("id", "?")
    out = []

    def bad(msg):
        out.append(f"{cid}: {msg}")

    if not re.match(r"^C-[0-9]{3}$", str(claim.get("id", ""))):
        bad("id must look like C-001")
    if claim.get("category") not in CATEGORIES:
        bad("unknown category")
    if not str(claim.get("text", "")).strip():
        bad("missing text")
    src = claim.get("source")
    if not isinstance(src, dict) or src.get("kind") not in {"website", "readme", "doc"} or not src.get("location"):
        bad("source needs a kind and a location")
    elif src["kind"] == "website" and not DATE.match(str(src.get("retrieved", ""))):
        bad("a website source needs the date it was retrieved")
    elif src["kind"] != "website" and not HASH.match(str(src.get("commit", ""))):
        bad("a file source needs the 40 character commit it was read at")
    verdict = claim.get("verdict")
    if verdict not in VERDICTS:
        bad("unknown verdict")
        return out
    if verdict == "unverified":
        if not claim.get("to_establish"):
            bad("an unverified claim must list what is to be established")
        return out
    if not claim.get("evidence"):
        bad("a verdict needs evidence")
    if not HASH.match(str(claim.get("checked_at", ""))):
        bad("a verdict needs checked_at, a 40 character commit")
    if not DATE.match(str(claim.get("reviewed_at", ""))):
        bad("a verdict needs reviewed_at, a date")
    elif datetime.date.fromisoformat(claim["reviewed_at"]) > today:
        bad("reviewed_at is in the future")
    if verdict != "verified" and not str(claim.get("suggested_wording", "")).strip():
        bad("a verdict short of verified needs suggested_wording")
    if verdict == "verified-with-caveats" and not str(claim.get("caveats", "")).strip():
        bad("verified-with-caveats needs caveats")
    if verdict == "unverifiable" and not str(claim.get("reason", "")).strip():
        bad("unverifiable needs a reason")
    if verdict in {"overstated", "false"}:
        if claim.get("corrected_in"):
            if not HASH.match(str(claim["corrected_in"])):
                bad("corrected_in must be a 40 character commit")
        elif not str(claim.get("maintainers_reason", "")).strip():
            bad("an overstated or false verdict needs corrected_in or maintainers_reason")
    return out


def check(root=ROOT, today=None):
    today = today or datetime.date.today()
    path = root / "claims" / "claims.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    claims = data.get("claims", [])
    problems, seen = [], set()
    for i, c in enumerate(claims):
        problems += problems_for(c, today)
        cid = c.get("id")
        if cid in seen:
            problems.append(f"{cid}: duplicate id")
        seen.add(cid)
        if cid != f"C-{i + 1:03d}":
            problems.append(f"{cid}: ids must run C-001, C-002 and so on, in order")
    return len(claims), problems


def main():
    count, problems = check()
    for p in problems:
        print(p)
    print(f"claims: {count} claims, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
