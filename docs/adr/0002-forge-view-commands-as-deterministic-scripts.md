---
status: "accepted"
date: 2026-09-17
---

# Expose GitHub/GitLab views as deterministic slash commands, not skill judgment

## Context and Problem Statement

`ccp` needed a handful of one-shot project-management lookups — open the issues list, open CI/CD runs, open the PR/MR list, show the current branch's PR/MR, open the repo home page — that work the same way against either GitHub or GitLab. Each one is a fixed action with no branching logic once the forge is known, and the repo could be on either forge without saying so up front.

## Considered Options

* Slash commands whose body runs a bundled script via inline `` !`cmd` `` execution (CLI-executed, before Claude sees the prompt)
* A skill that tells Claude, in prose, to run the right `gh`/`glab` invocation itself
* GitHub's and GitLab's official MCP servers

## Decision Outcome

Chosen option: "slash commands with inline `` !`cmd` `` execution", because these are fixed lookups with no judgment call to make — the same script and argument should run every time a given command is typed, not something Claude decides how to approach per request. A skill would reintroduce exactly the non-determinism this doesn't need. The official MCP servers were ruled out for a different reason: they're remote API wrappers and have no way to open a window in the user's local browser, which is what four of the five commands need to do.

Forge detection (`plugins/ccp/scripts/forge.sh`) asks `gh repo view` and `glab repo view` directly whether either recognizes the current repo, rather than pattern-matching the remote URL for "github"/"gitlab" — this also covers self-hosted GitHub Enterprise and GitLab instances, which a URL substring check would miss.

### Consequences

* Good, because each command behaves identically every time — no dependence on Claude re-deriving the right CLI invocation per request.
* Good, because the same five commands work unmodified against a self-hosted forge.
* Neutral, because `glab` lacks a `--web` flag on `issue list`/`mr list`, so those two cases construct the URL from `glab repo view -F json`'s `web_url` field and open it via `open`/`xdg-open` instead of a single CLI flag — one more code path to maintain than the GitHub side.
* Bad, because forge detection costs a network round-trip (`gh repo view`/`glab repo view`) on every invocation rather than being free.

## Pros and Cons of the Options

### Slash commands with inline execution

* Good, because the script runs the same way every time, with no LLM discretion in between.
* Good, because `allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/forge.sh *)` scopes exactly what can run.
* Neutral, because it requires a bundled shell script rather than pure prose.

### A skill

* Good, because no separate script file is needed.
* Bad, because it reintroduces per-request judgment for something that has only one correct behavior.

### Official MCP servers

* Good, because they'd avoid shelling out to `gh`/`glab` for read operations Claude already needs elsewhere.
* Bad, because they run against the remote API, not the local machine, so they can't open a browser tab — the actual ask for four of these five commands.

## More Information

`/pr` is the one command that shows output in the terminal (`gh pr view` / `glab mr view`) rather than opening a browser tab, since it's a status check, not a page to open — the request itself distinguished "open the X view" (issues, actions, PRs list, repo) from "show the current PR."
