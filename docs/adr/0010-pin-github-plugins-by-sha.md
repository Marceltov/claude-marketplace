---
status: "accepted"
date: 2026-11-02
---

# GitHub-sourced plugins are pinned by sha, moved by a daily workflow

## Context and Problem Statement

The entries that point at another repository (engineering-conventions, trilium, paperless-ngx and six more) named only `repo`. An install made through claude.ai does not follow such an entry: engineering-conventions stayed at 0.4.2 there, with the Update button inactive, while the plugin was at 0.12.0. The CLI's `claude plugin update` reads the plugin repository and did update (0.5.2 → 0.12.0 on 2026-11-02). The marketplace itself had not changed since 2026-10-30, so nothing told claude.ai there was anything new. The official marketplace pins all 262 of its external entries by `sha`; an update there is a commit to the marketplace. Issue #38.

## Considered Options

1. **Pin by `sha`, moved by a workflow in this repository** when a plugin's `version` changes.
2. **Each plugin repository pushes its new `sha` here** on a version bump (repository dispatch).
3. **Move the plugins into this repository** (`./plugins/<name>`, as ccp, playwright and notefeed are).
4. **Leave it; update by hand** with the CLI or by reinstalling on claude.ai.

## Decision Outcome

Chosen: option 1. `scripts/pin_plugins.py` sets each GitHub entry's `source.sha` to the head of its branch (`source.ref`, else the default branch) when the `version` in that repository's `.claude-plugin/plugin.json` differs from the version at the pinned commit. `.github/workflows/pin-plugins.yml` runs it every hour at minute 17 (daily at 04:17 UTC until 2026-11-04, #40) and by hand, and commits the change to `main` as `CLAUDE-MARKETPLACE #38: Pin <names> to their new versions`. On a pull request it runs the tests and only reports.

Option 2 needs a token with write access here in every plugin repository, three of which are not Marcel's. Option 3 would end "nothing is forked or vendored" for the upstream plugins and split each plugin's history. Option 4 is what failed.

### Consequences

- Good, because a version bump in a plugin repository reaches every install, claude.ai's included, within a day; a commit without a bump does not, as the engineering-conventions rule "bump `version`, so installed plugins update" intends.
- Good, because what an install gets is a named commit, the same for everyone.
- Bad, because an update waits up to a day; run the workflow by hand to ship at once.
- Bad, because a plugin without a `version` is pinned once and never moved (the script warns).
- Neutral: `git-subdir` and `url` entries are left as they are; the `url` entry (superdesign) is pinned by hand already.

### Confirmation

`python3 -m unittest discover -s scripts` passes; a second run of the script on a pinned file says `unchanged`; `claude plugin validate .` passes. After the first pin reaches `main`, claude.ai offers the update for engineering-conventions (0.4.2 → 0.12.0).
