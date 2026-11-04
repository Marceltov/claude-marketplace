---
status: "accepted"
date: 2026-11-04
---

# Our plugins start the pin when their version changes

## Context and Problem Statement

ADR 0010 moves the pinned commits with a scheduled workflow, hourly since #40. A version bump in one of Marcel's own plugins still waits up to an hour before installs see it, and scheduled runs are late or skipped when GitHub is busy. ADR 0010 rejected letting plugin repositories push their new commit here (its option 2), because that needed a token with write access to this repository in every plugin repository, three of which were not Marcel's. Issue #42.

## Considered Options

1. **Our plugin repositories start this repository's pin workflow** (`gh workflow run pin-plugins.yml`) when `.claude-plugin/plugin.json` changes on `main`, with a token that may only start workflows here.
2. **A tighter schedule** (every 15 or 5 minutes).
3. **Leave it hourly.**

## Decision Outcome

Chosen: option 1, for the plugins in Marcel's own repositories (engineering-conventions, trilium-plugin, trilium-llm-wiki, paperless-ngx-plugin, passageway). Each has `.github/workflows/pin-in-marketplace.yml`, which runs on a push to `main` that changes `.claude-plugin/plugin.json` and starts `pin-plugins.yml` here with the secret `MARKETPLACE_PIN_TOKEN`. That token is a fine-grained personal access token on this repository only, with Actions: read and write and nothing else; it can start a workflow, not write code (checked on 2026-11-04). It is in 1Password as `Business Admin/claude-marketplace pin token`. The pin itself is unchanged: `scripts/pin_plugins.py` decides, and the workflow commits. The hourly run stays, for the plugins of others and as the fallback.

Option 2 does not make GitHub run schedules on time, and fills the Actions list with runs that change nothing. Option 3 is what we had.

### Consequences

- Good, because a version bump in our plugins reaches installs about a minute after its merge.
- Good, because a leaked token can start the pin and nothing else; ADR 0010's objection to option 2 was write access.
- Bad, because the token lives as a secret in five repositories and has to be renewed in all of them when it is replaced.
- Neutral: a plugin of someone else still waits for the hourly run.

### Confirmation

A version bump merged in engineering-conventions starts a `workflow_dispatch` run of `pin-plugins.yml` here within a minute, and its pin commit follows.
