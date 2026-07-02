# MCP Client Configuration

## Question History

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

Replace `{teamId}` and `{botId}` with the DocsBot team and bot IDs. Replace `<TOKEN>` with a DocsBot API key or a DocsBot MCP OAuth token prefixed with `mcp-`.

## Install The Skill

```bash
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-question-history
```

or:

```bash
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-question-history
```
