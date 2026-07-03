---
name: docsbot-bot-builder-admin-mcp
description: Use when creating, configuring, tuning, testing, or handing off a DocsBot bot through the DocsBot Admin MCP. Covers discovery, branding, bot creation, source selection, source tags, prompts, widget/embed/helpdesk/Slack deployment choices, lead capture, escalation, Skills, external MCP connectors, and final dashboard/share links.
---

# DocsBot Bot Builder Admin MCP

Use this skill to build a high-quality DocsBot bot through the hosted DocsBot Admin MCP at `https://mcp.docsbot.ai`.

Admin MCP exposes only two tools:

- `search` to discover catalog operations and schemas.
- `execute` to run one selected operation by `operationId`.

Always search before executing an operation unless the exact operation was already returned in this turn.

This skill is the build surface. Do not use adjacent DocsBot demo-bot skills, public demo/pilot endpoints, onboarding bot creators, or helper wrappers as a shortcut for final-product validation. Those paths can create scaffold artifacts that fail this skill's rubric. For validation, use Admin MCP `search` and `execute` plus ordinary public research only.

## Quick Start

1. Load [workflow.md](references/workflow.md) before starting a real bot setup.
2. Load [operations.md](references/operations.md) before the first MCP write or when operation names/payload fields matter.
3. Load [branding-appearance.md](references/branding-appearance.md) before applying brand, widget, first-message, starter-question, or support URL settings.
4. Load [deployment-surfaces.md](references/deployment-surfaces.md) before choosing or handing off widget/embed/dashboard/Help Scout/Slack/API deployment.
5. Load [prompt-instructions.md](references/prompt-instructions.md) before creating or materially changing prompts.
6. Load [actions-integrations.md](references/actions-integrations.md) before configuring actions, integrations, Skills, external MCP servers, or deployment safety settings.
7. Load [final-handoff.md](references/final-handoff.md) before writing the final user-facing deliverable.
8. Load [evaluation-rubric.md](references/evaluation-rubric.md) when judging whether a configured bot is complete.

## Operating Rules

- Resolve the target team with `get_teams`; never assume the OAuth token is tied to one team.
- Use `idempotencyKey` for create/update operations when practical.
- For destructive writes, billing changes, integration disconnects, source deletion, member changes, and bot deletion, summarize the intended action and ask for confirmation unless the user already explicitly authorized that exact action.
- Never expose OAuth tokens, API keys, signed upload URLs, custom header secrets, bot signature keys, or secret binding values in user-facing output.
- Bot/settings reads may return signature-like or secret-like fields. Treat them as sensitive, do not quote them, and report the catalog/sanitization issue separately from the configured bot quality unless you exposed the value.
- Preserve the exact DocsBot prompt template structure. Customize company/product context and necessary extra instructions, but keep `search_documentation`, major sections, ordering, and tool-selection instructions unless the target use case makes them wrong.
- Prefer minimal, focused questions. Infer from the business website, docs, public support center, product pages, sitemap, and user context before asking.

## Build Flow

Use this sequence for production bot setup:

1. Define purpose, audience, deployment, and success criteria.
2. Research the business and product, including public docs, knowledge base, help center, sitemap, pricing/product pages, integrations, and support/contact paths.
3. Analyze branding through `post_teams_teamid_bots_analyze` when a public domain is available. Use its colors/logos/language/widget detection as the first pass, then refine contrast and first message.
4. Create the bot with a valid locale code such as `en` and an agent prompt that includes `search_documentation` when `isAgent` is true. Omit `model` unless the user explicitly requests a non-default model, so the DocsBot API uses the current default. Also omit rate-limit and IP-recording fields during create so their default/null state is preserved.
5. Update appearance, first message, starter questions, support link, agent settings, source tag vocabulary, actions, lead collection, MCP servers, and skill settings.
6. Add sources. Use public URL, website, sitemap, RSS, Q&A, and uploaded-file flows as appropriate. Do not poll waiting for indexing; configure the rest of the bot while sources ingest. For Truto/cloud connectors, give the dashboard deep link when file selection or OAuth must happen outside MCP.
7. Tune prompts from the closest exact prompt asset. Insert company/product context and deployment-specific behavior with minimal in-place edits, without replacing or reorganizing the tested template guardrails.
8. Configure actions: escalation, lead capture, scheduling/custom buttons, web search, Skills, external MCP connectors, Help Scout, Slack, webhooks, Stripe/billing, or other integrations only when they clearly serve the use case.
9. Verify the bot with final reads: bot settings, source details/status counts, tag counts, OpenAPI retrieval schema, integrations/skills settings, safety settings, and final dashboard/share links.
10. Hand off using [final-handoff.md](references/final-handoff.md): include a clear "try the bot now" link, custom next steps, relevant dashboard deep links, useful test prompts, unresolved dashboard-only steps, and a concise readiness status.

