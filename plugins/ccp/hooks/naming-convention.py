#!/usr/bin/env python3
"""Inject the repo/issue naming convention as standing context for the session.

Runs as a SessionStart hook so the rule applies to every branch, commit, and
PR this session creates -- not just ones made through the ship-pr/
triage-issues skills, and not only when one of those skills happens to get
invoked. Mirrors how the markdown-style plugin injects its formatting rule.
See docs/adr/0006 in this repo for why the convention takes this shape.
"""

import json

INSTRUCTION = """\
Repo/issue naming convention (from the ccp plugin): every branch, commit \
message, and PR title you create in a git repo carries a \
`<REPONAME> #<issue-number>` prefix, so work can be traced back to its repo \
and issue by name alone.

Commit messages and PR titles: `<REPONAME> #<issue-number>: <message>` \
(e.g. `CLAUDE-MARKETPLACE #6: Add propose-skill skill to ccp`). Branches use \
the punctuation-free equivalent, since refs can't hold `#`/`:` cleanly: \
`<reponame-lowercase>-<issue-number>-<slug>` \
(e.g. `claude-marketplace-6-add-propose-skill`).

Resolve the issue number from whatever's already known (the user named one \
directly, or it came from triaging issues) or, failing that, by matching the \
change against the repo's own open issues (`gh issue list` / \
`glab issue list`) -- never by asking the user or using a placeholder id. \
Only when no issue can be confidently matched, fall back to a plain, \
unprefixed name.

This applies whenever you create a branch, commit, or PR yourself, not just \
inside the ship-pr/triage-issues skills -- see those skills for the exact \
commands that resolve the repo name and issue number."""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": INSTRUCTION,
    }
}))
