#!/usr/bin/env bash
set -euo pipefail

codex mcp add docsbot --url https://mcp.docsbot.ai
codex mcp login docsbot

echo "DocsBot Administration configured directly. Start a new Codex thread to use it."
