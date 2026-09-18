---
description: Scan the current conversation for a repeatable work pattern worth turning into a skill, propose a few candidate directions, then file a GitHub issue against the marketplace repo (never a direct commit — the invoking user usually has no write access there) with everything a maintainer needs to build it. Use when asked to "skillify this", "turn this into a skill", "propose a new skill", "file a skill request", "make this repeatable", or similar.
---

# propose-skill: turn a chat pattern into a skill request

Never assume prior knowledge of what's worth codifying — the value here is in reading *this* conversation, not guessing from the skill's own name.

## 1. Scan the conversation for candidates

Look for patterns like:

- A multi-step procedure the user walked you through that required judgment calls (not just one obvious tool call).
- A workaround or non-obvious sequence you'd otherwise have to rediscover next time.
- Something the user corrected you on, or had to explain twice.
- A task shape that's clearly going to recur (project-specific conventions, a repeated review checklist, a recurring integration).

Skip anything that was a one-off, trivial, or already covered by an existing skill — check the current plugin's other skills and, if reachable, the rest of the marketplace before proposing something that overlaps.

## 2. Propose 2-4 directions, then let the user steer

Present each candidate as one line: what the pattern is, and why it's worth codifying (repeats, non-obvious, multi-step, previously corrected). Ask which one to pursue, or whether the user has something else in mind — their steer always wins over your own read of the chat, including a direction not on your list.

## 3. Draft the skill spec

Once a direction is picked, write it up as if you were about to create the skill yourself (see `superpowers:writing-skills` for the quality bar on structure and phrasing), but don't create any files — the issue carries the spec instead:

- **Plugin**: an existing plugin in this marketplace it fits under, or a proposed new one with a one-line reason why it doesn't fit an existing one.
- **Skill name**: kebab-case, verb-first where it fits the marketplace's existing naming (`ship-pr`, `resolve-conflicts`, `triage-issues`).
- **Description / trigger phrases**: the exact frontmatter-style one-liner, phrased so another Claude instance reading only that line knows when to fire it.
- **Workflow**: numbered steps describing what actually happened in this conversation, generalized just enough to repeat — not a transcript, and not so abstract it loses the judgment calls that made it worth codifying.
- **Source context**: one or two sentences on what prompted this, with anything sensitive (secrets, internal URLs, proprietary details) left out — the issue is public.

## 4. File the issue in the marketplace repo, not the current one

The target is always `Marceltov/claude-marketplace`, regardless of which repo this skill was invoked from — that's where skills actually live, and the invoking user typically can't push there directly.

```bash
gh issue create --repo Marceltov/claude-marketplace \
  --title "New skill: <skill-name>" \
  --body "$(cat <<'EOF'
## Plugin
<existing plugin, or proposed new one + reason>

## Skill name
<kebab-case-name>

## Description / trigger
<the frontmatter-style one-liner>

## Workflow
1. ...
2. ...

## Source context
<1-2 sentences, nothing sensitive>
EOF
)"
```

## 5. Report back

Give the user the issue URL. Don't create branches, files, or PRs for the proposed skill itself — that's the maintainer's call once the issue is triaged.
