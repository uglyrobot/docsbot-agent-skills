# DocsBot Agent Tools

Install DocsBot Admin MCP in Codex, Claude Code, and other MCP- or Agent Skills-compatible clients.

DocsBot Admin MCP is a hosted Streamable HTTP MCP server for authorized DocsBot dashboard administration:

```text
https://mcp.docsbot.ai
```

It exposes a compact two-tool interface:

- `search` discovers relevant DocsBot Admin API catalog operations.
- `execute` runs a selected catalog operation with structured parameters.

Authentication uses browser-based OAuth with Dynamic Client Registration. DocsBot evaluates dashboard permissions and RBAC live on every action.

## Install In Codex As A Plugin

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add uglyrobot/docsbot-agent-tools
codex plugin add docsbot-mcp@docsbot
```

Then start a new Codex thread and ask Codex to use DocsBot Admin MCP.

You can also browse it from Codex:

```text
codex
/plugins
```

Open the `DocsBot` marketplace tab and install `docsbot-mcp`.

## Install In Codex As Direct MCP

If you do not need the Codex plugin wrapper:

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

## Install As A Portable Agent Skill

This repository also includes an Agent Skills-compatible package:

```text
skills/docsbot-admin-mcp/
```

Use it with Claude Code or another skills-compatible agent by copying that folder into the client's skills directory, then configure the remote MCP server according to that client's MCP setup flow.

The skill follows the open Agent Skills `SKILL.md` layout:

```text
skills/docsbot-admin-mcp/
├── SKILL.md
├── assets/
└── references/
```

## Generic MCP Configuration

For clients that accept JSON MCP configuration:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

A copy is available at:

```text
mcp/docsbot-admin.mcp.json
```

## Repository Layout

```text
.agents/plugins/marketplace.json        # Codex marketplace catalog
plugins/docsbot-mcp/                    # Codex plugin package
skills/docsbot-admin-mcp/               # Portable Agent Skill package
mcp/docsbot-admin.mcp.json              # Generic MCP config example
clients/                                # Client-specific installation notes
scripts/                                # Convenience install scripts
```

## Docs

- DocsBot MCP server guide: https://docsbot.ai/documentation/developer/mcp-server
- DocsBot: https://docsbot.ai

## Client Notes

- [Codex](clients/codex.md)
- [Claude Code and Agent Skills clients](clients/agent-skills.md)
- [Generic MCP clients](clients/generic-mcp.md)

## Security

DocsBot Admin MCP acts as the authorized DocsBot user. Existing team roles, bot access, billing permissions, and dashboard RBAC remain the source of truth.

Review and revoke authorized MCP clients from **API & Integrations** in the DocsBot dashboard.
