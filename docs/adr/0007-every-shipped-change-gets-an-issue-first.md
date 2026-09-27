---
status: "accepted"
date: 2026-09-27
---

# Every shipped change gets an issue first

## Context and Problem Statement

ADR 0006 gave branches, commits, and PR titles a `<REPONAME> #<issue-number>` prefix, but when no open issue matched the change, `ship-pr` shipped it with a plain, unprefixed name. That left gaps in exactly the tracing the prefix exists for.

## Considered Options

* Keep the unprefixed fallback (ADR 0006)
* Ask the user for an issue when none matches
* Create an issue automatically when none matches

## Decision Outcome

Chosen option: create an issue automatically. When the issue number isn't already known and no open issue matches with confidence, `ship-pr` runs `gh issue create` / `glab issue create` with a short title and description of the change, then uses the new number for the branch, commit, and PR as usual. The PR's `Closes #N` closes it on merge.

### Consequences

* Good, because every branch, commit, and PR carries the prefix, with no unnamed fallback.
* Good, because it doesn't block on a question, which ADR 0006 already ruled out.
* Bad, because an ambiguous match (two plausible issues) now yields a third, new issue rather than one of the existing ones, which can leave near-duplicates to clean up.
