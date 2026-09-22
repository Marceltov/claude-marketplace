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

`scripts/unwrap-markdown.py` rejoins hard-wrapped blocks in place and leaves everything listed above untouched. It is idempotent, so running it on clean files does nothing.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/unwrap-markdown.py" README.md
```

It prints the path of each file it changed and stays silent otherwise, so empty output means the files were already clean. To check a whole repository:

```bash
git ls-files '*.md' | xargs python3 "${CLAUDE_PLUGIN_ROOT}/scripts/unwrap-markdown.py"
```

## When this is the wrong convention

Some projects deliberately wrap Markdown at a fixed column and enforce it in CI. There this convention fights the house style, and running the unwrapper would produce a large reformatting diff — follow the repo instead.
