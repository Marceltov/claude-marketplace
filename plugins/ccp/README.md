# ccp

Code Collaboration Platform toolkit. The `ship-pr` skill ships uncommitted work end to end: branch, commit, PR, an ADR when the change is architecturally significant, and a merge that only happens after you explicitly confirm it. A `Stop` hook nudges you when work is left unshipped; it never acts on its own. Slash commands round it out with one-shot GitHub/GitLab project-management views.

## Install

```bash
/plugin marketplace add Marceltov/claude-marketplace
/plugin install ccp@marceltov
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

## The nudge hook

A `Stop` hook (`hooks/nudge-ship.py`) runs after every turn and checks for uncommitted changes, or a branch that's ahead of the default branch with no open PR. If it finds either, it shows a `systemMessage` — a warning printed to the user, not fed into Claude's context — suggesting the `ship-pr` skill. It never branches, commits, opens a PR, or merges by itself; it only ever surfaces a reminder. It stays quiet once a PR is already open and the tree is clean.

## Project-management commands

Five slash commands, all backed by `scripts/forge.sh`, which detects GitHub vs GitLab by asking `gh` and `glab` directly whether either recognizes the current repo (so self-hosted instances work the same as github.com/gitlab.com) and runs the matching CLI:

| Command | GitHub | GitLab |
| --- | --- | --- |
| `/issues` | `gh issue list --web` | opens `<repo>/-/issues` |
| `/actions` | `gh browse --actions` | opens `<repo>/-/pipelines` |
| `/prs` | `gh pr list --web` | opens `<repo>/-/merge_requests` |
| `/pr` | `gh pr view` (terminal) | `glab mr view` (terminal) |
| `/repo` | `gh repo view --web` | `glab repo view --web` |
| `/project` | `gh browse --projects` | opens `<repo>/-/boards` |

`/issues`, `/actions`, `/prs`, `/repo`, and `/project` open a browser tab; `/pr` prints the current branch's PR/MR to the terminal instead, since that one's about a quick status check, not a page to open. `glab` has no `--web` flag on `issue list`/`mr list`, so those two cases open a URL directly via `open`/`xdg-open` (falling back to Python's `webbrowser` module, or just printing the URL if neither is available). GitLab has no direct equivalent of GitHub Projects; `/project` opens the closest thing, its issue board.

## The resolve-conflicts skill

Ask to "resolve conflicts", "sync this branch with main", or similar, and this skill brings the current branch into a mergeable state without merging the PR/MR itself. `scripts/sync-branch.sh` handles the mechanical half — find the target branch (the open PR/MR's base, or the repo default), fetch it, attempt `git merge --no-edit`. If that conflicts, the skill resolves each file with judgment: trivial cases (lockfiles, changelogs, generated files) get resolved directly, but a conflict that changes logic on both sides gets described to the user instead of guessed at. See `docs/adr/0003` for why it draws the line there.

## The triage-issues skill

Ask "show me the issues," "what should I work on," "triage the backlog," or similar. Fetches open issues (GitHub or GitLab) — or the linked GitHub Project's items, if you ask for "project"/"board" specifically — groups and sorts them for triage (bugs before enhancements, unassigned before already-claimed, labels/milestones over raw recency), and summarizes each with what doing it would actually involve, not just its title. Ends by asking which one to start on.

Pick one and it hands off into `ship-pr`: names a branch from the issue (`<number>-<slug>`), runs `ship-pr`'s branch step with that name, and the rest of that skill proceeds as normal — confirm-gated merge included. When the PR gets opened, its body includes a closing reference (`Closes #<number>`) back to the issue.

GitLab's issue board has no JSON-listing command in `glab`, so project/board mode is GitHub-only for now; GitLab always uses the plain issue list.

## The propose-skill skill

Ask to "skillify this", "turn this into a skill", "propose a new skill", or similar. Scans the current conversation for a repeatable work pattern (a multi-step procedure, a workaround, something you had to correct or explain twice), proposes a few candidate directions, and lets you pick or steer toward something else. Once you pick, it drafts a full spec — plugin, skill name, description/trigger phrases, workflow steps, source context — and files it as a GitHub issue against `Marceltov/claude-marketplace`, never the repo you're currently in. That's deliberate: skills live in the marketplace repo, and you usually don't have write access there, so this always goes through an issue for a maintainer to pick up, not a direct commit.

## License

MIT, same as the marketplace.
