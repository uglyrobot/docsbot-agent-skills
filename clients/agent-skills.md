# Claude Code And Agent Skills Clients

This repository includes a portable Agent Skills package:

```text
skills/docsbot-admin-mcp/
```

The skill uses the standard layout:

```text
docsbot-admin-mcp/
├── SKILL.md
├── assets/
└── references/
```

To use it, copy or install that folder into the target client's skills directory, then configure the remote MCP server in that client:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

The skill itself does not store credentials. The MCP client should start the DocsBot browser OAuth flow and store the resulting token according to that client's normal credential storage rules.

Use the skill when the user asks to administer DocsBot, manage teams, inspect bots, configure sources, review dashboard data, manage integrations or Skills, or use the DocsBot Admin API through an agent.
