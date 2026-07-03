# Forward-Test Scenarios

Use these scenarios to validate the skill with disposable bots in the `Demo Bots` team. Delete test bots unless the user asks to keep them.

When a scenario is judged as final-product quality instead of a smoke test, use a clean production-like saved bot name. Track disposability in your notes and cleanup list, not in the saved name or description.

Validation must exercise this Admin MCP skill directly. Do not use `docsbot-demo-bot`, public demo/pilot endpoints, onboarding creators, or adjacent helper skills to create the bot for a final-product test.

## Common Test Matrix

1. Public SaaS support widget
   - Example company: Stripe, Linear, Supabase, or Vercel.
   - Purpose: public support and presales.
   - Sources: docs root, pricing page, changelog or release notes.
   - Tags: `product`, `pricing`, `updates` when sources are distinct.
   - Actions: escalation, lead collection before escalation, custom pricing/demo button, optional web search.

2. Developer documentation assistant
   - Example company: Next.js, Cloudflare Workers, Sentry, or PostHog.
   - Purpose: technical docs search for developers.
   - Sources: developer docs, API reference, selected getting-started pages.
   - Tags: `guide`, `api`, `changelog`, or version tags when docs differ.
   - Actions: GitHub/code-reading skill only if public code is important; web search only for live release/status facts.

3. Internal support/helpdesk copilot
   - Example company with public help center: Shopify, GitLab, Notion, or Slack.
   - Purpose: helpdesk tier-2 draft assistance.
   - Sources: public help center plus support policy pages.
   - Tags: `support`, `billing`, `account`, `admin`.
   - Actions: Help Scout or helpdesk integration notes, no customer-facing OAuth MCPs unless scoped safely.

4. Sales/presales qualification bot
   - Example company: HubSpot, Webflow, or Airtable.
   - Purpose: qualify leads and answer plan/use-case questions.
   - Sources: homepage, product pages, pricing, case studies, feature announcements.
   - Actions: lead collection before response or before escalation, scheduling button, pricing CTA, escalation.

5. Open-source technical assistant
   - Example project/company: Tailwind CSS, Astro, FastAPI, or LangChain.
   - Purpose: answer technical questions from docs and optionally code.
   - Sources: docs, API reference, migration guide, release notes.
   - Tags: `docs`, `api`, `migration`, and version tags if needed.
   - Actions: GitHub skill or MCP for live code when configured; prompt must say when to use it instead of docs.

## Validation Checklist

For each test bot:

- Resolve `Demo Bots` with `get_teams`.
- Create with valid locale and agent prompt containing `search_documentation`.
- Run `post_teams_teamid_bots_analyze` for the company domain when available.
- Update appearance, first message, starter questions, prompt, source tags, and actions.
- Create through explicit Admin MCP create/update operations; do not use demo/onboarding scaffold creation, public demo/pilot endpoints, or adjacent demo-bot skills as the main build path for final-product tests.
- Add at least one small public source and verify it was queued with the expected fields, tags, and refresh schedule.
- Verify `get_teams_teamid_bots_botid_sources_counts` and tag counts.
- For final-product quality, do a final source status check before handoff. Verify ready page/chunk coverage per tag when available and replace failed critical sources before handoff.
- Do not wait for critical sitemaps/RSS/website crawls to finish indexing during validation. If the final check still shows indexing, mark readiness as pending indexing and caution that answers for those areas may be incomplete until ingest finishes.
- Read source details and sample indexed URLs or equivalent evidence for critical ready tags; do not rely on aggregate counts alone.
- Verify safety choices for public bots: `piiRedaction` remains false unless requested or compliance-driven, link safety, lead-field necessity, and support/escalation URL fit.
- Verify public support/presales actions: escalation/contact, lead collection or no-lead rationale, support URL, scheduling/booking decision, and any custom buttons only when the use case requires them.
- Verify first message, starter questions, placeholder, logo/icon/header, and brand color from saved bot settings.
- Verify prompt tag-routing text matches why tags exist, including one-tag, multi-tag, clarification, and untagged=false exclusion behavior where appropriate; it does not need to repeat every tag key when the retrieval schema descriptions are sufficient.
- Verify tags discriminate between source groups; do not assign every tag to every source unless there is only one broad tag.
- Verify source titles have no scaffold labels such as `undefined Website` or `undefined Sitemap`.
- Verify deployment-mode rationale for internal/helpdesk bots: Help Scout, Slack, webhook, MCP connector, or dashboard/link-only.
- If Help Scout auto-drafting, Slack deployment, webhook delivery, or another connected integration is promised, verify it with integration/webhook reads; `widgetType` alone is only website-widget metadata.
- Verify support-staff bot PII/log/token handling and whether PII redaction is requested or compliance-driven.
- Verify dynamic/fresh content strategy for pricing, changelog, status, incidents, support workflows, and fast-changing platform docs.
- Verify important website/docs/support/pricing/changelog/product sources have monthly auto-refresh where scheduling is supported, unless another cadence is justified.
- Ignore inherited or unrelated analytics in shared demo environments unless dates/topics prove the stats belong to the new bot.
- Verify bot settings after update.
- Verify retrieval OpenAPI tag enums when source tags are configured.
- Produce dashboard chat/deep links.
- Delete the bot unless retention was requested.

Record any MCP gaps or product issues separately from skill defects. If an operation fails because of current backend behavior, preserve the error message and adjust the skill only if the agent can avoid or recover from it.

Small public sources are acceptable for smoke tests. They are not enough for a final-product score unless the requested bot is narrow. For broad developer, support, or presales bots, the test should prove source breadth with a coverage matrix and realistic per-tag questions.

## Historical Smoke Tests

On 2026-07-03, early smoke tests proved the basic Admin MCP create/update/source/delete path against disposable Demo Bots team bots. These are not final-product quality examples and should not be used as the bar for current validation:

- Linear public support/presales widget: analyzer branding, `helpscout` widget type, first message, support handoff, lead collection before escalation, `product` and `pricing` source tags, two URL sources, ready counts verified.
- Vercel developer docs assistant: analyzer branding, developer-docs prompt, `platform` and `nextjs` source tags, two URL sources, ready counts verified.
- Webflow presales/onboarding bot: analyzer branding, lead collection before response, `product` and `pricing` source tags, two URL sources, ready counts verified.
