---
description: Bring a branch into a mergeable state by pulling its target branch, merging it in, and resolving any conflicts. Use when asked to "resolve conflicts", "sync this branch with main", "update this branch", "merge main into this", or when a PR/MR shows as not mergeable due to conflicts.
---

# resolve-conflicts: sync with target, resolve, verify mergeable

Gets a branch to a state where its PR/MR can merge cleanly. Stops at that point — it never merges the PR/MR itself; that's ship-pr's job, and ship-pr's confirm gate still applies.

## 1. Run the mechanical part

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/sync-branch.sh
```

This refuses to run on a dirty working tree (commit or stash first — don't stash silently without telling the user, since it hides in-progress work). It otherwise: finds the target branch (the open PR/MR's base if one exists, else the repo's default branch), fetches it, and attempts `git merge --no-edit origin/<target>`. There's exactly one right way to do this part, so it's scripted rather than re-derived per request.

If it exits 0, the merge was clean — skip to step 4. If it exits nonzero, it printed the conflicted files; move to step 2.

## 2. Resolve each conflicted file

This is the part that needs judgment, so it isn't scripted. For each file `git diff --name-only --diff-filter=U` listed:

1. Read the full file, not just the conflict markers — understand what each side was trying to do, not just what the lines say.
2. Produce a resolution that preserves the intent of both sides where they don't actually contradict each other. Don't default to "ours" or "theirs" wholesale unless the conflict is genuinely trivial (a lockfile, a changelog entry, a generated file) — those are the only cases where picking one side outright is safe without reading the surrounding logic.
3. If a conflict changes logic rather than nearby unrelated lines — two different implementations of the same function, a schema field changed on both sides in incompatible ways — stop and describe the conflict to the user instead of guessing. Silently picking a side on something semantically ambiguous is exactly the failure mode this step exists to avoid.
4. Remove the conflict markers and `git add` the file once it's resolved.

## 3. Finish the merge

```bash
git commit --no-edit
```

If a build or test command is discoverable for this repo, run it before pushing — conflict markers being gone doesn't mean the merged logic is correct, only that git stopped complaining about it.

`git merge --abort` cleanly backs out of the whole thing if resolution goes sideways partway through; prefer it over trying to hand-fix a merge that's gotten confusing.

## 4. Push and confirm mergeable

```bash
git push
```

Then confirm the forge agrees it's mergeable:

```bash
gh pr view --json mergeable -q .mergeable      # GitHub: expect MERGEABLE
glab mr view -F json                           # GitLab: check merge_status
```

Report the result. Don't merge the PR/MR — that's a separate, explicitly confirmed step (see the `ship-pr` skill).
