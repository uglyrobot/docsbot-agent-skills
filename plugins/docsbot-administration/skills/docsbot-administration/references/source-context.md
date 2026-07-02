# Source Context

These workflow instructions are based on the DocsBot developer documentation:

- Admin MCP: `src/pages/documentation/developer/mcp-server.md`
- Teams Admin API: `src/pages/documentation/developer/team-api.md`
- Bots Admin API: `src/pages/documentation/developer/bot-api.md`
- Sources Admin API: `src/pages/documentation/developer/source-api.md`
- Authentication: `src/pages/documentation/developer/authentication.md`

Key behavior:

- Admin MCP uses OAuth and Dynamic Client Registration at `https://mcp.docsbot.ai`.
- Admin MCP exposes only `search` and `execute`.
- Admin MCP tokens identify the DocsBot user, not a fixed current team.
- DocsBot checks team access, bot access, billing permissions, and roles live on each action.
- Team-scoped API work should start by resolving the working team.
- Bot-scoped API work should resolve the working bot from the selected team.
