---
description: End-to-end git shipping workflow — branch, commit all changes, open a PR, write an ADR when the change is architecturally significant, then merge only after the user explicitly confirms. Use when asked to "ship this", "open a PR for this work", "ship it", or to turn the current uncommitted changes into a merged PR.
---

# ship-pr: branch to merge, with a confirm gate

A fixed sequence for turning working-tree changes into a merged PR. Every step before the merge can run without asking; the merge step never runs without an explicit yes from the user, no matter how the earlier steps went.

## 0. Preconditions

Run `git status` before anything else. If the tree is clean and the current branch has no unpushed commits ahead of its PR-worthy base, there is nothing to ship — say so and stop.

If the current branch is the repo's default branch (`main`/`master`) and it has uncommitted changes, always create a new branch before committing — never commit directly to the default branch. If already on a non-default branch, reuse it unless the user asked for a fresh one.

## 1. Branch

Name it a short kebab-case slug describing the change (e.g. `unwrap-markdown-hook`, not `feature/fix-1` or a timestamp). Derive it from what actually changed, not from the literal request text.

```bash
git checkout -b <slug>
```

## 2. Commit

Stage explicitly, never with a blanket `-A`/`.` without reviewing what it picks up — run `git status` after staging and check for anything that looks like a secret or an unrelated file before committing.

Write the commit message the same way you would for any commit in this session: focus on *why*, follow the repo's existing message style (check `git log` if unfamiliar with it), and keep whatever attribution trailer this session is already using.

If the changes naturally split into unrelated concerns, use separate commits rather than one commit that bundles them — but still one branch and one PR unless the user says otherwise.

## 3. ADR — only when it earns its keep

Write an ADR when the change has at least one of these:

- Introduces or removes a dependency, tool, service, or convention future contributors will run into.
- Is hard to reverse, or reversing it would be expensive.
- Picks between two or more reasonable approaches for a non-obvious reason — the kind of thing a future reader would ask "why not the other way?" about.
- Changes something cross-cutting: a shared interface, a security boundary, a data model, a build/release process.

Skip it for bug fixes, docs, dependency bumps within the same major version, formatting, tests, or anything a diff already explains on its own.

When one is warranted:

1. Look for where this repo already keeps ADRs — check, in order, `docs/adr/`, `doc/adr/`, `adr/`, `architecture/decisions/`. Use whichever exists; if none does, create `docs/adr/`.
2. Number it one past the highest existing ADR (`0001` if the directory is new).
3. Base it on `templates/adr-template.md` in this plugin — the [MADR](https://adr.github.io/madr/) format. Fill in `Context and Problem Statement`, `Considered Options`, and `Decision Outcome` at minimum; drop whichever optional sections (`Decision Drivers`, `Consequences`, `Confirmation`, `Pros and Cons`, `More Information`) don't earn their keep for this decision, same as the template's own comments say. Keep it short — a paragraph or two per section, not an essay.
4. Commit the ADR in the same branch, either folded into the main commit or as its own commit titled like `Add ADR NNNN: <title>`.

## 4. Push and open the PR

```bash
git push -u origin <slug>
gh pr create --title "<short imperative title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test plan
<checklist>
EOF
)"
```

Follow this session's existing PR conventions (attribution trailer, no placeholder sections). Report the PR URL back to the user.

## 5. Confirm, then merge

Stop here and show the user the PR URL, then ask directly: merge now, or wait? Do not treat an earlier general "go ahead and ship this" as covering the merge — that authorization was for building the PR, not for merging it, per this session's standing rule that approval doesn't carry across separate risky actions.

Only on an explicit yes:

1. Check how prior PRs in this repo were merged (`gh pr list --state merged` or `git log --merges` for the merge commit shape) and match that method. Default to `gh pr merge <number> --merge` when there's no discernible precedent.
2. Run the merge. Never pass `--admin` to bypass required checks unless the user explicitly says to.
3. Confirm the merge landed (`gh pr view <number> --json state,mergedAt`) and report the result.

If the user says wait, or doesn't answer, leave the PR open and stop — do not poll for approval or merge later without being asked again.
