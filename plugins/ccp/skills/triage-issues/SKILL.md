---
description: Fetch open issues (or the linked GitHub Project's items) for this repo, group and sort them for triage, summarize each with a suggested next step, and let the user pick one to start on. Use when asked "show me the issues", "what should I work on", "triage the backlog", "list issues from the project/board", or similar.
---

# triage-issues: fetch, rank, summarize, hand off

Turns a raw issue list into something to act on, then hands the picked issue to the `ship-pr` skill to start work.

## 1. Pick the source

Default to this repo's issues. Switch to the linked GitHub Project only when the user's phrasing says "project" or "board" specifically — issues and project items overlap heavily, and the plain issue list is cheaper to fetch and covers the common case.

**GitHub, issues (default):**

```bash
gh issue list --state open --limit 30 \
  --json number,title,labels,assignees,comments,updatedAt,url,body
```

**GitHub, project (when asked for it):** find the linked project first — `gh project list --owner <owner> --format json` — and if more than one comes back, ask which before proceeding. Then:

```bash
gh project item-list <number> --owner <owner> --format json --limit 50
```

**GitLab, issues:**

```bash
glab issue list -O json
```

GitLab's issue board has no equivalent JSON-listing command in `glab`, so project/board mode isn't supported there yet — use issues even if the user says "board."

## 2. Group and sort for triage

There's no fixed formula — every repo's label taxonomy is different — but use this judgment, in order:

1. Bugs and anything that looks blocking before enhancements, questions, or discussion-only issues.
2. Unassigned before already-assigned — an assigned issue already has someone on it.
3. Within a tier, prefer whatever the labels/milestones actually signal (a `priority:high` label, an overdue milestone) over recency; fall back to most-recently-active when nothing else distinguishes two issues.

Drop anything that's clearly not actionable right now (blocked on another issue, waiting on external input) to the bottom rather than excluding it.

## 3. Summarize each with a next step

Read each issue's title and body (not just the title) and write one line describing what doing it would actually involve — not a restatement of the title. Distinguish, for instance, a small self-contained fix from something that needs a design discussion first or has no repro steps yet. This is where the judgment is; a title alone usually doesn't say enough to act on.

## 4. Present as a numbered list

One line per issue: number, a short next-step summary, then labels/assignee in parentheses. Numbered so the user can respond with just a number. End by asking which one to start on — don't just list and stop.

## 5. On pick, hand off to ship-pr

Once the user picks one:

1. The issue number is already known — skip `ship-pr`'s own issue lookup and go straight to its branch step (§1) with that number, so the branch, commit, and PR all get the `<REPONAME> #<issue-number>` prefix.
2. Everything else in `ship-pr` proceeds exactly as it normally would, confirm-gated merge included.
3. When `ship-pr` gets to opening the PR, include a closing reference to the issue in the PR body (`Closes #<number>` on GitHub, `Closes #<iid>` on GitLab) so merging it closes the issue automatically.
