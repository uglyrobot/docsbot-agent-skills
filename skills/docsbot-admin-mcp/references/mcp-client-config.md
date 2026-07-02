# MCP Client Configuration

## Generic Streamable HTTP MCP

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

## Codex Direct MCP

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

## Codex Plugin Marketplace

```bash
codex plugin marketplace add uglyrobot/docsbot-agent-tools
codex plugin add docsbot-mcp@docsbot
```

Then start a new Codex thread and ask Codex to use DocsBot Admin MCP.

## Claude Code And Other Agent Skills Clients

Copy or install the folder:

```text
skills/docsbot-admin-mcp/
```

into the client's skills directory. Then configure the MCP server using that client's remote MCP setup flow.
