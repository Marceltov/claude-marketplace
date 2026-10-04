# rules

General working rules for every session, in every repo. A SessionStart hook prints [`RULES.md`](RULES.md) into the context at startup, after `/clear`, after compaction and on resume.

The rules are aimed at keeping context small: quiet tool output, narrow reads and searches, no subagents unless asked, short replies. Edit `RULES.md` to change them; keep it short, since it is sent with every session.

A repo's CLAUDE.md takes precedence where the two disagree.
