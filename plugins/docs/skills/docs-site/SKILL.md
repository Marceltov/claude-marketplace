---
description: Set up or extend a project's documentation site with MkDocs and the Material theme, in the app's own colours and typeface, published with GitHub Pages. Use when asked to "set up the docs", "write the documentation", "add a docs site", "add a page to the docs", or when a project with a README and no docs/ folder is about to be released.
---

# docs-site: a documentation site in the app's own colours

The site is MkDocs with Material, built with `--strict` in CI and deployed by GitHub Pages. It looks like the app it documents: the palette comes from the app's CSS tokens, the typeface from the app's font. Everything is a file in the repository; nothing is configured by clicking.

Templates: `templates/` next to this file. Palette: `../../scripts/palette.py`.

## 0. Does the site exist?

`ls mkdocs.yml docs/`. If both exist, skip to step 5 and work inside the existing structure: add or change pages, keep the nav in `mkdocs.yml` in step with them, and build before committing. Never rewrite an existing site's configuration to match the template.

## 1. The app's colours and typeface

Read the app's stylesheet (`app/globals.css`, `src/index.css`, a Tailwind `@theme`) and take:

- the **accent** on a light background and on a dark one: the colour of links, the primary button, the active nav item. Often named `--accent`, `--primary`, `--brand`.
- the **dark page background**, if the app has a dark scheme.
- the **font family** the app sets on `body`.

Make the palette block:

```sh
python3 <plugin>/scripts/palette.py --light '#176b5c' --dark '#7fcdb6' --dark-bg '#15181b' --note "noticebox's green"
```

If the app has one accent only, pass it as both and let the script lighten nothing: Material's dark scheme needs a colour that reads on dark, so prefer a lighter tint of the same hue for `--dark`. If the font is on Google Fonts, name it under `theme.font` in `mkdocs.yml`; if it is vendored or private, delete `theme.font` and let Material use its default rather than loading something that is not the app's.

## 2. The files

Copy from `templates/` and fill in:

| File | What to set |
|---|---|
| `mkdocs.yml` | `site_name`, `site_description` (one sentence), `site_url` (`https://<owner>.github.io/<repo>/` unless a domain exists), `repo_url`, `repo_name`, the fonts, the `nav` |
| `docs/stylesheets/extra.css` | the palette block from step 1 on top of the template |
| `docs/assets/icon.svg` | the app's icon; a 20 to 24 px mark on a transparent background. Without one, remove `logo` and `favicon` from `mkdocs.yml` |
| `requirements-docs.txt` | as the template; bump the pin when Dependabot does |
| `.github/workflows/docs.yml` | as the template |
| `docs/index.md` | from the template |

Exclude from the site what is in `docs/` for other reasons (`adr/`, `agents/`, working notes) with `exclude_docs`.

## 3. The pages

The structure is the reader's path, not the code's:

- **Home** says what the app is in two paragraphs and a picture, then where to go.
- **Get started**: `quick-start.md` runs the app in the shortest way (Docker Compose where it exists) and ends with the first useful thing done; `concepts.md` defines the words the rest of the docs use.
- **Using**: one page per thing a person does, named by the doing ("Posting notes", "Deciding a report").
- **Integrations**: how other software talks to the app: HTTP endpoints, client libraries, MCP, webhooks.
- **Self-hosting**: `configuration.md` with every setting in one table (name, default, meaning), then one page per operator concern: access and login, reverse proxy, storage, backups, retention, notifications, metrics, logs, upgrading.

A page starts with a sentence that says what the page answers. Settings go in a table whose first column is the name in code. Commands and configuration go in fenced blocks with the language set. Admonitions are for warnings and for "if you run X, note Y", not for emphasis. Screenshots are `docs/assets/screenshot-<name>-light.png` and `-dark.png`, shown with `#only-light` and `#only-dark`, taken from the real app at a width around 1200 px; a single screenshot without a dark variant is shown plainly. Write from the reader's side: what they do and what happens, in the same words the app's UI uses. No "simply", no "just", no marketing.

Every page in `docs/` that is not excluded must be in the `nav`, and every nav entry must exist: `--strict` fails otherwise.

## 4. Build before committing

```sh
uv venv .venv-docs && . .venv-docs/bin/activate && uv pip install -r requirements-docs.txt && mkdocs build --strict
```

(or `python3 -m venv` and `pip`). Fix every warning: a broken link, a page outside the nav, an anchor that does not exist. Add `.venv-docs/` and `site/` to `.gitignore`.

## 5. Publishing

- `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow` turns Pages on for the repository, once; a 409 means it already is.
- The workflow deploys on every push to `main` that touches the docs, and only builds on pull requests.
- With a domain: `docs/CNAME` with the host name, a CNAME record to `<owner>.github.io`, and `site_url` set to it.
- Link the site from the README's first paragraph.

## 6. Keeping it true

Docs change in the same pull request as the behaviour they describe. When a setting, an endpoint, a state or a page of the UI changes, the page that names it changes too, and the quick start is run once more if it is touched.
