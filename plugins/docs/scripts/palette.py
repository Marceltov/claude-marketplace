#!/usr/bin/env python3
"""The Material for MkDocs palette from an app's own colours.

    palette.py --light '#176b5c' --dark '#7fcdb6' [--dark-bg '#15181b'] [--note 'noticebox's green']

Prints the `extra.css` that sets Material's primary and accent colours for the light scheme (`default`) and the dark
scheme (`slate`): the app's accent as given, plus the lighter and darker variants Material uses for hover and the
header shadow, each a fixed step towards white or black. `--dark-bg` is the app's dark page background, used as the
header's background in the dark scheme so the docs and the app sit together.
"""
import argparse


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise SystemExit(f"not a colour: #{h}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix(h: str, towards: tuple[int, int, int], amount: float) -> str:
    r, g, b = hex_to_rgb(h)
    out = [round(c + (t - c) * amount) for c, t in zip((r, g, b), towards)]
    return "#" + "".join(f"{c:02x}" for c in out)


def lighter(h: str) -> str:
    return mix(h, (255, 255, 255), 0.18)


def darker(h: str) -> str:
    return mix(h, (0, 0, 0), 0.22)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--light", required=True, help="the accent on a light background, e.g. '#176b5c'")
    p.add_argument("--dark", required=True, help="the accent on a dark background, e.g. '#7fcdb6'")
    p.add_argument("--dark-bg", default=None, help="the app's dark page background, e.g. '#15181b'")
    p.add_argument("--note", default="the app's own accent", help="what the colour is, for the comment")
    a = p.parse_args()
    for h in (a.light, a.dark, a.dark_bg or "#000"):
        hex_to_rgb(h)
    lines = [
        f"/* {a.note}, as the app sets it, so the docs and the app look related. Made by palette.py (docs plugin). */",
        '[data-md-color-scheme="default"] {',
        f"  --md-primary-fg-color: {a.light};",
        f"  --md-primary-fg-color--light: {lighter(a.light)};",
        f"  --md-primary-fg-color--dark: {darker(a.light)};",
        f"  --md-accent-fg-color: {a.light};",
        "}",
        "",
        '[data-md-color-scheme="slate"] {',
        f"  --md-primary-fg-color: {a.dark};",
        f"  --md-primary-fg-color--light: {lighter(a.dark)};",
        f"  --md-primary-fg-color--dark: {darker(a.dark)};",
    ]
    if a.dark_bg:
        lines.append(f"  --md-primary-bg-color: {a.dark_bg};")
    lines += [f"  --md-accent-fg-color: {a.dark};", "}"]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
