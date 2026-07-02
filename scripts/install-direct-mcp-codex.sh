#!/usr/bin/env bash
set -euo pipefail

codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot

echo "DocsBot Admin MCP configured directly. Start a new Codex thread to use it."
