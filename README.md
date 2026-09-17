# marceltov — Claude Code plugin marketplace

A curated marketplace of the Claude Code plugins I actually use every day.

Every entry points at its upstream repository — nothing is vendored or forked here. This repo is just the index.

## Install

```bash
/plugin marketplace add Marceltov/claude-marketplace
```

Then install what you want:

```bash
/plugin install superpowers@marceltov
/plugin install context7@marceltov
/plugin install frontend-design@marceltov
/plugin install ponytail@marceltov
/plugin install i-have-adhd@marceltov
/plugin install notfair@marceltov
```

Or browse interactively with `/plugin`.

## Plugins

| Plugin | What it does | Upstream |
| --- | --- | --- |
| `superpowers` | Brainstorming, subagent-driven development, systematic debugging, red/green TDD, and skill authoring. | [obra/superpowers](https://github.com/obra/superpowers) |
| `context7` | MCP server that pulls version-specific library docs straight from source repos into context. | [Upstash Context7](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/context7) |
| `frontend-design` | Production-grade frontend interfaces that avoid generic AI aesthetics. | [Anthropic](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) |
| `ponytail` | Lazy senior dev mode: YAGNI, stdlib first, no unrequested abstractions. | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| `i-have-adhd` | ADHD-friendly output: next action first, numbered steps, no tangents. | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) |
| `notfair` | Ads, analytics, SEO and GEO workflows (Google/Meta/TikTok Ads, GA4, Search Console, WordPress). | [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) |

> The plugin upstream calls itself `notfair`, not `not-fair` — plugin names must match the upstream `plugin.json`, so that is the name used here.

## Updating

Plugins track their upstream default branch, so they are not pinned to a commit. To pull the latest versions:

```bash
/plugin marketplace update marceltov
/plugin update
```

To freeze a plugin instead, add a 40-character `sha` (and optionally a `ref`) to its `source` object in `.claude-plugin/marketplace.json`.

## Adding a plugin

Append an entry to the `plugins` array in `.claude-plugin/marketplace.json`. The `name` must match the `name` in the upstream plugin's `.claude-plugin/plugin.json`.

Source shapes used here:

```jsonc
// plugin at the root of its own repo
{ "source": "github", "repo": "owner/repo" }

// plugin in a subdirectory of a monorepo
{ "source": "git-subdir", "url": "https://github.com/owner/repo.git", "path": "plugins/thing", "ref": "main" }
```

Validate before committing:

```bash
claude plugin validate .
```

## License

MIT — see [LICENSE](LICENSE). The plugins themselves are licensed by their respective upstream authors.
