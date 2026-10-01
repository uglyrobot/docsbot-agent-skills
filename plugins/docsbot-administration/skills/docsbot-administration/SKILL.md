---
name: docsbot-administration
description: Use this bundled DocsBot Administration workflow whenever the DocsBot Administration plugin is installed and the user asks to manage DocsBot teams, bots, sources, members, integrations, Skills, reports, or read-only account usage. This skill teaches efficient Admin MCP usage, current team detection, team and bot lookup, safe writes, and optional metadata discovery.
license: MIT
metadata:
  author: DocsBot
  version: "0.6.0"
  mcp_server_url: https://mcp.docsbot.ai
---

# DocsBot Administration

Use the hosted DocsBot Administration MCP server for account and dashboard administration:

```text
https://mcp.docsbot.ai
```

The hosted server advertises fixed, named Admin MCP tools. Call a known tool directly with its operation-specific `pathParams`, `query`, and/or `body` input. For example, call `list_teams` to resolve the team, `list_bots` with `pathParams.teamId` to resolve a bot, and `get_bot` with `pathParams.teamId` and `pathParams.botId` to inspect it. Read the advertised input schema before sending fields that are not already clear. Do not call a generic `execute` tool or send an `operationId`.

`list_tool_categories`, `search_tools`, and `get_tool_schema` inspect metadata for tools already advertised to the client. Use them only when the relevant name or schema is unclear; they do not enable, execute, or discover hidden operations. Stable tool names remain callable across additive, backward-compatible hosted MCP updates. New or changed metadata may be held by OpenAI's automated scan while the last approved definition remains live; a newly added tool is unavailable until approved. Keep calls compatible with the currently advertised schema. Plugin skills, config, and listing changes require a new package ZIP.

## Standard Workflow

1. Establish the working team before any team-scoped action.
2. Establish the working bot before any bot-scoped action.
3. Call a known named tool directly. Use `search_tools` only to locate an unfamiliar advertised tool.
4. Use `get_tool_schema` when input shape, permissions, or side effects are unclear.
5. Send required `pathParams`, `query`, and/or `body` fields to that named tool.
6. Keep useful IDs from results in thread context: team ID/name, bot ID/name, source IDs, member emails, integration IDs, and pagination state.

## Bot Builder Subworkflow

When the user asks to create, configure, tune, test, or hand off a new DocsBot bot, load the dedicated [bot-builder subworkflow](references/bot-builder/SKILL.md) before making MCP writes.

That subworkflow is part of DocsBot Administration, but it is intentionally kept as a nested reference tree because production bot creation has its own discovery, branding, source-selection, prompt, deployment, action, evaluation, and handoff rubric. Follow its reference chain from `references/bot-builder/` for bot-building tasks instead of merging those rules into this general administration workflow.

During a new or complete bot setup, prepare the voice prompt as well as the text prompt. The logical `voicePrompt` is saved as `voiceAgent.instructions`. Follow the bot-builder's voice guidance to preserve existing settings; enable advanced voice only when the user requests it, confirms it, or clearly includes voice in the intended outcome.

## Response Quality Subworkflow

When the user asks why a bot answered a question a certain way, to inspect question or conversation history, diagnose weak answers, or improve response quality from log evidence, load the [response-quality subworkflow](references/response-quality/SKILL.md). Use its evidence and remediation guidance before making changes.

## Evals and Instruction History

Before selecting a saved Evals or instruction-history workflow, inspect the currently advertised tools with `search_tools` and verify the relevant input contracts with `get_tool_schema`. Load the [Evals and instruction workflow](references/evals/SKILL.md) only for capabilities whose named tools are advertised. Bundled documentation does not mean Evals APIs, reports, version history, or dashboard handoffs are released for this account. If the tools are absent, draft questions locally, review ordinary conversation history through the response-quality workflow, and improve current instructions through advertised `get_bot`/`update_bot` tools. Do not call missing tools or promise saved sets, runs, or version restoration.

