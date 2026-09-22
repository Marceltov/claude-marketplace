# markdown-style

Keeps Markdown prose unwrapped: one physical line per paragraph, list item, table row and blockquote, so a one-word edit never reflows a whole block.

## Why

Hard-wrapping Markdown at 80 or 100 columns makes diffs unreadable. Change one word and every following line in the block reflows, so the diff shows a rewritten paragraph instead of the one line you touched. Renderers wrap for you and editors soft-wrap, so the hard wrap buys nothing and costs review clarity.

## Install

```bash
/plugin marketplace add Marceltov/claude-marketplace
/plugin install markdown-style@marceltov
```

## What it does

The `markdown-style` skill carries the convention and loads on demand — when Claude writes Markdown, when a file arrives hard-wrapped and needs unwrapping, or when you ask why something was reformatted. `scripts/unwrap-markdown.py` does the actual rewriting.

Nothing runs automatically. An earlier version enforced this with a `PostToolUse` hook on every Markdown write; it was removed, so the convention now applies when the skill is in play rather than on every file unconditionally.

## What it never touches

Fenced code blocks, YAML front matter, standalone indented code, headings, thematic breaks, HTML blocks, link reference definitions, and blank lines. Explicit hard breaks — two trailing spaces or a trailing backslash — are preserved, and the following line stays separate.

The unwrapper is idempotent, so it is a no-op on files that are already clean.

## Standalone use

The formatter is a plain script with no dependencies beyond Python 3, so you can run it outside Claude Code:

```bash
git ls-files '*.md' | xargs python3 scripts/unwrap-markdown.py
```

It prints the path of each file it changed and stays silent otherwise, which makes it usable as a CI check.

## When this is the wrong convention

Some repositories deliberately wrap Markdown and enforce it in CI. There, this convention fights the house style — follow the repo instead, and don't run the unwrapper over it.

## License

MIT, same as the marketplace.
