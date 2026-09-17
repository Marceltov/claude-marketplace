#!/usr/bin/env python3
"""Stop hook: nudge when there is unshipped work, never act on its own.

Runs after Claude finishes a turn. Checks for uncommitted changes or a
branch that is ahead of the default branch with no open PR, and if so prints
a systemMessage — a warning shown to the user in the terminal that does not
enter Claude's context and does not block the turn from ending.

Deliberately not hookSpecificOutput.additionalContext: on the Stop event
that field forces another turn (subject to the same loop protection as
decision: "block"), so using it here would turn a passive reminder into an
unrequested continuation. See docs/adr/0001 in this repo.
"""

import json
import subprocess
import sys


def run(*args):
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def default_branch():
    ref = run("git", "symbolic-ref", "refs/remotes/origin/HEAD")
    if ref:
        return ref.rsplit("/", 1)[-1]
    for candidate in ("main", "master"):
        if run("git", "rev-parse", "--verify", "--quiet", candidate) is not None:
            return candidate
    return "main"


def open_pr_exists():
    state = run("gh", "pr", "view", "--json", "state", "-q", ".state")
    return state == "OPEN"


def main():
    try:
        json.load(sys.stdin)
    except (ValueError, OSError):
        pass  # payload isn't needed beyond confirming this is a Stop event

    if run("git", "rev-parse", "--is-inside-work-tree") != "true":
        return

    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD")
    if not branch or branch == "HEAD":
        return  # detached HEAD, nothing to nudge about

    dirty = bool(run("git", "status", "--porcelain"))
    base = default_branch()
    ahead = None
    if branch != base:
        ahead = run("git", "rev-list", f"{base}..HEAD", "--count")

    has_unshipped_commits = bool(ahead) and ahead != "0"

    if not dirty and not has_unshipped_commits:
        return
    if has_unshipped_commits and not dirty and open_pr_exists():
        return  # already in flight; the ship-pr skill's confirm gate covers the rest

    if dirty:
        message = f"Uncommitted changes on `{branch}`. Ship it? (ship-pr skill)"
    else:
        message = (
            f"`{branch}` is {ahead} commit(s) ahead of `{base}` with no open PR. "
            "Ship it? (ship-pr skill)"
        )
    print(json.dumps({"systemMessage": message}))


if __name__ == "__main__":
    main()
