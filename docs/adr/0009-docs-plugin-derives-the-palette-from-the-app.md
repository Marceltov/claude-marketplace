---
status: accepted
date: 2026-10-10
decision-makers: Marcel Bruckner
---

# The docs plugin builds every site the same way and takes its colours from the app

## Context and Problem Statement

notefeed's documentation site (MkDocs, Material, GitHub Pages, a palette in the app's colours) was set up by hand and worked well. noticebox needs the same, and so will the next tool. Setting it up again each time, from memory, would drift: a different theme feature here, a different workflow there, colours chosen anew. Issue #22.

## Considered Options

* A **`docs` plugin with a `docs-site` skill** holding the procedure, the templates and a script that derives the Material palette from the app's own CSS tokens. Chosen.
* A **template repository** to copy from. Rejected: it carries no procedure for extending an existing site, and the colours would still be picked by hand.
* **Nothing:** set each site up by hand. Rejected: drift.

## Decision Outcome

Chosen option: the plugin. Every site is MkDocs with Material, built with `--strict`, deployed by the same Pages workflow, and the palette is computed from two accent colours read from the app's stylesheet, so the docs of a tool look like the tool without anyone choosing colours twice.

### Consequences

* Good, because a new tool's docs are one skill invocation away and look like the tool from the first build.
* Good, because the writing rules (reader's path, one page per thing a person does, settings in tables, docs change with the behaviour) travel with the procedure.
* Bad, because a project whose app has no accent colour or no dark scheme gets a palette that is only an approximation; the skill says what to pass then.
