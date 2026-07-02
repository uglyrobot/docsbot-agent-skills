---
name: docsbot-documentation-search
description: Search and fetch a DocsBot bot's indexed documentation, knowledge base, and training sources through a per-bot remote MCP server. Activate when a user asks to use an agent to answer from, inspect, retrieve, or cite content already indexed in a specific DocsBot bot.
license: MIT
compatibility: Requires an MCP-compatible agent or client with Streamable HTTP support and Bearer-token authentication.
metadata:
  author: DocsBot
  version: "0.1.0"
  mcp_server_url_template: https://api.docsbot.ai/teams/{teamId}/bots/{botId}/mcp/
---

# DocsBot Documentation Search

Use this skill when working with a specific DocsBot bot's indexed training data through the per-bot Documentation server:

```text
https://api.docsbot.ai/teams/{teamId}/bots/{botId}/mcp/
```

This server gives an authorized agent a focused read-only retrieval surface over the bot's indexed sources:

- `search` runs hybrid semantic and keyword search across the bot's indexed documentation, website pages, help center articles, files, and other training sources.
- `fetch` retrieves the full source content for an ID returned by `search` when full-document retrieval is available for that source.

## Setup

Configure the MCP server with the DocsBot team ID, bot ID, and a Bearer token:

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

The token can be a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`. Documentation search is available on Standard plans and above.

## Workflow

1. Identify the target DocsBot team and bot before searching.
2. Use `search` first with the user's natural-language query or a concise keyword query.
3. If the bot uses retriever tags, pass `tags` and `include_untagged` only when the user or task clearly calls for a scoped search.
4. Use `fetch` for source IDs returned by `search` when the task needs exact source text, broader context, or citations.
5. Answer from retrieved content and mention gaps when the indexed sources do not contain enough evidence.

## Constraints

- Do not use this skill for DocsBot account administration; use DocsBot Administration for teams, bots, sources, settings, members, integrations, or billing.
- Do not invent team IDs, bot IDs, source IDs, tags, or source content.
- Treat `fetch` failures on older sources as a data freshness issue; the source may need to be refreshed in DocsBot before full-document retrieval is available.
- Do not expose API keys, OAuth tokens, or private indexed content beyond what is necessary for the user's task.
- Successful `search` and `fetch` calls consume DocsBot AI Credits.

## References

- [MCP client configuration](references/mcp-client-config.md)
