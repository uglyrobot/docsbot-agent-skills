# Codex Installation

## Plugin Marketplace

Install the DocsBot marketplace:

```bash
codex plugin marketplace add uglyrobot/docsbot-agent-tools
codex plugin add docsbot-mcp@docsbot
```

Then start a new Codex thread and ask Codex to use DocsBot Admin MCP.

You can also browse the marketplace from the TUI:

```text
codex
/plugins
```

Open the `DocsBot` marketplace tab and install `docsbot-mcp`.

## Direct MCP

If you only want the remote MCP server and not the plugin card/marketplace packaging:

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

Start a new thread after install or login so Codex loads the server.
