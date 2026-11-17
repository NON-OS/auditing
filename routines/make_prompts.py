#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fill the cloud prompt templates for one engagement.

usage: make_prompts.py OWNER/PRIVATE_REPO KERNEL_COMMIT OUT_DIR

Writes OUT_DIR/lead.md, OUT_DIR/refuter.md and one OUT_DIR/wsNN.md per workstream checklist. Each
file is the full text of one cloud routine's prompt. A routine starts with no memory, so each prompt
has to carry everything it needs.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKLISTS = HERE.parent / "checklists"
KERNEL_URL = "https://github.com/NON-OS/microkernel.git"


def fill(template, values):
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        raise ValueError(f"unfilled placeholders: {sorted(set(left))}")
    return out


def title_of(path):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    return re.sub(r"^#\s*WS\d+\.\s*", "", first)


def build(private_repo, kernel_ref, out_dir, checklists=CHECKLISTS):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", private_repo):
        raise ValueError("the private repository must look like owner/name")
    if not re.fullmatch(r"[0-9a-f]{40}", kernel_ref):
        raise ValueError("the kernel commit must be a full 40 character hash")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    base = {"PRIVATE_REPO": private_repo, "KERNEL_REF": kernel_ref, "KERNEL_URL": KERNEL_URL}
    written = []
    for name in ("lead", "refuter"):
        text = fill((HERE / f"{name}-prompt.md").read_text(encoding="utf-8"), base)
        (out / f"{name}.md").write_text(text, encoding="utf-8")
        written.append(f"{name}.md")
    worker = (HERE / "worker-prompt.md").read_text(encoding="utf-8")
    for cl in sorted(checklists.glob("ws[0-9][0-9]-*.md")):
        ws = cl.name[:4]
        values = dict(base, WS=ws, WS_TITLE=title_of(cl), CHECKLIST=cl.name)
        (out / f"{ws}.md").write_text(fill(worker, values), encoding="utf-8")
        written.append(f"{ws}.md")
    return written


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        written = build(argv[0], argv[1], argv[2])
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    print(f"wrote {len(written)} prompts to {argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
