#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Baseline measurements of a source tree, for the first phase of an engagement.

It counts, per top-level directory: Rust, C and assembly lines, `unsafe` occurrences, inline
assembly, lint allowances, and Cargo lock entries. The numbers are crude on purpose. They say
where to look first and give a reader something to compare a later run against. They are not
findings.

usage: metrics.py TREE [--json]
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP = {".git", "target", "node_modules", ".cargo", "vendor"}
UNSAFE = re.compile(r"\bunsafe\b")
ASM = re.compile(r"\b(?:global_asm|asm)!")
ALLOW = re.compile(r"#!?\[allow\(")


def code_lines(text):
    n = 0
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("//"):
            n += 1
    return n


def measure(tree):
    tree = Path(tree)
    out = defaultdict(lambda: defaultdict(int))
    locks = 0
    for f in tree.rglob("*"):
        if not f.is_file():
            continue
        parts = f.relative_to(tree).parts
        if any(p in SKIP for p in parts):
            continue
        top = parts[0] if len(parts) > 1 else "."
        if f.name == "Cargo.lock":
            try:
                locks += len(re.findall(r"^\[\[package\]\]", f.read_text(), re.M))
            except OSError:
                pass
            continue
        suffix = f.suffix.lower()
        if suffix not in (".rs", ".c", ".h", ".s"):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        key = {".rs": "rust_lines", ".c": "c_lines", ".h": "c_lines", ".s": "asm_lines"}[suffix]
        out[top][key] += code_lines(text)
        out[top]["files"] += 1
        if suffix == ".rs":
            out[top]["unsafe"] += len(UNSAFE.findall(text))
            out[top]["inline_asm"] += len(ASM.findall(text))
            out[top]["allows"] += len(ALLOW.findall(text))
    return {"directories": {k: dict(v) for k, v in sorted(out.items())}, "cargo_lock_packages": locks}


def as_markdown(result):
    cols = ["files", "rust_lines", "c_lines", "asm_lines", "unsafe", "inline_asm", "allows"]
    lines = ["| directory | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    totals = defaultdict(int)
    for d, vals in result["directories"].items():
        lines.append(f"| {d} | " + " | ".join(str(vals.get(c, 0)) for c in cols) + " |")
        for c in cols:
            totals[c] += vals.get(c, 0)
    lines.append("| total | " + " | ".join(str(totals[c]) for c in cols) + " |")
    lines.append("")
    lines.append(f"Cargo lock packages across all lockfiles: {result['cargo_lock_packages']}")
    return "\n".join(lines)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    result = measure(argv[0])
    print(json.dumps(result, indent=2) if "--json" in argv else as_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
