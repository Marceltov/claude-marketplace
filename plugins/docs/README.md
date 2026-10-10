# docs

One skill, `docs-site`: a documentation site for a project with [MkDocs](https://www.mkdocs.org/) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme, published with GitHub Pages, in the colours and the typeface of the app it documents.

```bash
/plugin install docs@marceltov
```

Then, in a repository: "set up the docs", "write the documentation site", "add a page about X to the docs". The skill reads the app's CSS tokens for the palette, writes `mkdocs.yml`, `docs/stylesheets/extra.css`, `requirements-docs.txt` and `.github/workflows/docs.yml`, lays out the pages, builds with `mkdocs build --strict` before anything is committed, and turns on Pages for the repository.

- `skills/docs-site/SKILL.md`: the procedure and the writing rules.
- `skills/docs-site/templates/`: the files it starts from.
- `scripts/palette.py`: the Material palette from two accent colours.
