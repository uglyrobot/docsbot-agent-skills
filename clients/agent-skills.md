# Claude Code And Agent Skills Clients

## Claude Code Plugin

The Claude Code plugin is the easiest installation path because it bundles both the DocsBot Administration workflow skill and the remote MCP server configuration:

```text
/plugin marketplace add uglyrobot/docsbot-agent-skills
/plugin install docsbot-administration@docsbot-plugins
/reload-plugins
```

After installation, run `/mcp`, select `docsbot`, and complete the browser-based DocsBot OAuth flow. No DocsBot API key is required.

The commands below remain available when you want portable skills without the plugin wrapper.

This repository includes portable Agent Skills packages:

```text
skills/docsbot-administration/
skills/docsbot-documentation-search/
skills/docsbot-question-history/
```

| Skill | Use |
| --- | --- |
| `docsbot-administration` | Administer DocsBot teams, bots, sources, members, integrations, Skills, reporting, and supported billing settings. |
| `docsbot-documentation-search` | Search and fetch indexed documentation and training-source content from a specific DocsBot bot. |
| `docsbot-question-history` | Search and fetch prior DocsBot questions, answers, conversations, and support history for a specific bot. |

## CLI Install

Use the common `npx skills` installer:

```bash
npx skills add uglyrobot/docsbot-agent-skills
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-administration
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search
npx skills add uglyrobot/docsbot-agent-skills --skill docsbot-question-history
npx skills add uglyrobot/docsbot-agent-skills --list
```

The installer targets `.agents/skills/` and symlinks into `.claude/skills/` for Claude Code compatibility when supported.

## SkillKit Install

For multi-agent installs:

```bash
npx skillkit install uglyrobot/docsbot-agent-skills
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-administration
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-documentation-search
npx skillkit install uglyrobot/docsbot-agent-skills --skill docsbot-question-history
npx skillkit install uglyrobot/docsbot-agent-skills --list
```

## Manual Install

The skill uses the standard layout:

```text
docsbot-administration/
├── SKILL.md
├── assets/
└── references/
```

To use a skill, copy or install that folder into the target client's skills directory, then configure the relevant remote MCP server in that client.

DocsBot Administration:

```json
{
  "mcpServers": {
    "docsbot": {
      "url": "https://mcp.docsbot.ai"
    }
  }
}
```

DocsBot Documentation Search:

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

DocsBot Question History:

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

The skills themselves do not store credentials. Configure credentials in the MCP client according to that client's normal credential storage rules.

Use `docsbot-administration` for account and dashboard administration. Use `docsbot-documentation-search` for indexed bot source retrieval. Use `docsbot-question-history` for historical support question and conversation retrieval.
