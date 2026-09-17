---
status: "accepted"
date: 2026-09-17
---

# Ship uncommitted work through a skill with a confirm-gated merge

## Context and Problem Statement

Turning a working tree into a merged PR is a repeated sequence — branch, commit, PR, sometimes an ADR — that was previously assembled by hand each time, in whatever order and with whatever branch got reused for it. One step in that sequence, the merge, is materially different from the rest: it is the point where a change joins shared history and stops being cheaply reversible. How should this sequence be packaged so it runs reliably without giving away standing authorization to take that one risky step on its own?

## Considered Options

* A skill Claude loads when a request matches its description (e.g. "ship this")
* A slash command the user types explicitly
* No packaging — keep assembling the steps ad hoc per request

## Decision Outcome

Chosen option: "a skill", because the requests this replaces ("ship this," "open a PR for this work") are exactly the phrasing a skill's description matching is built for, and a command would need to be remembered and typed verbatim instead. The skill hard-codes a stopping point: every step through opening the PR can run without asking, and the merge step always requires an explicit yes on that specific PR — an earlier general "go ahead and ship this" authorizes building the PR, not merging it.

### Consequences

* Good, because shipping routine work becomes one request instead of five, and the failure mode observed while building this skill — reusing an already-merged branch for unrelated new work — is now written down as a precondition to check.
* Good, because the merge, the one step that is hard to reverse, keeps a human in the loop on every single PR, regardless of how the earlier steps went.
* Bad, because the skill only fires when Claude recognizes the request as matching its description; a command would guarantee invocation at the cost of needing exact recall.

## Pros and Cons of the Options

### A skill

* Good, because it matches natural phrasing ("ship this") without the user needing to know a command name.
* Neutral, because it composes with whatever commit/PR conventions are already in effect for the session, instead of duplicating them.
* Bad, because invocation depends on description matching rather than being guaranteed.

### A slash command

* Good, because invocation is deterministic — no ambiguity about whether it fired.
* Bad, because it requires the user to remember and type an exact command rather than asking in plain language.

### No packaging

* Bad, because every run re-derives the same sequence, and it is where the branch-reuse mistake made during this session's own dogfooding actually happened.
