#!/usr/bin/env python3
"""Inject the Markdown prose convention as standing context for the session.

Runs as a SessionStart hook. Unlike a skill, this needs no invocation decision:
the instruction is in context from the first turn, so prose is written unwrapped
rather than unwrapped after the fact by the PostToolUse hook.
"""

import json

INSTRUCTION = """\
Markdown formatting (from the markdown-style plugin):

Write each paragraph, list item, table row and blockquote as ONE physical line, \
however long it gets. Never insert a manual line break to wrap prose at a column \
such as 80 or 100 — Markdown renderers wrap for you, and a hard wrap makes every \
later edit reflow the whole block, turning a one-word change into a multi-line diff.

Keep newlines only where Markdown gives them meaning: the blank line between \
blocks, every line inside a fenced code block, and an explicit hard break (two \
trailing spaces or a trailing backslash).

This applies to every .md file you write or edit, including README files, and to \
long table cells."""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": INSTRUCTION,
    }
}))
