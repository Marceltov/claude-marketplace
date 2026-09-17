---
description: The unwrapped-Markdown convention — paragraphs, list items, table rows and blockquotes are one physical line each, never hard-wrapped at a column. Use when writing or editing Markdown, when a file arrives hard-wrapped and needs unwrapping, or when asked why a Markdown file was reformatted.
---

# Markdown style: no manual line breaks

Every paragraph, list item, table row and blockquote is **one physical line**, however long. The renderer wraps; the source does not.

Manual wrapping makes diffs unreadable. Change one word in a block wrapped at 80 columns and every following line reflows, so `git diff` shows the whole paragraph rewritten instead of the one line you touched. That buys nothing: editors soft-wrap, and GitHub renders both forms identically.

## Writing

Write the whole paragraph on one line and let it run past 80, 120, whatever your editor shows. Do not add a newline to tidy it. Long table cells stay on their row's single line too.

Keep line breaks only where Markdown gives them meaning:

- The blank line between blocks.
- Every line inside a fenced code block, where newlines are content.
- An explicit hard break: two trailing spaces or a trailing backslash. Rare — prefer a new paragraph unless you specifically need a `<br>`.
- Headings, thematic breaks, HTML blocks, indented code and link reference definitions, which are each their own line by definition.

## Unwrapping an existing file

`hooks/unwrap-markdown.py` rejoins hard-wrapped blocks in place and leaves everything listed above untouched. It is idempotent, so running it on clean files does nothing.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/unwrap-markdown.py" README.md
```

It prints the path of each file it changed and stays silent otherwise, so empty output means the files were already clean. To check a whole repository:

```bash
git ls-files '*.md' | xargs python3 "${CLAUDE_PLUGIN_ROOT}/hooks/unwrap-markdown.py"
```

## How the plugin enforces this

Two layers, because either alone is incomplete:

| Layer | Hook | What it covers |
| --- | --- | --- |
| Instruction | `SessionStart` injects the convention as standing context | Prose is written unwrapped in the first place, with no skill invocation needed |
| Correction | `PostToolUse` on `Write\|Edit` runs the unwrapper | Guarantees the result, and catches Markdown that arrived already wrapped |

When the correction hook reports that it reformatted a file, re-read that file before editing it again — its line numbers have shifted.

## When this is the wrong convention

Some projects deliberately wrap Markdown at a fixed column and enforce it in CI. In such a repository this plugin fights the house style and will produce large reformatting diffs. Disable it per-project in that repo's `.claude/settings.local.json`:

```json
{ "enabledPlugins": { "markdown-style@marceltov": false } }
```
