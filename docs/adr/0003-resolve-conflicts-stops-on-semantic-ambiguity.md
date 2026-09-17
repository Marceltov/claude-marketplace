---
status: "accepted"
date: 2026-09-17
---

# resolve-conflicts auto-merges mechanically, but stops on semantic conflicts

## Context and Problem Statement

Bringing a branch into a mergeable state has two very different halves: finding the target branch, fetching it, and attempting the merge is mechanical (same script, same steps, every time); resolving an actual conflict is not, since it requires understanding what each side of the conflict was trying to do. How much of conflict resolution should run without asking, and where should it stop and involve the user?

## Considered Options

* Fully automatic: resolve every conflict without asking, picking a side or synthesizing one
* Fully manual: only run the mechanical fetch-and-merge step, leave all resolution to the user
* Hybrid: auto-merge cleanly when possible, resolve trivial/generated-file conflicts automatically, but stop and describe anything that changes logic

## Decision Outcome

Chosen option: "hybrid", because most of the sequence genuinely has one right answer (which branch to fetch, whether a merge conflicted) and scripting it saves nothing by involving the user, while conflict resolution on real logic is exactly the kind of thing that goes wrong silently if automated — a merge that "resolves" by guessing wrong doesn't fail loudly, it ships broken behavior. `scripts/sync-branch.sh` handles the mechanical half and stops the moment a merge conflicts, listing the affected files; the `resolve-conflicts` skill takes over from there with instructions to resolve trivial cases (lockfiles, changelogs, generated files) directly but stop and describe anything that changed logic on both sides instead of picking one.

### Consequences

* Good, because the common case — target fetched, merge clean — needs no back-and-forth at all.
* Good, because a conflict that could hide a real behavioral disagreement gets surfaced instead of silently resolved in whichever direction seemed more likely.
* Bad, because "trivial" vs. "changes logic" is a judgment call the skill has to make per conflict, not a rule a script could enforce; a future iteration might need to sharpen that line if it proves too permissive or too cautious in practice.

## Pros and Cons of the Options

### Fully automatic

* Good, because it never interrupts the user.
* Bad, because a wrong automatic resolution on real logic ships silently — the worst failure mode available here.

### Fully manual

* Good, because it never guesses.
* Bad, because it throws away the mechanical part that has only one right answer, making even a conflict-free sync require a full manual walkthrough.

### Hybrid

* Good, because the two halves are handled the way each actually deserves.
* Neutral, because it means one script plus one skill instead of a single artifact, mirroring the split already made in docs/adr/0002 for the forge-view commands.
