#!/usr/bin/env bash
set -euo pipefail

MARKETPLACE_REPO="${1:-DocsBotAI/docsbot-agent-tools}"

codex plugin marketplace add "$MARKETPLACE_REPO"
codex plugin add docsbot-mcp@docsbot

echo "DocsBot Admin MCP plugin installed. Start a new Codex thread to use it."
