---
status: "accepted"
date: 2026-09-18
---

# propose-skill always files its issue against the marketplace repo, never the repo it's invoked from

## Context and Problem Statement

`ccp` is installed into arbitrary project repos, but a skill proposal produced by `propose-skill` is only useful if it lands somewhere a marketplace maintainer will see it and can act on it. The invoking user is typically a contributor to whatever project repo they're working in, not to `Marceltov/claude-marketplace` itself — so the question is which repo the resulting GitHub issue should target.

## Considered Options

* File the issue against the current project repo (wherever `ccp` happens to be running)
* File the issue against a fixed target: `Marceltov/claude-marketplace`
* Ask the user each time which repo to target

## Decision Outcome

Chosen option: "file against a fixed target, `Marceltov/claude-marketplace`" — skills only ever live in the marketplace repo, so that's the only repo where the issue can actually be turned into a merged skill. The current project repo has no mechanism to act on it, and asking every time adds a prompt for a question with only one sane answer.

### Consequences

* Good, because the issue always lands where someone with write access to the marketplace can pick it up.
* Good, because the skill needs no configuration or per-repo setup — the target is a constant.
* Bad, because it hardcodes one marketplace owner/repo; forking `ccp` for a different marketplace means updating this one string.

## Pros and Cons of the Options

### File against the current project repo

* Bad, because most project repos have no relationship to the marketplace and no one there can build a Claude Code skill from the issue.

### File against a fixed target

* Good, because it matches the one place a skill proposal can actually be realized.
* Neutral, because it assumes a single marketplace repo per `ccp` install, which holds today but wouldn't for a multi-marketplace fork.

### Ask each time

* Bad, because the answer is the same every time for this plugin's current audience — the prompt would just be friction, not a real choice.
