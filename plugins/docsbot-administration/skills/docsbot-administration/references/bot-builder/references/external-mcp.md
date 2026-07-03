# External MCP Actions

Read this only from `actions-integrations.md` when external MCP servers are in scope.

## Scope Decision

Prefer external MCP servers for non-user-scoped lookups/actions, such as public docs, status, inventory, catalog, billing lookup with safe identifiers, or internal operations for private team bots.

Be cautious with OAuth MCP servers that inherit the bot owner's scopes. Those are usually appropriate only for internal team bots, because public customers chatting with the bot are not the OAuth user and actions cannot automatically be limited to the end customer's account.

## Operation Flow

1. Search live Admin MCP catalog for MCP operations.
2. Discover tools with `post_teams_teamid_bots_botid_mcp_discover`.
3. If `requiresOAuth` or similar auth state appears, give the dashboard connection link and stop before promising availability.
4. Choose only the tool subset needed for the use case.
5. Draft metadata with `post_teams_teamid_bots_botid_mcp_server_draft`.
6. Save the reviewed server entry in `mcpServers` through `put_teams_teamid_bots_botid`.
7. Add prompt instructions that say when to use the MCP server and when not to.
8. Read the saved bot settings and verify the server appears with the expected tools/metadata.

## Safety Rules

- Do not run write-capable external MCP tools during setup unless the user explicitly authorizes that live action.
- Do not expose custom headers, OAuth tokens, or connector secrets.
- Public bots should not use owner-scoped OAuth MCP tools for customer account actions unless the user explicitly accepts the scope model and risk.
- If a tool needs customer identity, add prompt rules to ask for it and refuse unsafe assumptions.
- Prefer non-user-scoped reads for public bots; reserve owner-scoped actions for internal/private bots.

## Prompt Lines

```text
Use the status MCP server only for current service status or incident questions. For product usage and setup questions, use search_documentation first.
```

```text
Use the internal billing MCP only for staff-facing account lookup after the user provides a verified account identifier. Do not use it in public anonymous chats.
```

## Verification

- Read saved `mcpServers` from bot settings.
- Confirm the prompt mentions the server's use boundary.
- Confirm OAuth/dashboard-only steps are listed in handoff if incomplete.
- If the discovery result includes write-capable tools, document that they were not executed during verification unless explicitly authorized.
