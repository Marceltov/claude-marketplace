---
status: "accepted"
date: 2026-09-18
---

# Branches, commit messages, and PR titles carry a `<REPONAME> #<issue-number>` prefix

## Context and Problem Statement

Across multiple repos and multiple issues, it's hard to tell at a glance which commit, branch, or PR belongs to which piece of tracked work, especially once several repos' histories get mixed together in tooling (dashboards, cross-repo search, notifications) that shows them side by side. `ship-pr` and `triage-issues` already had the pieces (branch slugs, `Closes #N` in PR bodies) but no consistent, greppable prefix tying all three artifacts for one unit of work together by name.

## Considered Options

* No prefix — rely on `Closes #N` in the PR body and the repo context alone
* A parenthesized prefix identical across branch, commit, and PR: `(reponame-issueid)`
* A `<REPONAME> #<issue-number>: ` prefix on commit messages and PR titles, with a punctuation-free equivalent (`reponame-issueid-slug`) for branch names, since branch refs don't tolerate `#`/`:`/parens cleanly
* Always require an issue to exist before naming anything (ask the user, or block) vs. looking the issue up automatically and falling back to no prefix only when lookup can't resolve one

## Decision Outcome

Chosen option: `<REPONAME> #<issue-number>: <message>` for commit messages and PR titles (e.g. `CLAUDE-MARKETPLACE #6: Add propose-skill skill to ccp`), and `<reponame-lowercase>-<issue-number>-<slug>` for branch names (e.g. `claude-marketplace-6-add-propose-skill`) — same information, formatted for what each field actually tolerates. The issue number is resolved automatically: already known when handed off from `triage-issues` or named directly by the user, otherwise looked up by matching the change against the repo's open issues (`gh issue list` / `glab issue list`). Only when that lookup can't confidently resolve one match does the work ship without a prefix, rather than blocking on a question the user has already said not to ask.

Enforcement lives in the `ship-pr` and `triage-issues` skill bodies, which carry the exact commands and apply the convention to everything they create. A `SessionStart` hook (`hooks/naming-convention.py`) also injected it as standing context so it would cover branches/commits/PRs made outside those skills; that hook was removed on 2026-09-22 — see the update below.

### Consequences

* Good, because a commit, branch, or PR can be traced back to its repo and issue by name alone, even out of context (cross-repo dashboards, notifications, `git log` across clones).
* Good, because the common case (issue already known from triage, or unambiguous from the repo's issue list) needs no extra confirmation step.
* Bad, because automatic issue matching is a heuristic (title/body keyword match) — it can occasionally pick the wrong issue or miss one that exists but doesn't say so in its title, silently falling back to no prefix instead of erring.
* Neutral, because branch names and commit/PR titles now use two different (though clearly related) renderings of the same prefix, rather than one literal string everywhere.

## Pros and Cons of the Options

### No prefix

* Good, because it's what already existed — zero new surface.
* Bad, because it doesn't solve the actual problem: nothing in the name itself ties a commit/branch/PR to its repo and issue.

### Identical parenthesized prefix everywhere

* Good, because one literal string is simpler to generate and to pattern-match on.
* Bad, because branch names with parentheses need shell-quoting and read awkwardly in everyday `git checkout`/`git branch` usage — explicitly rejected in favor of a branch-safe rendering.

### Format-appropriate prefix per field, auto-resolved issue number

* Good, because each field gets a prefix rendering that's natural for how it's actually used (a ref vs. free text).
* Good, because it degrades gracefully (no prefix) instead of blocking when the automatic lookup genuinely can't find a match.

### Always require an issue up front

* Good, because it would guarantee 100% prefix coverage, no fallback case.
* Bad, because it turns every "just ship this" into a forced detour through issue creation/selection, for a convention whose whole point is to reduce friction, not add it.

## More Information

**Update (2026-09-22):** the `SessionStart` hook was removed. It re-injected this convention into every session in every repo, whether or not a branch was ever created, and the rule it injected duplicated text the `ship-pr` and `triage-issues` skill bodies already carry — a second copy to keep in sync for a case (creating a branch by hand, outside either skill) that had not actually come up. The convention itself is unchanged; the skills are now its only home.
