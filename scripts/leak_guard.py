#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail when the repository contains something that must never be public.

It checks for:

- a file in findings/ that is not a schema, the template, the README or a published finding;
- a tracked private/ directory, or a file that looks like key material by its name;
- private key blocks and common token formats;
- a public IPv4 address, which would identify a real host (reserved, private and documentation
  ranges are allowed, and scripts/ipv4_allow.txt can allow a specific address);
- a home directory path that names a person;
- any term listed in private/banned.txt, a local file that is never committed. Put real hostnames,
  usernames and similar terms there on the machine that runs the audit.

usage: leak_guard.py [ROOT]
"""
import ipaddress
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "private"}
KEY_NAMES = re.compile(r"\.(pem|key|seed|p12|pfx|jks|keystore)$|^\.env(\..*)?$|signing_key", re.I)
ALLOWED_FINDINGS = ("findings/schema/", "findings/published/", "findings/README.md", "findings/TEMPLATE.md")

PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("home path naming a person", re.compile(r"(?:/Users|/home)/(?!runner\b|example\b|user\b|you\b|name\b)[a-z][a-z0-9._-]{1,31}/")),
]
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")


def public_ip(text, allow):
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return False
    if text in allow:
        return False
    if ip.packed[0] == 0:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified or ip in ipaddress.ip_network("192.0.2.0/24")
                or ip in ipaddress.ip_network("198.51.100.0/24") or ip in ipaddress.ip_network("203.0.113.0/24"))


def tracked_files(root):
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=root, capture_output=True, check=True).stdout
        names = [n for n in out.decode().split("\0") if n]
        return [root / n for n in names if (root / n).is_file()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [f for f in root.rglob("*") if f.is_file()
                and not any(p in SKIP_DIRS for p in f.relative_to(root).parts)]


def check(root=ROOT):
    problems = []
    allow = set()
    allow_file = root / "scripts" / "ipv4_allow.txt"
    if allow_file.exists():
        allow = {l.strip() for l in allow_file.read_text().splitlines() if l.strip() and not l.startswith("#")}
    banned = []
    banned_file = root / "private" / "banned.txt"
    if banned_file.exists():
        banned = [l.strip().lower() for l in banned_file.read_text().splitlines()
                  if l.strip() and not l.startswith("#")]
    for f in tracked_files(root):
        rel = f.relative_to(root).as_posix()
        if rel.startswith("private/"):
            problems.append(f"{rel}: private/ must never be tracked")
            continue
        if rel.startswith("findings/") and not rel.startswith(ALLOWED_FINDINGS):
            problems.append(f"{rel}: only published findings may be stored in findings/")
        if KEY_NAMES.search(f.name):
            problems.append(f"{rel}: file name looks like key material")
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pat in PATTERNS:
            if pat.search(text):
                problems.append(f"{rel}: {label}")
        for m in IPV4.finditer(text):
            if public_ip(m.group(0), allow):
                problems.append(f"{rel}: public IPv4 address {m.group(0)}")
        low = text.lower()
        for term in banned:
            if term in low:
                problems.append(f"{rel}: contains a term from private/banned.txt")
    return problems


def main(argv):
    root = Path(argv[0]).resolve() if argv else ROOT
    problems = check(root)
    for p in problems:
        print(p)
    print(f"leak guard: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
