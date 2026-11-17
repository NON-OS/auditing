#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check that cited source locations exist.

Two uses, one rule: a citation must point at a file that exists at the audited commit, and a cited
line number must lie inside that file.

  check_citations.py ours KERNEL_DIR
      Check the citations in this repository's own Markdown. A citation here is written
      `kernel:path/to/file.rs` or `kernel:path/to/file.rs:120` or `kernel:path/to/file.rs:120-140`.
      The rest of the text is not a citation.

  check_citations.py kernel KERNEL_DIR [--json]
      Scan the kernel's own documentation for citations of the form `path/to/file.rs:120` and
      `path/to/file.rs`, and report those that no longer resolve. This is a documentation check, and
      the result is not a vulnerability.

KERNEL_DIR is a checkout of the kernel at the audited commit.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OURS = re.compile(r"`kernel:([A-Za-z0-9_./+-]+)(?::([0-9]+)(?:-([0-9]+))?)?`")
KERNEL_TOP = ("src", "userland", "nonos-", "stark-attest", "tools", "scripts", "verification", "docs",
              "mk", "toolchain", "third_party", "nonos.toml", "Cargo.toml", "Makefile", "flake.nix")
EXT = r"(?:rs|py|toml|lean|sh|mk|S|c|h|nix|md|json|yml|yaml|txt|ld)"
THEIRS = re.compile(r"`((?:" + "|".join(re.escape(t) for t in KERNEL_TOP) + r")[A-Za-z0-9_./+-]*\." + EXT +
                    r")(?::([0-9]+)(?:-([0-9]+))?)?`")
SKIP_DIRS = {".git", "private"}


def line_count(path, cache):
    if path not in cache:
        try:
            with path.open("rb") as fh:
                cache[path] = sum(1 for _ in fh)
        except OSError:
            cache[path] = 0
    return cache[path]


def problems_in(text, kernel, pattern, name, cache):
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        for m in pattern.finditer(line):
            rel, lo, hi = m.group(1), m.group(2), m.group(3)
            target = kernel / rel
            if not target.is_file():
                out.append({"file": name, "line": n, "cite": m.group(0).strip("`"), "why": "no such file"})
                continue
            if lo:
                last = int(hi or lo)
                if int(lo) < 1 or last < int(lo) or last > line_count(target, cache):
                    out.append({"file": name, "line": n, "cite": m.group(0).strip("`"),
                                "why": f"line outside the file ({line_count(target, cache)} lines)"})
    return out


def check_ours(kernel, root=ROOT):
    cache, found, total = {}, [], 0
    for f in sorted(root.rglob("*.md")):
        rel = f.relative_to(root)
        if any(p in SKIP_DIRS for p in rel.parts):
            continue
        text = f.read_text(encoding="utf-8")
        total += len(OURS.findall(text))
        found += problems_in(text, kernel, OURS, str(rel), cache)
    return total, found


def check_kernel_docs(kernel):
    cache, found, total = {}, [], 0
    for f in sorted((kernel / "docs").rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        total += len(THEIRS.findall(text))
        found += problems_in(text, kernel, THEIRS, str(f.relative_to(kernel)), cache)
    return total, found


def main(argv):
    if len(argv) < 2 or argv[0] not in ("ours", "kernel"):
        print(__doc__)
        return 2
    kernel = Path(argv[1]).resolve()
    if not (kernel / "src").is_dir():
        print(f"{kernel} does not look like a kernel checkout", file=sys.stderr)
        return 2
    total, found = check_ours(kernel) if argv[0] == "ours" else check_kernel_docs(kernel)
    if "--json" in argv:
        print(json.dumps({"citations": total, "unresolved": found}, indent=2))
    else:
        for p in found:
            print(f"{p['file']}:{p['line']}: {p['cite']}: {p['why']}")
        print(f"citations: {total} checked, {len(found)} unresolved")
    # Our own citations must all resolve. The kernel's stale citations are reported, not failed on.
    return 1 if (argv[0] == "ours" and found) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
