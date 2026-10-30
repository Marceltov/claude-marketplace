---
status: "accepted"
date: 2026-10-30
---

# The standing rules move to the engineering-conventions plugin

## Context and Problem Statement

ADR 0008 gave the standing rules for every session (small tool output, narrow reads and searches, no unasked subagents, short replies) a `rules` plugin with a SessionStart hook. Since then, Marcel's conventions for every repository have their own public repository and plugin, [Marceltov/engineering-conventions](https://github.com/Marceltov/engineering-conventions), which also has a SessionStart hook. Two plugins now carry standing rules, and both inject them into every session. Where should the standing rules live?

## Considered Options

* Keep the `rules` plugin next to engineering-conventions
* Move the rules into engineering-conventions and remove the `rules` plugin

## Decision Outcome

Chosen option: move the rules into engineering-conventions. The rules are explained on its page _Working rules for Claude sessions_, and they reach each session through its hook, whose matcher is `startup|clear|compact|resume`, as before. One plugin and one hook now carry every standing rule, and the rules gain a page with their reasons. ADR 0008's reasoning still holds (a hook, not a skill, and kept short); only the place changes. The marketplace lists `engineering-conventions` in place of `rules`.

### Consequences

* Good, because every standing rule has one home, versioned and published with the conventions.
* Good, because there is one SessionStart hook instead of two.
* Bad, because an installed `rules@marceltov` stops updating: uninstall it and install `engineering-conventions@marceltov`.
