#!/usr/bin/env python3
"""Check a plugin repo's skills and zip them for upload to claude.ai.

Usage: build-claude-ai-skills.py [REPO_ROOT] [--out DIR] [--check-only]

Every skills/<name>/SKILL.md is checked against claude.ai's skill rules
(name = folder name, lowercase letters/digits/hyphens, at most 64 chars,
no reserved words; a description of at most 1024 chars without XML tags).
Skills with a `.claude-code-only` marker are checked but not zipped.
If the repo has scripts/sync-shared.sh, its --check must pass too.
Each zip holds the skill folder itself, which is what claude.ai expects.
"""
import argparse
import pathlib
import re
import subprocess
import sys
import zipfile

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
RESERVED = ("anthropic", "claude")
MARKER = ".claude-code-only"


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def check_skill(skill):
    errors = []
    meta = frontmatter((skill / "SKILL.md").read_text())
    if meta is None:
        return ["SKILL.md has no YAML frontmatter"]
    name, desc = meta.get("name", ""), meta.get("description", "")
    if name != skill.name:
        errors.append(f"name '{name}' differs from folder '{skill.name}'")
    if not NAME_RE.match(name):
        errors.append("name must be 1-64 lowercase letters, digits or hyphens")
    if any(word in name for word in RESERVED):
        errors.append(f"name must not contain {' or '.join(RESERVED)}")
    if not desc:
        errors.append("description is missing")
    elif len(desc) > 1024:
        errors.append(f"description has {len(desc)} chars, max 1024")
    if re.search(r"<[A-Za-z/][^>]*>", desc):
        errors.append("description must not contain XML tags")
    return errors


def zip_skill(skill, out):
    target = out / f"{skill.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill.rglob("*")):
            if path.is_file() and path.name != MARKER:
                zf.write(path, pathlib.Path(skill.name) / path.relative_to(skill))
    return target


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    skills = sorted(p.parent for p in (root / "skills").glob("*/SKILL.md"))
    if not skills:
        sys.exit(f"no skills found under {root / 'skills'}")

    failed = False
    sync = root / "scripts" / "sync-shared.sh"
    if sync.exists() and subprocess.run([str(sync), "--check"]).returncode != 0:
        failed = True

    for skill in skills:
        for err in check_skill(skill):
            print(f"{skill.name}: {err}")
            failed = True
    if failed:
        sys.exit(1)

    if args.check_only:
        print(f"{len(skills)} skills ok")
        return

    out = (root / args.out) if not pathlib.Path(args.out).is_absolute() else pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        if (skill / MARKER).exists():
            print(f"skip (Claude Code only): {skill.name}")
            continue
        target = zip_skill(skill, out)
        print(f"built: {target.relative_to(root) if target.is_relative_to(root) else target}")


if __name__ == "__main__":
    main()
