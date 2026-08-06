# Cursor Installation

## Plugin Marketplace

After the DocsBot Administration package is approved and listed in the Cursor Marketplace, install it from a Cursor agent chat:

```text
/add-plugin docsbot-administration
```

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
