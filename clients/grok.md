# Grok Installation

Grok Build, consumer Grok connectors, and the xAI API have separate installation and authorization flows. After setup, verify the DocsBot connection in the client you intend to use.

## Grok Build

Grok Build supports Claude Code marketplaces, plugins, skills, and MCP configuration. Reuse the package’s `.claude-plugin/plugin.json`, root `skills/`, and `.mcp.json`; a separate Grok manifest is unnecessary. [Official compatibility documentation](https://docs.x.ai/build/features/skills-plugins-marketplaces).

Review this repository and its package before using the explicit trust option:

```bash
grok plugin marketplace add uglyrobot/docsbot-agent-skills
grok plugin install docsbot-administration --trust
```

The commands follow xAI’s [official plugin CLI guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md). They install from the configured repository marketplace and do not imply an official marketplace listing.

For direct MCP instead of the bundled plugin:

```bash
grok mcp add --transport http docsbot https://mcp.docsbot.ai
grok mcp doctor docsbot
```

Grok Build supports browser OAuth for remote servers. Authenticate when prompted or use the `/mcps` panel. [Official MCP setup](https://docs.x.ai/build/features/mcp-servers).

## Consumer Grok

Use [Grok Connectors](https://grok.com/connectors) to add a custom MCP connector for `https://mcp.docsbot.ai`, subject to your account’s connector access. Business and Enterprise administrators provision organization connectors. This is a connector setup; there is no claim that consumer Grok installs this skill or plugin ZIP. [Official connector documentation](https://docs.x.ai/grok/connectors).

## xAI API

Configure the remote MCP server in the request’s tool configuration, with its `server_url` and an application-supplied `authorization` token. The application must obtain, securely store, and refresh authorization; the API request does not promise browser OAuth discovery or Dynamic Client Registration. [Official remote MCP API documentation](https://docs.x.ai/developers/tools/remote-mcp).

## Updating The Admin Tools

This package requires fixed named Admin actions. If MCP `tools/list` still shows the old Admin `search`/`execute` dispatcher, complete the server and plugin migration before using the updated workflow. Update plugin/skill instructions, refresh advertised MCP tools, and start a new session if needed. Old dispatcher calls fail once the new server is deployed. Per-bot Documentation Search and Question History continue to use `search`/`fetch`.
