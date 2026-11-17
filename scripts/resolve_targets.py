#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resolve the named targets in targets/targets.toml to commit hashes.

The result is printed as JSON. Save it as reports/<id>/targets.lock.json at the start of an
engagement. A tag is resolved to the commit it points at, including through an annotated tag.

usage: resolve_targets.py        (needs Python 3.11 or newer, for tomllib)
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_ls_remote(output, kind, ref):
    """Return the commit hash for `ref` from `git ls-remote` output, peeling annotated tags."""
    wanted = {"tag": f"refs/tags/{ref}", "branch": f"refs/heads/{ref}"}[kind]
    direct, peeled = None, None
    for line in output.splitlines():
        sha, _, name = line.partition("\t")
        if name == wanted:
            direct = sha
        elif name == wanted + "^{}":
            peeled = sha
    return peeled or direct


def resolve(config, run=subprocess.run):
    url = config["repository"]["url"]
    result = {"repository": url, "targets": []}
    for t in config["target"]:
        patterns = [f"refs/tags/{t['ref']}*"] if t["kind"] == "tag" else [f"refs/heads/{t['ref']}"]
        out = run(["git", "ls-remote", url, *patterns], capture_output=True, text=True, check=True).stdout
        sha = parse_ls_remote(out, t["kind"], t["ref"])
        if not sha:
            raise SystemExit(f"could not resolve {t['kind']} {t['ref']}")
        result["targets"].append({"name": t["name"], "kind": t["kind"], "ref": t["ref"], "commit": sha})
    return result


def main():
    import tomllib

    config = tomllib.loads((ROOT / "targets" / "targets.toml").read_text())
    print(json.dumps(resolve(config), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
