#!/usr/bin/env bash
# Mechanical half of conflict resolution: figure out the target branch, fetch
# it, and attempt the merge. Deterministic — there's exactly one right way to
# do this part, so it's scripted rather than left to per-request judgment.
# Stops right before the part that actually needs judgment: if the merge
# conflicts, this reports the conflicted files and exits nonzero so the
# resolve-conflicts skill can take over from there.
set -euo pipefail

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree is not clean. Commit or stash your changes before syncing." >&2
  exit 2
fi

default_branch() {
  local ref
  ref=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null || true)
  if [ -n "$ref" ]; then
    echo "${ref##*/}"
    return
  fi
  for candidate in main master; do
    if git rev-parse --verify --quiet "$candidate" >/dev/null; then
      echo "$candidate"
      return
    fi
  done
  echo main
}

pr_base_branch() {
  local base=""
  if command -v gh >/dev/null 2>&1; then
    base=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null || true)
  fi
  if [ -z "$base" ] && command -v glab >/dev/null 2>&1; then
    base=$(glab mr view -F json 2>/dev/null \
      | python3 -c "import json,sys; print(json.load(sys.stdin).get('target_branch',''))" 2>/dev/null || true)
  fi
  echo "$base"
}

target="$(pr_base_branch)"
if [ -z "$target" ]; then
  target="$(default_branch)"
fi

echo "Target branch: $target"
git fetch origin "$target"

if git merge --no-edit "origin/$target"; then
  echo "Merged origin/$target cleanly. No conflicts."
  exit 0
fi

echo
echo "Merge conflicts in:"
git diff --name-only --diff-filter=U
echo
echo "Resolve each file, 'git add' it, then 'git commit --no-edit' to finish the merge."
echo "'git merge --abort' backs out cleanly if this should stop instead."
exit 1
