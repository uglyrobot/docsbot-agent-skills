---
name: docsbot-administration
description: Use this bundled DocsBot Administration workflow whenever the DocsBot Administration plugin is installed and the user asks to manage DocsBot teams, bots, sources, members, integrations, Skills, reports, or billing-related settings. This skill teaches efficient Admin MCP usage, current team detection, team and bot lookup, safe writes, and progressive operation discovery.
license: MIT
metadata:
  author: DocsBot
  version: "0.2.0"
  mcp_server_url: https://mcp.docsbot.ai
---

# DocsBot Administration

Use the hosted DocsBot Administration MCP server for account and dashboard administration:

```text
https://mcp.docsbot.ai
```

The server exposes two tools:

- `search` discovers Admin API catalog operations, required parameters, schemas, permission notes, response summaries, and side-effect levels.
- `execute` runs one selected catalog operation by `operationId` with structured `pathParams`, `query`, `body`, and optional `idempotencyKey`.

Always use progressive discovery. Do not call arbitrary DocsBot URLs, guess operation IDs, or assume all Admin API operations are loaded into the model context.

## Standard Workflow

1. Establish the working team before any team-scoped action.
2. Establish the working bot before any bot-scoped action.
3. Call `search` for the operation family or task.
4. Read the returned operation details, especially required fields, permission notes, response summaries, and side-effect level.
5. Call `execute` with only the selected `operationId` and the required structured arguments.
6. Keep useful IDs from results in thread context: team ID/name, bot ID/name, source IDs, member emails, integration IDs, and pagination state.

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

For bot-scoped work:

1. Ensure a working team is selected.
2. Search for `list bots`.
3. Execute the list-bots operation for the working team.
4. Match the bot by exact ID first, then exact or close name match.
5. If the bot is ambiguous, ask the user to choose.

For source-scoped work:

1. Ensure working team and bot are selected.
2. Search for `list sources`.
3. Use pagination and filters when supported instead of fetching every source.
4. Match source IDs directly when provided. Otherwise match by URL, title, type, status, or tags.
5. Fetch the full source only when list results are insufficient.

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

## Writes And Confirmation

Ask for confirmation before any destructive, expensive, privacy-sensitive, or access-changing action unless the user already explicitly authorized that exact action. This includes deleting bots or sources, changing members or invites, changing billing-related settings, editing API keys, modifying integrations, and deleting logged data.

Before a write, summarize:

- target team and bot when applicable
- operation purpose
- important IDs and names
- fields that will change
- expected side effect

Prefer `idempotencyKey` for create/update operations when the selected operation supports it.

## Reporting Results

Return concise results with IDs and names the user can verify:

- team name and ID
- bot name and ID
- source title/type/status and ID
- member email and role
- operation result, warnings, and next action

If an operation is denied, report the permission or plan limitation. Do not attempt to bypass DocsBot RBAC or plan gates.

## Constraints

- Do not invent team IDs, bot IDs, source IDs, operation IDs, tags, roles, or plan capabilities.
- Do not expose OAuth tokens, API keys, internal headers, or private response data beyond what the user needs.
- Do not use Admin MCP for per-bot documentation retrieval or question-history semantic search; those are separate per-bot MCP servers.
- Treat DocsBot dashboard RBAC as the source of truth.
