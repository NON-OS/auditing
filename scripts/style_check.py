#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Mechanical writing checks for the Markdown in this repository.

It catches the parts of the style rules a program can catch: forbidden punctuation and a short
list of words that inflate a claim without adding a fact. It does not judge whether a sentence
is good. A person does that in review.

usage: style_check.py [PATH ...]      (default: the whole repository)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_CHARS = {
    "—": "em dash",
    "–": "en dash",
    "…": "ellipsis character",
    "“": "curly double quote",
    "”": "curly double quote",
    "‘": "curly single quote",
    "’": "curly apostrophe",
}

# Words and phrases that tend to claim importance without a fact behind them.
INFLATED = [
    "delve", "pivotal", "tapestry", "testament", "underscore", "underscores", "underscored",
    "showcase", "showcases", "showcasing", "vibrant", "robust", "seamless", "seamlessly",
    "meticulous", "meticulously", "intricate", "intricacies", "multifaceted", "game-changing",
    "revolutionary", "cutting-edge", "state-of-the-art", "groundbreaking", "unparalleled",
    "empower", "empowers", "foster", "fosters", "leverage", "leverages", "leveraging",
    "crucial", "paramount",
]
PHRASES = [
    r"\bnot just\b[^.\n]{0,80}\bbut\b",
    r"\bin conclusion\b",
    r"\bit(?:'s| is) important to note\b",
    r"\bit(?:'s| is) worth noting\b",
    r"\bplays? a (?:crucial|pivotal|key|vital) role\b",
    r"\bstands? as a testament\b",
]

SKIP_DIRS = {".git", "node_modules", "private"}


def strip_code(text):
    """Blank out fenced code and inline code, which may quote forbidden text on purpose."""
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check_text(text, name):
    problems = []
    body = strip_code(text)
    for n, line in enumerate(body.split("\n"), 1):
        for ch, what in FORBIDDEN_CHARS.items():
            if ch in line:
                problems.append(f"{name}:{n}: {what}")
        low = line.lower()
        for w in INFLATED:
            if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
                problems.append(f"{name}:{n}: inflated word '{w}'")
        for pat in PHRASES:
            if re.search(pat, low):
                problems.append(f"{name}:{n}: phrase matching /{pat}/")
    return problems


def files(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            yield p
            continue
        for f in sorted(p.rglob("*.md")):
            if not any(part in SKIP_DIRS for part in f.relative_to(p).parts):
                yield f


def main(argv):
    targets = argv or [str(ROOT)]
    problems = []
    count = 0
    for f in files(targets):
        count += 1
        try:
            rel = f.resolve().relative_to(ROOT)
        except ValueError:
            rel = f
        problems += check_text(f.read_text(encoding="utf-8"), str(rel))
    for p in problems:
        print(p)
    print(f"style: {count} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
