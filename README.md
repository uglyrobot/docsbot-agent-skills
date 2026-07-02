# DocsBot Agent Skills

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
codex plugin marketplace add uglyrobot/docsbot-agent-skills
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

### CLI Install

Use the common `npx skills` installer:

```bash
# Install all skills in this repo
npx skills add uglyrobot/docsbot-agent-skills

# Install only the DocsBot Admin MCP skill
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-admin-mcp

# List available skills
npx skills add uglyrobot/docsbot-agent-skills --list
```

This installs into `.agents/skills/` and, for Claude Code compatibility, symlinks into `.claude/skills/` when supported by the installer.

### SkillKit Install

For multi-agent installs across clients such as Claude Code, Cursor, Copilot, and other skills-aware agents:

```bash
# Install all skills in this repo
npx skillkit install uglyrobot/docsbot-agent-skills

# Install only the DocsBot Admin MCP skill
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-admin-mcp

# List available skills
npx skillkit install uglyrobot/docsbot-agent-skills --list
```

### Manual Install

Clone the repo and copy the skill folder:

```bash
git clone https://github.com/uglyrobot/docsbot-agent-skills.git
cp -R docsbot-agent-skills/skills/docsbot-admin-mcp .agents/skills/
```

Then configure the remote MCP server according to your client's MCP setup flow.

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
skills.json                             # Skill catalog for installers and humans
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
