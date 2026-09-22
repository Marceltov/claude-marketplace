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

A `PostToolUse` hook on `Write|Edit` runs the unwrapper on every `.md` and `.markdown` file Claude writes, which guarantees the result whether or not the convention was in context — and catches files that arrived already wrapped, which an instruction never would.

The `markdown-style` skill carries the full convention and is available on demand, for example when you want Claude to write it unwrapped in the first place, unwrap a file by hand, or ask why something was reformatted.

## What it never touches

Fenced code blocks, YAML front matter, standalone indented code, headings, thematic breaks, HTML blocks, link reference definitions, and blank lines. Explicit hard breaks — two trailing spaces or a trailing backslash — are preserved, and the following line stays separate.

The unwrapper is idempotent, so it is a no-op on files that are already clean.

## Standalone use

The formatter is a plain script with no dependencies beyond Python 3, so you can run it outside Claude Code:

```bash
git ls-files '*.md' | xargs python3 hooks/unwrap-markdown.py
```

It prints the path of each file it changed and stays silent otherwise, which makes it usable as a CI check.

## Turning it off for one project

Some repositories deliberately wrap Markdown and enforce it in CI. There, this plugin fights the house style. Disable it in that repository's `.claude/settings.local.json`:

```json
{ "enabledPlugins": { "markdown-style@marceltov": false } }
```

## License

MIT, same as the marketplace.
