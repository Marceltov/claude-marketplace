---
status: "accepted"
date: 2026-09-17
---

# triage-issues defaults to plain issues and hands off to ship-pr rather than owning the workflow

## Context and Problem Statement

Turning a backlog into something actionable needs to fetch from somewhere (plain issues, or a linked GitHub Project's items with its richer status/field data), rank it, and then do something once the user picks one. Two decisions don't have an obvious single answer: which source to fetch from by default, and whether picking an issue should kick off branch/commit/PR itself or delegate to the `ship-pr` skill that already owns that sequence.

## Considered Options

* Source: always fetch Project items (richer) vs. always fetch plain issues (cheaper, works on both forges) vs. default to issues and switch to Project items only when asked
* Handoff: `triage-issues` re-implements branch/commit/PR/merge itself vs. it only names a branch and hands off to `ship-pr` for everything after that

## Decision Outcome

Chosen for source: "default to issues, switch to Project items on request" — issues and Project items overlap heavily for a GitHub repo (most Project items reference an issue), plain issues are one cheap `gh issue list --json ...` / `glab issue list -O json` call on either forge, and GitHub Projects need an extra owner/number lookup before anything can be fetched. Defaulting to the cheap, portable path and only paying for the richer one when the user names it directly avoids that lookup in the common case.

Chosen for handoff: `triage-issues` stops at naming a branch (`<number>-<slug>`) and invoking `ship-pr`'s branch step; it does not reimplement commit, PR, or merge. Duplicating that sequence here would mean two places to keep the confirm-gated-merge behavior correct instead of one.

### Consequences

* Good, because the common case (repo issues, either forge) never pays for a Project lookup it doesn't need.
* Good, because the confirm gate on merging only has one implementation to stay correct — `ship-pr`'s — regardless of whether work started from triage or from a plain "ship this."
* Bad, because GitLab's issue board has no JSON-listing command in `glab` today, so "project/board" mode is GitHub-only; GitLab always falls back to its plain issue list even if the user says "board."

## Pros and Cons of the Options

### Always fetch Project items

* Good, because it surfaces custom fields (status, iteration) issues alone don't have.
* Bad, because it requires resolving which project is linked before the first issue can even be listed, on every run.

### Always fetch plain issues

* Good, because it's one call, works identically on both forges.
* Bad, because it loses Project-specific triage data (status columns, custom fields) for users who do rely on a Project board.

### Default to issues, switch on request

* Good, because it's cheap by default and richer on demand.
* Neutral, because it means two code paths (issues vs. items) instead of one, mirrored only on GitHub.

### triage-issues re-implements the ship sequence

* Bad, because ship-pr's confirm gate — the one behavior this whole plugin exists to guarantee — would need to be duplicated and kept in sync in a second place.

### triage-issues hands off to ship-pr

* Good, because there's exactly one place a picked issue's work can end up merged from, and it's the one already reviewed for the confirm-gate behavior.
