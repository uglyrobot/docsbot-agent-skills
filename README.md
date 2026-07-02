# DocsBot Agent Skills

Install DocsBot skills in Codex, Claude Code, and other MCP- or Agent Skills-compatible clients.

DocsBot Administration is a hosted Streamable HTTP MCP server for authorized DocsBot dashboard administration:

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
codex plugin add docsbot-administration@docsbot
```

Then start a new Codex thread and ask Codex to use DocsBot Administration.

You can also browse it from Codex:

```text
codex
/plugins
```

Open the `DocsBot` marketplace tab and install `docsbot-administration`.

## Install In Codex As Direct MCP

If you do not need the Codex plugin wrapper:

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

## Install As Portable Agent Skills

This repository also includes Agent Skills-compatible packages:

```text
skills/docsbot-administration/
skills/docsbot-documentation-search/
skills/docsbot-question-history/
```

Available skills:

| Skill | Use |
| --- | --- |
| `docsbot-administration` | Administer DocsBot teams, bots, sources, members, integrations, Skills, reporting, and supported billing settings. |
| `docsbot-documentation-search` | Search and fetch indexed documentation, website, help center, file, and knowledge base content from a specific DocsBot bot. |
| `docsbot-question-history` | Search and fetch prior DocsBot questions, answers, conversations, escalation state, sentiment, and support history for a specific bot. |

### CLI Install

Use the common `npx skills` installer:

```bash
# Install all skills in this repo
npx skills add uglyrobot/docsbot-agent-skills

# Install only the DocsBot Administration skill
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-administration

# Install only the DocsBot Documentation Search skill
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search

# Install only the DocsBot Question History skill
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-question-history

# List available skills
npx skills add uglyrobot/docsbot-agent-skills --list
```

This installs into `.agents/skills/` and, for Claude Code compatibility, symlinks into `.claude/skills/` when supported by the installer.

### SkillKit Install

For multi-agent installs across clients such as Claude Code, Cursor, Copilot, and other skills-aware agents:

```bash
# Install all skills in this repo
npx skillkit install uglyrobot/docsbot-agent-skills

# Install only the DocsBot Administration skill
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-administration

# Install only the DocsBot Documentation Search skill
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search

# Install only the DocsBot Question History skill
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-question-history

# List available skills
npx skillkit install uglyrobot/docsbot-agent-skills --list
```

### Manual Install

Clone the repo and copy the skill folder you want:

```bash
git clone https://github.com/uglyrobot/docsbot-agent-skills.git
cp -R docsbot-agent-skills/skills/docsbot-administration .agents/skills/
cp -R docsbot-agent-skills/skills/docsbot-documentation-search .agents/skills/
cp -R docsbot-agent-skills/skills/docsbot-question-history .agents/skills/
```

Then configure the remote MCP server according to your client's MCP setup flow.

The skill follows the open Agent Skills `SKILL.md` layout:

```text
skills/<skill-name>/
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
mcp/docsbot-administration.mcp.json
mcp/docsbot-documentation-search.mcp.json
mcp/docsbot-question-history.mcp.json
```

## Repository Layout

```text
.agents/plugins/marketplace.json        # Codex marketplace catalog
plugins/docsbot-administration/         # Codex plugin package
skills/                                 # Portable Agent Skill packages
mcp/                                    # Generic MCP config examples
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

DocsBot Administration acts as the authorized DocsBot user. Existing team roles, bot access, billing permissions, and dashboard RBAC remain the source of truth.

Review and revoke authorized MCP clients from **API & Integrations** in the DocsBot dashboard.
