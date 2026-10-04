<EXTREMELY_IMPORTANT>
# General rules

These apply in every repo. Where a repo's CLAUDE.md says otherwise, it wins.

- Keep tool output small: quiet flags (`pytest -q`, `vitest --reporter=dot`), long output through `tail -n 40` or a targeted `grep`. While iterating, run only the tests that cover the change; run the full suite once before shipping.
- Read files by range when you know where to look. Don't re-read a file you've read or just edited.
- Search from the most likely path outward; don't sweep unrelated directories.
- No subagents unless asked. For search-only agents pass `model: haiku`.
- Skip brainstorming for small, clearly specified changes.
- Keep CLAUDE.md small: commands and non-obvious rules only. Put task-specific detail (recipes, style guides, background) in a project skill under `.claude/skills/<name>/SKILL.md` and leave a one-line pointer. When a CLAUDE.md you work in has grown such sections, offer to split them out.
- When a task is done (shipped, merged, or answered) and the next request is unrelated, tell me to `/clear` first.
- Replies: what changed and what's left. No preamble, no recap of the diff.
</EXTREMELY_IMPORTANT>