For final-product quality, fail the setup instead of softening the language when any of these are true:

- The bot name or description contains test, MCP test, disposable, demo, review, timestamp, or judge-review scaffolding.
- A critical source is failed or has zero chunks. If it is still indexing, do not wait; mark readiness as pending indexing and caution the user in the final response.
- Source tags exist but the agent prompt lacks compact routing guidance tailored to why the tags exist, including one-tag, multi-tag, clarification, or untagged=false exclusion behavior as appropriate.
- Source tags do not discriminate, such as assigning every tag to every source.
- Broad public support, developer, or presales coverage has fewer than 20 ready high-signal pages without an explicit narrow scope.
- Public lead/support widgets skip safety/action decisions such as link safety, default `piiRedaction: false` unless requested, lead capture or explicit no-lead rationale, support/escalation URLs, and clearly justified action choices.
- Public widgets keep a generic first message or lack verified brand assets when brand analysis is available.
- Internal/helpdesk bots claim Help Scout auto-drafting, Slack deployment, or another connected integration without integration read evidence or an explicit dashboard-only/private-copilot handoff.
- Fast-changing docs, pricing, changelog, status, support, or platform behavior has no refresh, RSS, live source/action, or prompt caveat plus canonical CTA.

Before handoff, run this readiness audit and report any failed item as "not final-product ready":

- Clean saved name/description.
- Saved branding and first message are specific to the business.
- All promised source areas are named, tagged, broad enough, and either ready/nonzero or explicitly called out as still indexing in the final response.
- Tags route to distinct source groups, have useful descriptions, and the agent prompt explains how to use them for the actual conflict model, such as product/version separation, combined categories, or when to set untagged to false. Public/internal or customer/staff audience splits require separate bots, not tag filtering.
- Public widgets have support/contact route, lead decision, safety decisions, and only the actions that serve the use case.
- Helpdesk/internal bots have an explicit deployment surface, integration evidence or dashboard-only rationale, and PII/log/token handling.
- Dynamic topics have freshness handling or explicit caveats.
- Important website, docs, support, pricing, changelog, and product sources have monthly auto-refresh when the source type supports it, unless the user requests a different cadence.
- Sensitive raw fields and inherited analytics are omitted from evidence.

## References

- [workflow.md](references/workflow.md): Detailed discovery, tuning, and handoff workflow.
- [operations.md](references/operations.md): Operation IDs, payload shapes, tested guardrails, and dashboard links.
- [branding-appearance.md](references/branding-appearance.md): Brand analysis, widget appearance, first message, starter questions, and visual readback checks.
- [widget-branding.md](references/widget-branding.md): Conditional detail for widget colors, header logo selection, contrast checks, and uploaded/custom logo fallback.
- [deployment-surfaces.md](references/deployment-surfaces.md): Widget/embed/dashboard/Help Scout/Slack/API deployment selection, handoff links, and verification.
- [prompt-instructions.md](references/prompt-instructions.md): Prompt preset selection, template guardrails, source-tag routing, prompt asset usage, and verification.
- [source-types.md](references/source-types.md): Source type selection, create payloads, refresh defaults, and links to conditional source-specific detail files.
- [actions-integrations.md](references/actions-integrations.md): Action/integration selection, public widget safety, and links to conditional action detail files for escalation, lead collection, buttons, scheduling, web search, webhooks, Skills, and MCP.
- [final-handoff.md](references/final-handoff.md): Required final user-facing deliverable shape, custom next steps, test prompts, and dashboard deep-link selection.
- [evaluation-rubric.md](references/evaluation-rubric.md): Scoring rubric for bot quality, completeness, and MCP hygiene.

## Source Anchors

Use current public DocsBot docs and live MCP catalog as source of truth:

- Admin MCP and per-bot MCP docs: `https://docsbot.ai/documentation/developer/mcp-server`
- Bot API docs: `https://docsbot.ai/documentation/developer/bot-api`
- Source API docs: `https://docsbot.ai/documentation/developer/source-api`
- Widget docs: `https://docsbot.ai/documentation/developer/embeddable-chat-widget`

If docs, code, and live MCP behavior disagree, state the conflict and follow live MCP validation for the immediate setup.
