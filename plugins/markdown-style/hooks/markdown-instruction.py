#!/usr/bin/env python3
"""Inject markdown-instruction.md as standing context for the session.

Runs as a SessionStart hook. Unlike a skill, this needs no invocation decision:
the instruction is in context from the first turn, so prose is written unwrapped
rather than unwrapped after the fact by the PostToolUse hook.
"""

import json
from pathlib import Path

instruction = Path(__file__).with_name("markdown-instruction.md").read_text().strip()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": instruction,
    }
}))
