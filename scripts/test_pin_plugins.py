"""Tests for pin_plugins.py with a fake GitHub. Run: python3 -m unittest discover -s scripts"""

import copy
import unittest

import pin_plugins


class FakeGitHub:
    def __init__(self, heads, versions):
        self.heads, self.versions, self.calls = heads, versions, []

    def default_branch(self, repo):
        return "main"

    def head(self, repo, ref):
        self.calls.append(("head", repo, ref))
        return self.heads[repo]

    def version(self, repo, sha):
        return self.versions.get(sha)


def market(*sources):
    return {"plugins": [{"name": f"p{i}", "source": s} for i, s in enumerate(sources)]}


class Pin(unittest.TestCase):
    def test_unpinned_entry_is_pinned_to_head(self):
        m = market({"source": "github", "repo": "o/a"})
        changes = pin_plugins.pin(m, FakeGitHub({"o/a": "h1"}, {"h1": "1.0.0"}))
        self.assertEqual(m["plugins"][0]["source"]["sha"], "h1")
        self.assertEqual(changes, ["p0: unpinned -> 1.0.0 (h1)"])

    def test_new_commit_without_version_bump_is_not_shipped(self):
        m = market({"source": "github", "repo": "o/a", "sha": "h1"})
        changes = pin_plugins.pin(m, FakeGitHub({"o/a": "h2"}, {"h1": "1.0.0", "h2": "1.0.0"}))
        self.assertEqual(m["plugins"][0]["source"]["sha"], "h1")
        self.assertEqual(changes, [])

    def test_version_bump_moves_the_pin(self):
        m = market({"source": "github", "repo": "o/a", "sha": "h1"})
        changes = pin_plugins.pin(m, FakeGitHub({"o/a": "h3"}, {"h1": "1.0.0", "h3": "1.1.0"}))
        self.assertEqual(m["plugins"][0]["source"]["sha"], "h3")
        self.assertEqual(changes, ["p0: 1.0.0 -> 1.1.0 (h3)"])

    def test_pin_at_head_is_left_alone(self):
        m = market({"source": "github", "repo": "o/a", "sha": "h1"})
        before = copy.deepcopy(m)
        self.assertEqual(pin_plugins.pin(m, FakeGitHub({"o/a": "h1"}, {"h1": "1.0.0"})), [])
        self.assertEqual(m, before)

    def test_other_source_kinds_are_untouched(self):
        m = {"plugins": [{"name": "local", "source": "./plugins/ccp"},
                         {"name": "sub", "source": {"source": "git-subdir", "url": "u", "path": "p", "ref": "main"}},
                         {"name": "url", "source": {"source": "url", "url": "u", "sha": "s"}}]}
        before = copy.deepcopy(m)
        fake = FakeGitHub({}, {})
        self.assertEqual(pin_plugins.pin(m, fake), [])
        self.assertEqual((m, fake.calls), (before, []))

    def test_an_entry_ref_is_followed_instead_of_the_default_branch(self):
        fake = FakeGitHub({"o/a": "h1"}, {"h1": "1.0.0"})
        pin_plugins.pin(market({"source": "github", "repo": "o/a", "ref": "stable"}), fake)
        self.assertEqual(fake.calls, [("head", "o/a", "stable")])

    def test_the_file_round_trips_unchanged(self):
        text = pin_plugins.MARKETPLACE.read_text()
        import json
        self.assertEqual(json.dumps(json.loads(text), indent=2, ensure_ascii=False) + "\n", text)


if __name__ == "__main__":
    unittest.main()
