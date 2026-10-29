# playwright

Microsoft's [Playwright MCP server](https://github.com/microsoft/playwright-mcp), registered twice:

- `playwright` opens a visible browser window, for watching or taking over an interaction.
- `playwright-headless` runs without a window, so it does not take focus while Claude browses, for example during scripted or timed runs.

The headless instance uses `--isolated`, which keeps its profile in memory. Both instances otherwise share the same persistent profile, and Chrome allows only one browser per profile at a time.
