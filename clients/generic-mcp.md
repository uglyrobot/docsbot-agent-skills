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

## DocsBot Documentation Search

Use the per-bot Documentation server to search and fetch a specific bot's indexed sources:

```json
{
  "mcpServers": {
    "docsbot-docs": {
      "url": "https://api.docsbot.ai/teams/{teamId}/bots/{botId}/mcp/",
      "headers": {
        "Authorization": "Bearer <TOKEN>"
      }
    }
  }
}
```

Replace `{teamId}` and `{botId}` with the target DocsBot team and bot IDs. Replace `<TOKEN>` with a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`.

Agents should call `search` first, then call `fetch` with source IDs returned from search when exact source text, broader context, or citations are needed.

## DocsBot Question History

Use the per-bot Question History server to search and fetch prior questions, answers, and conversation history:

```json
{
  "mcpServers": {
    "docsbot-question-history": {
      "url": "https://api.docsbot.ai/teams/{teamId}/bots/{botId}/questions/mcp/",
      "headers": {
        "Authorization": "Bearer <TOKEN>"
      }
    }
  }
}
```

Replace `{teamId}` and `{botId}` with the target DocsBot team and bot IDs. Replace `<TOKEN>` with a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`.

Agents should call `search` first, then call `fetch` with question IDs returned from search when the full conversation or exact prior answer is needed.
