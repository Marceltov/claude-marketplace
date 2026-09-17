---
description: The Markdown prose convention for this repo — paragraphs, list items and table rows are one line each, never hard-wrapped at a column. Use when writing or editing README.md or any Markdown file here, and to unwrap a file that came in hard-wrapped.
---

# Markdown style: no manual line breaks

Every paragraph, list item, table row and blockquote in this repo is **one physical line**, however long. The renderer wraps; the source does not.

Manual wrapping makes diffs unreadable: changing one word reflows the whole block, so `git diff` shows five rewritten lines instead of one. Editors soft-wrap, and GitHub renders identically either way, so a hard wrap buys nothing.

## Writing

Write the whole paragraph on one line and let it run past 80, 120, whatever. Do not insert a newline to "tidy" it. This applies to table cells too — a long cell stays on its row's single line.

Keep line breaks only where Markdown gives them meaning:

- Between blocks, i.e. the blank line separating paragraphs.
- Inside fenced code blocks, where every newline is content.
- An explicit hard break: two trailing spaces or a trailing backslash. Rare; use a new paragraph instead unless you specifically need a `<br>`.
- Indented code blocks, HTML blocks, headings, thematic breaks and link reference definitions, which are each their own line by definition.

## Unwrapping

`.claude/hooks/unwrap-markdown.py` rejoins hard-wrapped blocks in place and leaves everything above untouched. It is idempotent, so running it on clean files is a no-op.

```bash
python3 .claude/hooks/unwrap-markdown.py README.md
```

A `PostToolUse` hook in `.claude/settings.json` runs it automatically on every `.md` file Claude writes or edits, so a stray wrap gets corrected rather than committed. When the hook reports that it reformatted a file, re-read that file before editing it again — its line numbers have shifted.

To check the whole repo before a commit:

```bash
git ls-files '*.md' | xargs python3 .claude/hooks/unwrap-markdown.py
```

It prints the path of each file it changed and stays silent when everything is already unwrapped, so empty output means the tree is clean.
