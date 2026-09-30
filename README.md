# DocsBot Agent Skills

Install DocsBot skills and plugins in Cursor, Codex, Claude (chat, Cowork, and Claude Code), Grok Build, and other MCP- or Agent Skills-compatible clients.

DocsBot Administration is a hosted Streamable HTTP MCP server for authorized DocsBot dashboard administration. Its package at `plugins/docsbot-administration/` follows the portable [Agent Plugins v1](https://agent-plugins.org/) layout with a root `plugin.json`, `mcp.json`, and bundled workflow skill. Cursor and Codex also have client-specific marketplace manifests. The same package includes Claude’s `.claude-plugin/plugin.json` and `.mcp.json` layout, which Grok Build also supports. See the [client notes](#client-notes) for each installation surface.

```text
https://mcp.docsbot.ai
```

This package requires the Admin server with fixed named action tools. If MCP `tools/list` still advertises the old Admin `search`/`execute` dispatcher, complete the server and plugin migration before using this workflow. Optional `list_tool_categories`, `search_tools`, and `get_tool_schema` inspect advertised metadata.

Authentication uses browser-based OAuth with Dynamic Client Registration. DocsBot evaluates dashboard permissions and RBAC live on every action.

## Agent Plugins v1

Agent Plugins-compatible clients can load this directory as one portable package:

```text
plugins/docsbot-administration/
```

The root `plugin.json` declares the Agent Plugins v1 manifest and the root `mcp.json` declares the DocsBot remote MCP server as `streamable-http`. OAuth discovery and credential storage remain client-managed, so the package contains no credentials.

## Install In Cursor As A Plugin

After DocsBot Administration is approved and listed in the Cursor Marketplace, open a Cursor agent chat and run:

```text
/add-plugin docsbot-administration
```

The Cursor-specific `.cursor-plugin/plugin.json` package bundles the DocsBot Administration skill and native remote MCP configuration. Cursor opens the DocsBot OAuth flow when it connects.

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

## Install In Claude Code As A Plugin

Add this repository as a Claude Code plugin marketplace, then install DocsBot Administration:

```text
/plugin marketplace add uglyrobot/docsbot-agent-skills
/plugin install docsbot-administration@docsbot-plugins
```

Run `/reload-plugins` to activate it in the current session. Then run `/mcp`, select `docsbot`, and complete the browser-based DocsBot OAuth flow. Claude Code stores and refreshes the OAuth credentials through its normal MCP authentication flow.

Claude uses the shared `.claude-plugin/plugin.json`, root `skills/`, and `.mcp.json` package. For Claude chat and Cowork, install through **Customize → Plugins → Add**, then connect DocsBot from the plugin’s **Connectors** tab. See [Claude installation](clients/claude.md) for upload, marketplace, and direct connector options. This does not imply an Anthropic directory listing. [Official package reference](https://claude.com/docs/plugins/build).

## Install In Grok Build

Grok Build reads the Claude-compatible package; it does not need a separate Grok manifest. Review the package before explicitly trusting it:

```bash
grok plugin marketplace add uglyrobot/docsbot-agent-skills
grok plugin install docsbot-administration --trust
```

See [Grok installation](clients/grok.md) for direct MCP, consumer Grok connectors, and the separate xAI API setup. [Official Grok Build compatibility](https://docs.x.ai/build/features/skills-plugins-marketplaces).

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
| `docsbot-administration` | Administer DocsBot teams, bots, sources, members, integrations, Skills, reporting, and read-only account usage. |
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
.claude-plugin/marketplace.json         # Claude Code marketplace catalog
.cursor-plugin/marketplace.json         # Cursor Marketplace catalog
plugins/docsbot-administration/         # Shared plugin package root
plugins/docsbot-administration/plugin.json # Portable Agent Plugins v1 manifest
plugins/docsbot-administration/mcp.json # Portable Agent Plugins v1 MCP configuration
plugins/docsbot-administration/.codex-plugin/ # Codex-specific metadata
plugins/docsbot-administration/.claude-plugin/ # Claude Code-specific metadata
plugins/docsbot-administration/.cursor-plugin/ # Cursor-specific metadata and MCP config
plugins/docsbot-administration/skills/  # Bundled plugin workflow instructions
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
- [Cursor](clients/cursor.md)
- [Claude chat, Cowork, and Claude Code](clients/claude.md)
- [Grok Build, Grok connectors, and xAI API](clients/grok.md)
- [Portable Agent Skills clients](clients/agent-skills.md)
- [Generic MCP clients](clients/generic-mcp.md)

## Updating Existing Installations

The Admin endpoint is moving from its old `search`/`execute` dispatcher to fixed named action tools. Old Admin dispatcher calls fail against the new server. Update the plugin or skill, refresh the client’s advertised MCP tools, and start a new session if it keeps a cached tool list. The per-bot Documentation Search and Question History endpoints still use `search` and `fetch`.

## Package Maintenance

Run `python3 scripts/build-admin-release.py` before packaging. It validates client manifests and canonical/bundled skill-reference parity; CI runs the same validation. Add `--output /tmp/docsbot-administration.zip` to build the complete plugin ZIP after validation.

## Security

Hosted Admin MCP tools use stable names such as `list_teams`, `list_bots`, `get_bot`, `list_sources`, and `get_source`. Agents call these directly with the named tool's `pathParams`, `query`, and/or `body`; optional `list_tool_categories`, `search_tools`, and `get_tool_schema` inspect metadata only. Hosted tool changes are scanned automatically after publication: new tools and changed metadata can be held for review, while approved definitions remain available. Keep updates additive and backward compatible. Changes to plugin skills, configuration, or listing metadata require a new complete ZIP. Subscription and commerce mutations are outside this plugin; account usage reads remain available through advertised tools.

DocsBot Administration acts as the authorized DocsBot user. Existing team roles, bot access, billing permissions, and dashboard RBAC remain the source of truth.

Review and revoke authorized MCP clients from **API & Integrations** in the DocsBot dashboard.
