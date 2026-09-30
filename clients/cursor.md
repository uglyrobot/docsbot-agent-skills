# Cursor Installation

Cursor supports both the root Agent Plugins v1 manifest and the `.cursor-plugin/plugin.json` format included in this package. [Official formats reference](https://prod.cursor.com/docs/reference/plugins).

## Plugin Marketplace

Official listing review is pending. After the DocsBot Administration package is approved and listed in the Cursor Marketplace, install it from a Cursor agent chat:

```text
/add-plugin docsbot-administration
```

To install from this repository before an official listing, open **Customize → From GitHub Repository** and provide `https://github.com/uglyrobot/docsbot-agent-skills`; Cursor reads the repository’s `.cursor-plugin/marketplace.json`. Install DocsBot Administration from that marketplace. [Official repository import](https://prod.cursor.com/docs/skills).

The Cursor plugin bundles the DocsBot Administration skill and the remote Admin MCP configuration. Complete the browser-based DocsBot OAuth flow when Cursor prompts you to authenticate.

## Direct MCP

If you only need the remote Admin MCP server, add this configuration in Cursor instead:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

Cursor opens the DocsBot OAuth flow when it connects to the server. No DocsBot API key is required.

## Portable Skills And Cloud Agents

Cursor discovers project skills from `.agents/skills/`; see [portable installation](agent-skills.md) and [Cursor skills documentation](https://prod.cursor.com/docs/skills). A local project skill installation does not automatically make the skill available to Cloud Agents. For personal cloud skills, install into `~/.cursor/skills/` and enable **Settings → Agents → Context and Tools → Sync Skills for Cloud Agents**, subject to team policy. Only that personal directory syncs. Verify the cloud agent’s MCP connection separately.

This package requires fixed named Admin tools. If MCP `tools/list` still shows the old Admin `search`/`execute` dispatcher, complete the server and plugin migration before using the updated workflow. Update the package and refresh MCP tools or start a new session.
