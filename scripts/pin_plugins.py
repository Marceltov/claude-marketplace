#!/usr/bin/env python3
"""Pins every GitHub-sourced plugin in .claude-plugin/marketplace.json to a commit (ADR 0010).

    python3 scripts/pin_plugins.py            # rewrite the file where a plugin has a new version
    python3 scripts/pin_plugins.py --check    # only report

An install made through claude.ai is updated only when its marketplace entry changes; an entry that names a
repository without a `sha` never changes. So each entry carries `source.sha`, and this moves it to the head of the
plugin repository's branch (`source.ref`, else the default branch) when the `version` in `.claude-plugin/plugin.json`
there differs from the version at the pinned commit. A commit without a version bump does not reach the installs.

Uses only the standard library. GITHUB_TOKEN, when set, is sent (the workflow sets it; public repositories work
without). The last line of output is `changed: <names>` or `unchanged`.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

MARKETPLACE = Path(__file__).resolve().parents[1] / ".claude-plugin" / "marketplace.json"


class GitHub:
    def __init__(self, token: str | None = None):
        self.token = token

    def _get(self, path: str) -> dict:
        request = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"})
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def default_branch(self, repo: str) -> str:
        return self._get(f"/repos/{repo}")["default_branch"]

    def head(self, repo: str, ref: str) -> str:
        return self._get(f"/repos/{repo}/commits/{ref}")["sha"]

    def version(self, repo: str, sha: str) -> str | None:
        """The version in .claude-plugin/plugin.json at that commit, or None if it has none."""
        try:
            content = self._get(f"/repos/{repo}/contents/.claude-plugin/plugin.json?ref={sha}")["content"]
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            raise
        return json.loads(base64.b64decode(content)).get("version")


def pin(marketplace: dict, github) -> list[str]:
    """Moves each GitHub entry's sha where its version changed; returns one line per change. Changes `marketplace`."""
    changes = []
    for plugin in marketplace["plugins"]:
        source = plugin.get("source")
        if not isinstance(source, dict) or source.get("source") != "github":
            continue
        repo = source["repo"]
        head = github.head(repo, source.get("ref") or github.default_branch(repo))
        pinned = source.get("sha")
        if pinned == head:
            continue
        new = github.version(repo, head)
        old = github.version(repo, pinned) if pinned else None
        if pinned and new == old:
            if new is None:
                print(f"warning: {plugin['name']}: {repo} has no version in .claude-plugin/plugin.json; it is never moved", file=sys.stderr)
            continue
        source["sha"] = head
        changes.append(f"{plugin['name']}: {old or 'unpinned'} -> {new or 'no version'} ({head[:7]})")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report, write nothing")
    args = parser.parse_args()

    marketplace = json.loads(MARKETPLACE.read_text())
    changes = pin(marketplace, GitHub(os.environ.get("GITHUB_TOKEN")))
    for line in changes:
        print(line)
    if changes and not args.check:
        MARKETPLACE.write_text(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n")
    print("changed: " + ", ".join(c.split(":")[0] for c in changes) if changes else "unchanged")


if __name__ == "__main__":
    main()
