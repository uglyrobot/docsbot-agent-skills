# Generic MCP Clients

DocsBot Administration is a hosted Streamable HTTP MCP server:

```text
https://mcp.docsbot.ai
```

Use this configuration shape for clients that accept JSON MCP config:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

The server advertises OAuth discovery metadata and Dynamic Client Registration:

```text
https://mcp.docsbot.ai/.well-known/oauth-protected-resource
https://mcp.docsbot.ai/.well-known/oauth-authorization-server
https://mcp.docsbot.ai/oauth/register
```

After authentication, agents should call `search` first to discover the relevant Admin API operation, then call `execute` with the selected `operationId` and structured parameters.
