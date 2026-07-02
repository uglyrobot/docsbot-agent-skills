#!/usr/bin/env bash
set -euo pipefail

MARKETPLACE_REPO="${1:-uglyrobot/docsbot-agent-skills}"

codex plugin marketplace add "$MARKETPLACE_REPO"
codex plugin add docsbot-administration@docsbot

echo "DocsBot Administration plugin installed. Start a new Codex thread to use it."
