# Claude Installation

The plugin package at `plugins/docsbot-administration/` contains `.claude-plugin/plugin.json`, root `skills/`, and a remote server in `.mcp.json`. Claude chat, Cowork, and Claude Code use this shared layout. Availability in Anthropic’s directory depends on listing approval.

## Claude Chat And Cowork

Open **Customize → Plugins → Add**. Upload the complete plugin ZIP, or choose **Add marketplace** with this repository URL:

```text
https://github.com/uglyrobot/docsbot-agent-skills
```

After installing DocsBot Administration, open its **Connectors** tab and add or connect DocsBot. Sign in with your DocsBot account. On Team and Enterprise, an Owner provisions the connector before members connect their accounts. [Official plugin structure and installation](https://claude.com/docs/plugins/build), [support by app](https://claude.com/docs/plugins/platform-support).

For a direct remote connector without the plugin’s workflow skill, use **Settings → Connectors** and add `https://mcp.docsbot.ai`. Remote connectors use this UI rather than `claude_desktop_config.json`. [Official remote connector setup](https://support.claude.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers).

## Claude Code

```text
/plugin marketplace add uglyrobot/docsbot-agent-skills
/plugin install docsbot-administration@docsbot-plugins
/reload-plugins
```

Run `/mcp`, select `docsbot`, and authenticate. Claude Code connects to the bundled server directly. [Official Claude Code plugin installation](https://code.claude.com/docs/en/discover-plugins).

For portable skills alone, follow [Agent Skills installation](agent-skills.md) and configure MCP separately.

## Updating The Admin Tools

This package requires fixed named Admin tools. If MCP `tools/list` still shows the old Admin `search`/`execute` dispatcher, complete the server and plugin migration before using the updated workflow. Update the installed package, refresh MCP tools, and start a new session if needed; old dispatcher calls fail once the new server is deployed. Per-bot documentation and question-history `search`/`fetch` tools are unchanged.
