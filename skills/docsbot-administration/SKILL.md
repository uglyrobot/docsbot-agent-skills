---
name: docsbot-administration
description: Use DocsBot Administration to administer DocsBot teams, bots, sources, members, integrations, Skills, reporting, and supported billing settings through an OAuth-authenticated remote MCP server. Activate when a user asks to manage DocsBot, inspect DocsBot account state, configure bots or sources, review dashboard data, or use the DocsBot Admin API through an agent.
license: MIT
compatibility: Requires an MCP-compatible agent or client with Streamable HTTP support and browser-based OAuth.
metadata:
  author: DocsBot
  version: "0.1.0"
  mcp_server_url: https://mcp.docsbot.ai
---

# DocsBot Administration

Use this skill when working with the hosted DocsBot Administration server:

```text
https://mcp.docsbot.ai
```

DocsBot Administration gives an authorized agent access to DocsBot dashboard administration through a compact two-tool MCP surface:

- `search` finds relevant DocsBot Admin API catalog operations, schemas, permission notes, response summaries, and side-effect levels.
- `execute` runs one selected catalog operation by `operationId` with structured `pathParams`, `query`, `body`, and optional `idempotencyKey`.

The server uses browser-based OAuth with Dynamic Client Registration. The token identifies the DocsBot user, and DocsBot evaluates team access, bot access, billing permissions, and role checks live on each action.

## Setup

If the MCP server is not already configured, add it to the client as a Streamable HTTP MCP server:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

For Codex, the direct MCP setup is:

```bash
codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot
```

For Codex plugin installation, use the marketplace package in this repository instead:

```bash
codex plugin marketplace add uglyrobot/docsbot-agent-skills
codex plugin add docsbot-administration@docsbot
```

## Workflow

1. Confirm the user wants to act in DocsBot and clarify the target team, bot, source, integration, report, member, or setting when needed.
2. Use `search` first. Search for the operation family or task, not a guessed URL.
3. Read the returned operation details, especially required fields, permission notes, and side-effect level.
4. Use `execute` only with a selected `operationId` and structured parameters.
5. For writes, destructive actions, member changes, source deletion, billing changes, or integration changes, summarize the intended action and ask for confirmation before execution unless the user's request already explicitly authorizes that exact action.
6. Report the result with IDs, names, and next steps that the user can verify in DocsBot.

## Constraints

- Do not call arbitrary DocsBot URLs. DocsBot Administration execution is limited to known catalog operations.
- Do not invent team IDs, bot IDs, source IDs, or operation IDs. Discover them with `search` and prior `execute` calls.
- Treat existing DocsBot dashboard RBAC as the source of truth. If an action is denied, report the denial rather than attempting to bypass it.
- Prefer idempotency keys for create/update operations when the operation supports them.
- Do not expose OAuth tokens, API keys, internal headers, or private response data beyond what the user needs for the task.

## References

- [DocsBot MCP server guide](references/mcp-server.md)
- [MCP client configuration examples](references/mcp-client-config.md)