## Team Detection

The Admin MCP token identifies the authorized DocsBot user. It does not contain a fixed team ID or role snapshot, and DocsBot checks current team access and permissions live on each call.

When the user does not provide a team ID:

1. Call `list_teams`.
2. If exactly one team is returned, use it as the working team and state its name.
3. If multiple teams are returned, choose only when the user's wording clearly matches a team name, domain, customer, or prior thread context.
4. If multiple teams remain plausible, ask the user which team to use and show the shortest useful choices: team name, team ID, plan, and bot count when available.

If a user says "current team", "my team", or "the active team", do not assume the dashboard session's internal `currentTeam` is available through MCP. Resolve the working team from explicit context or by listing teams.

## Bot And Source Lookup

For bot-scoped work:

1. Ensure a working team is selected.
2. Call `list_bots` with `pathParams.teamId` for the working team.
3. Match the bot by exact ID first, then exact or close name match.
4. If the bot is ambiguous, ask the user to choose.

For source-scoped work:

1. Ensure working team and bot are selected.
2. Call `list_sources` with `pathParams.teamId` and `pathParams.botId`.
3. Use pagination and filters when supported instead of fetching every source.
4. Match source IDs directly when provided. Otherwise match by URL, title, type, status, or tags.
5. Fetch the full source only when list results are insufficient.

Use tag operations when the task mentions source tags, retriever tags, targeted retrieval, or tagged documentation. Bot `retrieverTags` define the allowed tag vocabulary, and source tags must match that vocabulary.

## Metadata Discovery Queries

When the tool name is unfamiliar, use `search_tools` with a focused task phrase:

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
- `account usage`

Metadata discovery is optional when the named tool is known. Use `get_tool_schema` for its advertised input contract when needed.

## Fast Path Operations

Call these stable names directly for common setup and lookup tasks:

| Task | Named tool |
| --- | --- |
| List teams visible to the authorized user | `list_teams` |
| Get one team by ID | `get_team` |
| Create a team | `create_team` |
| Update team settings | `update_team` |
| List bots in a team | `list_bots` |
| Get one bot by ID | `get_bot` |
| Create a bot | `create_bot` |
| Update bot settings | `update_bot` |
| Delete a bot | `delete_bot` |
| List a bot's research jobs | `list_research_jobs` |
| Get one research job | `get_research_job` |
| Cancel and remove a research job | `cancel_research_job` |

If a named tool is absent from the advertised catalog, do not attempt a generic operation. Report that the capability is unavailable.

## Writes And Confirmation

Ask for confirmation before any destructive, expensive, privacy-sensitive, or access-changing action unless the user already explicitly authorized that exact action. This includes deleting bots or sources, changing members or invites, editing API keys, modifying integrations, and deleting logged data.

Before a write, summarize:

- target team and bot when applicable
- operation purpose
- important IDs and names
- fields that will change
- expected side effect

Use an idempotency key for create/update tools only when its advertised schema supports one.

## Reporting Results

Return concise results with IDs and names the user can verify:

- team name and ID
- bot name and ID
- source title/type/status and ID
- member email and role
- operation result, warnings, and next action

If an operation is denied, report the permission or plan limitation. Do not attempt to bypass DocsBot RBAC or plan gates.

## Constraints

- Do not invent team IDs, bot IDs, source IDs, tool names, tags, roles, or plan capabilities.
- Do not expose OAuth tokens, API keys, internal headers, or private response data beyond what the user needs.
- Do not use Admin MCP for per-bot documentation retrieval or question-history semantic search; those are separate per-bot MCP servers.
- Treat DocsBot dashboard RBAC as the source of truth.

Subscription and commerce mutations are outside this plugin. Do not use `update_bot` to enable Stripe payments, refunds, cancellations, or other commerce actions. Read account usage through an advertised read tool when available.

## References

- [Bot-builder subworkflow](references/bot-builder/SKILL.md)
