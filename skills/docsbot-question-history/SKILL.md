---
name: docsbot-question-history
description: Search and fetch prior DocsBot bot questions, answers, and conversation history through a per-bot remote MCP server. Activate when a user asks to analyze support history, find past answers, review escalations, inspect unresolved questions, or reuse previous DocsBot conversations.
license: MIT
compatibility: Requires an MCP-compatible agent or client with Streamable HTTP support and Bearer-token authentication.
metadata:
  author: DocsBot
  version: "0.1.0"
  mcp_server_url_template: https://api.docsbot.ai/teams/{teamId}/bots/{botId}/questions/mcp/
---

# DocsBot Question History

Use this skill when working with a specific DocsBot bot's historical question and answer data through the per-bot Question History server:

```text
https://api.docsbot.ai/teams/{teamId}/bots/{botId}/questions/mcp/
```

This server gives an authorized agent a focused read-only retrieval surface over prior bot conversations:

- `search` runs semantic search across logged questions, answers, and conversation history.
- `fetch` retrieves a full question or conversation by ID returned from `search`.

Search results can include operational metadata such as whether the bot could answer, escalation state, resolved state, sentiment, and topic when that data is available.

## Setup

Configure the MCP server with the DocsBot team ID, bot ID, and a Bearer token:

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

The token can be a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`. Question History search requires a bot with at least 5,000 logged questions.

## Workflow

1. Identify the target DocsBot team and bot before searching.
2. Use `search` first with the user's natural-language query, support topic, customer issue, escalation phrase, or answer pattern.
3. Review result metadata such as `couldAnswer`, `escalation`, `resolved`, `escalated`, `sentiment`, and `topic` when present.
4. Use `fetch` for question IDs returned by `search` when the task needs the full conversation or exact answer history.
5. Summarize patterns, cite relevant prior answers, and call out limits when history is sparse or unavailable.

## Constraints

- Do not use this skill for DocsBot account administration; use DocsBot Administration for teams, bots, sources, settings, members, integrations, or billing.
- Do not invent team IDs, bot IDs, question IDs, conversation history, or support outcomes.
- Respect the privacy of logged questions and conversations. Do not expose more customer data than the user needs for the task.
- If the bot has fewer than 5,000 logged questions, report that Question History search is not available for that bot yet.
- Successful `search` and `fetch` calls consume DocsBot AI Credits.

## References

- [MCP client configuration](references/mcp-client-config.md)
