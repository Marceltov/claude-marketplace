#!/usr/bin/env python3
"""Inject naming-convention.md as standing context for the session.

Runs as a SessionStart hook so the rule applies to every branch, commit, and
PR this session creates -- not just ones made through the ship-pr/
triage-issues skills, and not only when one of those skills happens to get
invoked. Mirrors how the markdown-style plugin injects its formatting rule.
See docs/adr/0006 in this repo for why the convention takes this shape.
"""

import json
from pathlib import Path

instruction = Path(__file__).with_name("naming-convention.md").read_text().strip()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": instruction,
    }
}))
