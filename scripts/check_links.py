#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check that every relative link in the Markdown files points at a file that exists.

External links are not fetched: CI must not depend on the network, and a dead external link
is a documentation problem, not a correctness one. Anchors are not checked.

usage: check_links.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "private"}


def links(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return LINK.findall(text)


def check(root=ROOT):
    problems = []
    count = 0
    for f in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in f.relative_to(root).parts):
            continue
        for target in links(f.read_text(encoding="utf-8")):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            count += 1
            dest = (f.parent / path).resolve()
            if not dest.exists():
                problems.append(f"{f.relative_to(root)}: broken link {target}")
    return count, problems


def main():
    count, problems = check()
    for p in problems:
        print(p)
    print(f"links: {count} relative links, {len(problems)} broken")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
