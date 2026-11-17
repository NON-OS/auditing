#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Build the private workspace for a local audit session.
#
# usage:  scripts/setup_local_workspace.sh [--dry-run]
#
# environment:
#   AUDIT_HOME   where the workspace goes (default ~/audit-private)
#   BRIEF        the engagement brief to copy in (default /Users/Shared/audit-handoff/brief.md)
#   KERNEL_URL   the kernel repository (default https://github.com/NON-OS/microkernel.git)
#   RELEASE_TAG  the release to audit (default v0.9.3.5)
#
# What it makes: the notes folders, the kernel checked out twice and read only for you, once at the
# release and once at main, each at a full commit hash recorded in targets.lock.json, a copy of this
# repository, and the prompt to start the session with. It touches nothing outside AUDIT_HOME, reads no
# key, and sets no remote on the workspace, so nothing in it can be pushed anywhere by accident.

set -euo pipefail

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) sed -n '3,17p' "$0"; exit 0 ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

AUDIT_HOME="${AUDIT_HOME:-$HOME/audit-private}"
BRIEF="${BRIEF:-/Users/Shared/audit-handoff/brief.md}"
KERNEL_URL="${KERNEL_URL:-https://github.com/NON-OS/microkernel.git}"
RELEASE_TAG="${RELEASE_TAG:-v0.9.3.5}"
AUDIT_URL="https://github.com/NON-OS/auditing.git"
HERE="$(cd "$(dirname "$0")" && pwd)"

say() { printf '\n== %s\n' "$*"; }
run() { if [ "$DRY_RUN" = 1 ]; then printf '   would run: %s\n' "$*"; else "$@"; fi; }

say "Resolve the targets to full commit hashes"
release="$(git ls-remote "$KERNEL_URL" "refs/tags/${RELEASE_TAG}^{}" | cut -f1)"
[ -n "$release" ] || release="$(git ls-remote "$KERNEL_URL" "refs/tags/${RELEASE_TAG}" | cut -f1)"
main_ref="$(git ls-remote "$KERNEL_URL" refs/heads/main | cut -f1)"
[[ "$release" =~ ^[0-9a-f]{40}$ ]] || { echo "could not resolve tag $RELEASE_TAG" >&2; exit 1; }
[[ "$main_ref" =~ ^[0-9a-f]{40}$ ]] || { echo "could not resolve main" >&2; exit 1; }
echo "release $RELEASE_TAG = $release"
echo "main = $main_ref"

say "Workspace folders"
run mkdir -p "$AUDIT_HOME"/{notes,findings-private,refutations,logs}
run chmod 700 "$AUDIT_HOME"

say "Targets"
if [ "$DRY_RUN" = 0 ]; then
  printf '{\n  "repository": "%s",\n  "targets": [\n    {"name": "release", "ref": "%s", "commit": "%s"},\n    {"name": "main", "ref": "main", "commit": "%s"}\n  ]\n}\n' \
    "$KERNEL_URL" "$RELEASE_TAG" "$release" "$main_ref" > "$AUDIT_HOME/targets.lock.json"
fi

say "Kernel source, two read-only checkouts"
if [ ! -d "$AUDIT_HOME/kernel-src/.git" ]; then
  run git clone --filter=blob:none --no-checkout "$KERNEL_URL" "$AUDIT_HOME/kernel-src"
fi
run git -C "$AUDIT_HOME/kernel-src" fetch --quiet origin "$release" "$main_ref"
[ -d "$AUDIT_HOME/kernel-release" ] || run git -C "$AUDIT_HOME/kernel-src" worktree add --detach "$AUDIT_HOME/kernel-release" "$release"
[ -d "$AUDIT_HOME/kernel-main" ]    || run git -C "$AUDIT_HOME/kernel-src" worktree add --detach "$AUDIT_HOME/kernel-main" "$main_ref"

say "The audit repository"
[ -d "$AUDIT_HOME/auditing/.git" ] || run git clone "$AUDIT_URL" "$AUDIT_HOME/auditing"

say "The engagement brief"
if [ -f "$BRIEF" ]; then
  run cp "$BRIEF" "$AUDIT_HOME/brief.md"
else
  echo "no brief at $BRIEF. Copy it to $AUDIT_HOME/brief.md before you start." >&2
fi

say "The starting prompt"
if [ "$DRY_RUN" = 0 ]; then
  {
    cat "$HERE/../routines/local-prompt.md"
    cat <<EOF

## Your setup

- Workspace (private, all notes and candidates go here): $AUDIT_HOME
- Engagement brief: $AUDIT_HOME/brief.md
- Audit repository, read only for you: $AUDIT_HOME/auditing
- Kernel at the release $RELEASE_TAG, read only: $AUDIT_HOME/kernel-release, commit $release
- Kernel at main, read only: $AUDIT_HOME/kernel-main, commit $main_ref
- Targets file: $AUDIT_HOME/targets.lock.json

Start with the release. Say which commit every note refers to.
EOF
  } > "$AUDIT_HOME/START-PROMPT.md"
fi

say "Workspace repository, local only"
[ -d "$AUDIT_HOME/.git" ] || run git -C "$AUDIT_HOME" init -q
if [ "$DRY_RUN" = 0 ]; then
  printf 'kernel-src/\nkernel-release/\nkernel-main/\nauditing/\n' > "$AUDIT_HOME/.gitignore"
fi

say "Done"
echo "Workspace: $AUDIT_HOME"
echo "Next: start Claude Code in $AUDIT_HOME with an API key, and give it $AUDIT_HOME/START-PROMPT.md."
