---
name: docsbot-administration
description: Use DocsBot Administration to administer DocsBot teams, bots, sources, members, integrations, Skills, reporting, and supported billing settings through an OAuth-authenticated remote MCP server. Activate when a user asks to manage DocsBot, inspect DocsBot account state, configure bots or sources, review dashboard data, or use the DocsBot Admin API through an agent.
license: MIT
compatibility: Requires an MCP-compatible agent or client with Streamable HTTP support and browser-based OAuth.
metadata:
  author: DocsBot
  version: "0.2.0"
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

1. Establish the working team before any team-scoped action.
2. Establish the working bot before any bot-scoped action.
3. Use `search` first. Search for the operation family or task, not a guessed URL.
4. Read the returned operation details, especially required fields, permission notes, response summaries, and side-effect level.
5. Use `execute` only with a selected `operationId` and structured parameters.
6. Keep useful IDs from results in thread context: team ID/name, bot ID/name, source IDs, member emails, integration IDs, and pagination state.
7. For writes, destructive actions, member changes, source deletion, billing changes, or integration changes, summarize the intended action and ask for confirmation before execution unless the user's request already explicitly authorizes that exact action.
8. Report the result with IDs, names, and next steps that the user can verify in DocsBot.

## Bot Builder Subworkflow

When the user asks to create, configure, tune, test, or hand off a new DocsBot bot, load the dedicated [bot-builder subworkflow](references/bot-builder/SKILL.md) before making MCP writes.

That subworkflow is part of DocsBot Administration, but it is intentionally kept as a nested reference tree because production bot creation has its own discovery, branding, source-selection, prompt, deployment, action, evaluation, and handoff rubric. Follow its reference chain from `references/bot-builder/` for bot-building tasks instead of merging those rules into this general administration workflow.

## Team Detection

The Admin MCP token identifies the authorized DocsBot user. It does not contain a fixed team ID or role snapshot, and DocsBot checks current team access and permissions live on each call.

When the user does not provide a team ID:

1. Search for the list-teams operation with a query like `list teams`.
2. Execute the list-teams operation.
3. If exactly one team is returned, use it as the working team and state its name.
4. If multiple teams are returned, choose only when the user's wording clearly matches a team name, domain, customer, or prior thread context.
5. If multiple teams remain plausible, ask the user which team to use and show the shortest useful choices: team name, team ID, plan, and bot count when available.

If a user says "current team", "my team", or "the active team", do not assume the dashboard session's internal `currentTeam` is available through MCP. Resolve the working team from explicit context or by listing teams.

## Bot And Source Lookup

For bot-scoped work, ensure a working team is selected, search for `list bots`, execute the list-bots operation, then match by exact bot ID first and bot name second. If the bot is ambiguous, ask the user to choose.

For source-scoped work, ensure working team and bot are selected, search for `list sources`, and use pagination or supported filters instead of fetching every source. Match source IDs directly when provided; otherwise match by URL, title, type, status, or tags. Fetch the full source only when list results are insufficient.

Use tag operations when the task mentions source tags, retriever tags, targeted retrieval, or tagged documentation. Bot `retrieverTags` define the allowed tag vocabulary, and source tags must match that vocabulary.

## Common Search Queries

Use short catalog searches that describe the operation family:

- `list teams`
- `get team`
- `list bots`
- `get bot`
- `update bot`
- `list sources`
- `get source`
- `create source`
- `update source`
- `delete source`
- `source tag counts`
- `team members`
- `invites`
- `questions`
- `conversations`
- `leads`
- `stats`
- `webhooks`
- `integrations`
- `MCP connections`
- `Skills library`
- `billing`

Prefer one focused search before each new operation family instead of broad searches that return unrelated operations.

## Fast Path Operations

For common setup and lookup tasks, search for these terms and expect these operation IDs in the Admin MCP catalog:

| Task | Search query | Expected operationId |
| --- | --- | --- |
| List teams visible to the authorized user | `list teams` or `GET /api/teams` | `get_teams` |
| Get one team by ID | `get team` or `GET /api/teams/{teamId}` | `get_teams_teamid` |
| Create a team | `create team` or `POST /api/teams` | `post_teams` |
| Update team settings | `update team` or `PUT /api/teams/{teamId}` | `put_teams_teamid` |
| List bots in a team | `list bots` or `GET /api/teams/{teamId}/bots` | `get_teams_teamid_bots` |
| Get one bot by ID | `get bot` or `GET /api/teams/{teamId}/bots/{botId}` | `get_teams_teamid_bots_botid` |
| Create a bot | `create bot` or `POST /api/teams/{teamId}/bots` | `post_teams_teamid_bots` |
| Update bot settings | `update bot` or `PUT /api/teams/{teamId}/bots/{botId}` | `put_teams_teamid_bots_botid` |
| Delete a bot | `delete bot` or `DELETE /api/teams/{teamId}/bots/{botId}` | `delete_teams_teamid_bots_botid` |

Use these IDs as recognition hints after `search` returns results. If search returns a different matching operation, trust the live catalog result and read its schema before executing.

## Constraints

- Do not call arbitrary DocsBot URLs. DocsBot Administration execution is limited to known catalog operations.
- Do not invent team IDs, bot IDs, source IDs, or operation IDs. Discover them with `search` and prior `execute` calls.
- Treat existing DocsBot dashboard RBAC as the source of truth. If an action is denied, report the denial rather than attempting to bypass it.
- Prefer idempotency keys for create/update operations when the operation supports them.
- Do not expose OAuth tokens, API keys, internal headers, or private response data beyond what the user needs for the task.
- Do not use Admin MCP for per-bot documentation retrieval or question-history semantic search; those are separate per-bot MCP servers.

## References

- [DocsBot MCP server guide](references/mcp-server.md)
- [MCP client configuration examples](references/mcp-client-config.md)
- [Bot-builder subworkflow](references/bot-builder/SKILL.md)
