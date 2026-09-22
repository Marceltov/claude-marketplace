#!/usr/bin/env python3
"""Unwrap hard-wrapped prose in a Markdown file so each paragraph is one line.

Markdown renderers do the wrapping, so a manual line break inside a paragraph
only makes diffs noisy: reflowing one sentence rewrites the whole block. This
joins every paragraph, list item, table row, and blockquote back into a single
line.

Left untouched: fenced code, YAML front matter, standalone indented code,
headings, thematic breaks, HTML blocks, link reference definitions, and blank
lines. A line ending in an explicit hard break (two spaces or a backslash)
keeps it, and the next line stays separate.

Usage: unwrap-markdown.py FILE...
Rewrites in place and prints each path it changed; silent when already unwrapped.
"""

import re
import sys

FENCE = re.compile(r"^\s{0,3}(```+|~~~+)")
HEADING = re.compile(r"^\s{0,3}#{1,6}(\s|$)")
BULLET = re.compile(r"^\s*([-*+]|\d{1,9}[.)])\s")
BLOCKQUOTE = re.compile(r"^\s{0,3}>")
TABLE = re.compile(r"^\s*\|")
HTML = re.compile(r"^\s{0,3}<")
RULE = re.compile(r"^\s{0,3}([-*_])\s*(\1\s*){2,}$")
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s")
INDENTED_CODE = re.compile(r"^(\s{4,}|\t)")
HARD_BREAK = re.compile(r"(\s\s|\\)$")


def unwrap(text):
    lines = text.split("\n")
    out = []
    buf = None          # block being accumulated, or None
    buf_quoted = False  # buf started as a blockquote
    fence = None        # open fence marker, or None
    front_matter = False

    def flush():
        nonlocal buf
        if buf is not None:
            # Keep a trailing hard break; drop incidental trailing whitespace.
            out.append(buf if HARD_BREAK.search(buf) else buf.rstrip())
            buf = None

    for i, line in enumerate(lines):
        if front_matter:
            out.append(line)
            if line.strip() == "---":
                front_matter = False
            continue
        if i == 0 and line.strip() == "---":
            front_matter = True
            out.append(line)
            continue

        if fence is not None:
            out.append(line)
            if line.strip().startswith(fence):
                fence = None
            continue

        m = FENCE.match(line)
        if m:
            flush()
            out.append(line)
            fence = m.group(1)[:3]
            continue

        # Blocks emitted verbatim, never joined and never joined onto. An
        # indented line only counts as code when it does not continue a list
        # item or paragraph already in progress.
        if (not line.strip() or HTML.match(line) or RULE.match(line)
                or HEADING.match(line) or REFDEF.match(line)
                or (buf is None and INDENTED_CODE.match(line))):
            flush()
            out.append(line)
            continue

        quoted = bool(BLOCKQUOTE.match(line))
        # These open a new block but may still absorb continuation lines.
        starts_block = (bool(BULLET.match(line)) or bool(TABLE.match(line))
                        or (quoted and not buf_quoted))

        joinable = (
            buf is not None
            and not starts_block
            and not HARD_BREAK.search(buf)
            and quoted == buf_quoted
        )
        if joinable:
            cont = BLOCKQUOTE.sub("", line, count=1) if quoted else line
            buf = buf.rstrip() + " " + cont.strip()
        else:
            flush()
            buf = line
            buf_quoted = quoted

    flush()
    return "\n".join(out)


def main(paths):
    changed = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                original = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        result = unwrap(original)
        if result != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(result)
            changed.append(path)
    return changed


if __name__ == "__main__":
    for path in main(sys.argv[1:]):
        print(path)
