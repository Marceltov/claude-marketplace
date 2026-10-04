---
status: "accepted"
date: 2026-10-04
---

# The rules plugin injects standing rules at session start

## Context and Problem Statement

On 2026-09-22 this repo removed its SessionStart hooks (`f71085c`, `a51f1d5`; see the update in ADR 0001): each one injected a rule into every session in every repo, and each duplicated text that already lived in a skill that loads when relevant. Since then no plugin here registers a hook.

Some rules, though, are meant for every session: how to keep tool output, reads and replies small, so that context stays small across all repos. They belong to no single task, so a skill, which loads only when its description matches, would rarely fire for them. How should they reach every session?

## Considered Options

* A `rules` plugin with a SessionStart hook that prints `RULES.md`
* A skill whose description says to use it always
* A user-level `~/.claude/CLAUDE.md`

## Decision Outcome

Chosen option: a `rules` plugin with a SessionStart hook, because it is the only option that puts the rules in context from the first turn on every machine where the marketplace is installed. The hook is one `cat` of `RULES.md`, and its matcher (`startup|clear|compact|resume`) brings the rules back after `/clear` and compaction. A skill depends on matching and would skip exactly the turns where the rules matter. A user CLAUDE.md works, but it isn't versioned or shared through the marketplace.

This does not reverse the reasoning of 2026-09-22: those hooks duplicated skills and applied rules that only some sessions needed. `RULES.md` is the only copy of these rules, and they apply everywhere. A repo's CLAUDE.md wins where the two disagree.

### Consequences

* Good, because the rules hold in every session, in every repo, with one file to edit.
* Bad, because `RULES.md` is sent with every session, so it has to stay short.
