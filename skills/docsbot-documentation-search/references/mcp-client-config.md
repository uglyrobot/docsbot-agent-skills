# MCP Client Configuration

## Documentation Search

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

Replace `{teamId}` and `{botId}` with the DocsBot team and bot IDs. Replace `<TOKEN>` with a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`.

## Install The Skill

```bash
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search
```

or:

```bash
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search
```
