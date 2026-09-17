# ship-pr

Ships uncommitted work end to end: branch, commit, PR, an ADR when the change is architecturally significant, and a merge that only happens after you explicitly confirm it.

## Install

```bash
/plugin marketplace add Marceltov/claude-marketplace
/plugin install ship-pr@marceltov
```

## What it does

Ask for "ship this", "open a PR for this work", or similar, and the `ship-pr` skill runs a fixed sequence:

1. **Branch** — off the default branch, named for what changed, never committing straight to `main`/`master`.
2. **Commit** — staged deliberately, reviewed for secrets, following the repo's existing message conventions.
3. **ADR** — written only when the change introduces a dependency or convention, is hard to reverse, picks between two reasonable approaches for a non-obvious reason, or touches something cross-cutting. Skipped for fixes, docs, and anything a diff already explains.
4. **PR** — opened with `gh pr create`, following the repo's existing PR conventions.
5. **Merge** — happens only after you say yes to that specific PR. An earlier "go ahead and ship this" authorizes steps 1-4, not the merge.

## Why the confirm gate

Everything up to opening the PR is easy to undo — close the PR, delete the branch. Merging isn't, so it gets its own explicit approval every time, never inherited from an earlier "go ahead."

## License

MIT, same as the marketplace.
