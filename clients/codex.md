# Codex Installation

## Plugin Marketplace

Install the DocsBot marketplace:

```bash
codex plugin marketplace add uglyrobot/docsbot-agent-skills
codex plugin add docsbot-administration@docsbot
```

Then start a new Codex thread and ask Codex to use DocsBot Administration.

The plugin bundles a DocsBot Administration skill so Codex has the standard workflow instructions after install: resolve the working team, resolve the working bot, use Admin MCP `search` before `execute`, and confirm destructive or access-changing writes.

You can also browse the marketplace from the TUI:

```text
codex
/plugins
```

Open the `DocsBot` marketplace tab and install `docsbot-administration`.

## Direct MCP

If you only want the remote MCP server and not the plugin card/marketplace packaging:

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

Start a new thread after install or login so Codex loads the server.
