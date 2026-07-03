# Bot Creation And Tuning Workflow

## Intake

Collect enough to infer the setup without turning the work into a quiz:

- Bot purpose: support, presales, onboarding, internal team, department, partner enablement, helpdesk copilot, or research.
- Audience: public customers, signed-in customers, employees, support staff, sales team, or a mixed group.
- Deployment: widget, embedded chat, dashboard chat, Help Scout, Slack, API, external MCP/search, or internal-only.
- Brand inputs: website/domain, product name, colors/logos if known, tone, first-message expectations.
- Knowledge sources: public docs, knowledge base, marketing pages, changelog, blog subset, sitemap, RSS, files, cloud drives, support history, code repos, or private SOPs.
- Action scope: escalation, lead capture, meeting booking, custom CTAs, web search, Skills, external MCP connectors, webhooks, Stripe/billing, helpdesk/Slack integrations.

Ask only for missing information that materially affects setup, such as private files, required escalation destination, or whether a live action should be customer-facing.

## Research

Use the user's domain and public docs to infer:

- Product categories, target customers, pricing/support terminology, and likely question clusters.
- Best source candidates: docs/KB, docs sitemap, developer docs, support articles, product/pricing pages, getting-started content, changelog/RSS, and current feature announcements.
- Sources to avoid or limit: full blog archives, broad marketing category pages, stale announcement archives, legal/policy pages that could conflict with docs, and unrelated SEO pages.
- Deployment hints: existing helpdesk widgets, support/contact links, Slack/community links, app portals, developer docs, or public status pages.

Prefer current high-signal sources. If a blog or changelog matters, use a focused category, tag, RSS feed, or recent announcement source rather than a full archive.

Before creating sources, decide whether the bot is being built as:

- A final-product bot: broad enough, polished enough, and verified enough for the user's intended workflow.
- A validation/demo bot: useful for proving the MCP workflow, but intentionally smaller or disposable.

Do not let a validation-scale source set carry final-product language in the prompt or handoff.

## Branding

Before applying brand and widget appearance settings, read [branding-appearance.md](branding-appearance.md).

When a public website is available:

1. Run `post_teams_teamid_bots_analyze` with `siteURL`.
2. Prefer returned brand colors and full logos over generic favicons.
3. Choose a widget color with contrast against the site background, not just the first brand color.
4. Prefer a full logo for header/logo and an icon/avatar for compact bot icon when available.
5. Save the full analyzer result into `brandAnalysis` during bot create/update, using `{ domain, url, ...analysisResult }`.
6. Verify saved `brandAnalysis.colors` and `brandAnalysis.logos`; they are required for dashboard brand presets and discovered bot icons.

For website widget deployments, load [widget-branding.md](widget-branding.md) before saving the final color/logo pair. Visually check that the chosen header logo contrasts with the chosen widget color, and use its upload fallback when the right logo was not returned by brand analysis.

Set a custom first message that matches the use case. Avoid generic "What can I help you with?" when the business and purpose are known.

Before final handoff, verify saved brand fields from the bot read, not only the analyzer output: widget color, logo/header/icon where available, support URL, first message, placeholder, and starter questions. For widgets, also verify logo/color contrast or list it as remaining visual review.

For final-product bots, use a clean production name and description. Avoid test, MCP test, timestamped, disposable, judge-review, review, demo, or scaffolding language in the bot itself.

## Deployment Surface

Before choosing or handing off a deployment surface, read [deployment-surfaces.md](deployment-surfaces.md). The selected surface affects branding, prompt tone, safety settings, actions, Skills/MCP risk, and which dashboard-only steps the user must complete.

## Prompt Tuning

Before creating or materially changing prompts, read [prompt-instructions.md](prompt-instructions.md).

In the main workflow, remember the core rule: start from the closest exact DocsBot prompt asset, preserve its sections and tested tool/grounding guardrails, then minimally insert company/product context, deployment behavior, source-tag routing, and action/Skill/MCP usage guidance. Do not fully replace, broadly reorder, or hand-write the template unless the user explicitly asks for a bespoke prompt and accepts losing template guardrails.

If `retrieverTags` are configured, the agent prompt should include compact routing guidance customized to why the tags exist. Do not repeat every tag ID and description in the prompt; those already appear in the search tool schema. State whether searches should normally use one tag, may combine multiple tags, should ask a clarifying question before searching, or should set untagged to false to avoid conflicting/noisy global sources. Untagged/global sources are included by default, so mention them only when excluding them matters. Tags must discriminate; if every source should be searched together, skip tags or use one broad tag.

## Sources

Before creating sources, read [source-types.md](source-types.md). It links to source-specific detail refs such as document uploads and connector handoffs; load those only when the selected source category requires them. Use live Admin MCP `search` for `post_teams_teamid_bots_botid_sources` when an exact payload schema matters, because supported source types and connector fields can change.

Use this selection logic:

- Docs, KB, support center, developer docs, or product-detail coverage: prefer sitemaps. Use full sitemaps unless sub-sitemaps cleanly exclude sections you do not want, such as full blogs, stale archives, legal-only pages, jobs, or unrelated marketing pages.
- No sitemap: use MCP website mapping (`post_teams_teamid_bots_botid_sources_map`) to fetch candidate site structure, then create a `website` source with the root `url` and the full selected `urls` set. The website scan usually finds quickly accessible top-level or obvious linked URLs; it is not a complete crawl and can miss deep docs/KB/product pages. Check the returned URLs against navigation, docs indexes, or a brief manual crawl before claiming final-product coverage. If mapping is shallow or fails, briefly crawl/fetch public pages yourself and create a complete URL list from all applicable URLs.
- URL lists do not crawl linked pages. They index only the URLs you provide, so never use a single docs/KB root URL list as if it imports the linked knowledge base.
- Specific important pages: add as URL list/website source only when every needed URL is enumerated or when the bot scope is intentionally narrow.
- Broad final-product bots need broad source coverage. Do not treat a handful of top-level pages as final-product quality for a large developer, support, or presales domain.
- Public docs with distinct products or versions: define source tags first, then assign each source to the matching tag during creation. If sources already exist, apply tags afterward with the bulk tag operation and verify counts.
- Changelog/release notes: use RSS or a focused category if available.
- Files: get a signed upload URL through MCP, upload bytes outside MCP, then create the document source.
- Cloud connectors or Truto-backed sources: MCP can create/update some records, but user OAuth/file selection often must happen in the dashboard. Give the exact dashboard link and what to choose.
- Helpdesk history: prefer native integrations like Help Scout where supported; configure routing and prompt separately.

For final-product builds, create the bot through the Admin MCP bot create operation and add named sources explicitly. Do not use adjacent demo-bot skills, public demo/pilot URLs, or onboarding bot creation as the main build path. Demo/onboarding-created bots often include scaffolded source titles, broad auto-sources, copied analytics, or disposable descriptions. If you inherit any of those artifacts, fix or remove them before final handoff.

For final-product setups, build a coverage matrix before handoff:

- Each declared answer domain or source tag.
- Source URL/title/type.
- Status, page count, chunk count, and tag.
- Sampled indexed URLs or other source-detail evidence, not only aggregate counts.
- Refresh behavior when available. Important website, docs, support, pricing, changelog, and product sources should auto-refresh monthly when the source type supports scheduling, unless the user requests another cadence.
- Why that source is sufficient for the questions the prompt promises to answer.
- Follow-up needed when coverage is dashboard-only, private, failed, or too shallow.

After adding sources, do not poll waiting for indexing to finish. Indexing large websites, sitemaps, document batches, and cloud sources can take a long time. Read the created source once to confirm it was queued with the expected type, URL/file fields, tags, and refresh schedule, then continue configuring prompts, branding, actions, integrations, Skills, MCP, safety, and handoff links.

Before final handoff, do one final source status check with source list/details, source counts, and tag counts. If sources are still `pending` or `indexing`, do not wait; caution the user that the bot may not fully answer from those sources until indexing completes. Failed or zero-content sources in a target-critical tag are blockers. Retry with alternate crawlable URLs, a scoped website crawl, a curated URL list, Q&A, or a dashboard handoff only when a final read shows failure/zero content or an obviously bad queued source. Broad fallback, changelog, pricing, and status sources are critical when the prompt promises those topics.

For broad final-product bots, prefer sitemap sources scoped to a docs/help center/product section because website mapping is usually incomplete. Use website mapping only as a discovery aid or when sitemaps are unavailable or too noisy, and fill gaps with complete curated URL batches. A validation bot can use small sources, but label that as demo-scale. As a hard gate, broad developer/support/presales bots need at least 20 ready high-signal pages, every critical tag needs nonzero ready chunks, and large suites should usually have 50+ ready pages or a clearly narrowed promise.

Before handoff, scrub sources:

- No source title should be `undefined Website`, `undefined Sitemap`, or another scaffold label.
- Untagged sources are acceptable for shared/global context. If untagged sources contain conflicting product/version/audience content, the prompt must explain when to set untagged to false.
- Still-indexing sources may remain queued, but the final response must clearly caution the user that coverage is pending indexing and the bot is not fully ready for those topics yet.
- No source should have all tags unless the tag design intentionally has a single broad tag.
- If a scaffold source cannot be renamed or deleted in time, narrow the bot scope and report it as not final-product ready.

For pricing/plan bots, treat pricing freshness and crawlability as first-class. If public pricing pages produce no indexed content, fall back to crawlable pricing help-center pages, product catalog pages, plan-limit docs, curated Q&A, or a clear dashboard/live-web-search handoff. Verify ready page/chunk counts for the pricing tag, not just tag assignment counts.

For dynamic topics such as status, pricing, billing, plan limits, incidents, quota usage, or support entitlements, choose one of:

- A source that refreshes on an appropriate schedule. For important web sources, default to monthly auto-refresh where supported.
- RSS or changelog sources that are ready and non-empty.
- Live web search or a non-user-scoped MCP/action when current facts are required.
- Prompt caveats or a specific custom button only when a visible canonical live-page handoff is required and no better action covers it.

If none of those is configured, narrow the prompt so the bot does not promise current answers for that topic.

For broad final-product support bots, also check breadth per tag. One source per tag can pass only when that source has enough ready pages/chunks and sampled URLs for the promised subdomain. As a rule of thumb, critical tags should have at least several representative URLs and enough chunks to answer realistic questions, not just a single landing page or tiny Q&A source.

For Sentry-like developer support bots, check coverage for SDK/platform setup breadth, missing events, source maps/releases, tracing/performance, sampling, alerts/issues, project/org configuration, DSN/client keys, auth, and changelog freshness before calling the setup final.

## Source Tags

Use source tags when the bot covers information that could conflict:

- Multiple products.
- Multiple major product versions.
- Regional/legal variations.
- Billing vs technical vs developer docs.
- Same-audience procedure families.

Do not use source tags to isolate public vs internal/private knowledge, or customer-facing vs staff-only procedures. Tag filtering is retrieval guidance, not a security boundary. Create separate bots with separate source sets and deployment surfaces for those use cases.

Keep tag keys short and stable, for example `v1`, `v2`, `api`, `billing`, `developer`, `admin-procedure`. Descriptions should explain when the agent should filter to that tag.

Add compact prompt guidance that matches the tag design. Examples:

```text
When a question is about a specific product or version, filter search_documentation to that tag. If the product/version is unclear and answers may differ, ask a brief clarifying question before searching.

For cross-product comparisons, search the relevant product tags together. Keep untagged/global sources included unless they would conflict with the selected product or version; when they would conflict, set untagged to false.
```

## Actions And Integrations

Before configuring actions, integrations, Skills, external MCP servers, deployment actions, or public widget safety settings, read [actions-integrations.md](actions-integrations.md). It links to Skills-library and external-MCP details only when those categories are in scope.

In the main workflow, keep actions minimal and purposeful: enable only what supports the bot's deployment, verify saved settings from bot/integration reads, and add matching prompt instructions for every action the user should know how to trigger. For public bots, keep `piiRedaction` false unless the user requests it or a concrete compliance requirement exists.

## Handoff

Before writing the final response, read [final-handoff.md](final-handoff.md). The final user-facing message must be a practical deliverable, not only an audit report.

End every real setup with:

- Bot name, team, bot ID.
- Source coverage matrix with status, page/chunk counts, and unresolved failed or shallow areas.
- Final source status check: ready/failed/indexing counts, tag counts, schedule/freshness, and any indexing sources that are not ready yet.
- Source tags, what they are for, and verified tag counts.
- Prompt tag-routing verification: confirm the prompt has compact tag-routing guidance customized to the tag purpose, the retrieval schema exposes tag IDs/descriptions, and any intentional multi-tag behavior or untagged=false exclusion behavior is documented.
- Enabled actions/integrations/skills/MCP connectors.
- Prompt/template used and major customizations.
- Retrieval OpenAPI tag-enum verification when source tags are configured.
- Optional live retrieval test with `post_teams_teamid_bots_botid_search` only when authorized; use tags to verify routing when configured.
- Safety choices for public bots, including PII redaction, link safety, lead fields, and support/escalation URL rationale.
- Auto-refresh choices for important web sources, especially docs, support, pricing, changelog, product, and status sources.
- Dashboard chat link and relevant deep links.
- Public share/embed link only when confirmed from bot/dashboard data.
- Suggested test questions for happy path, missing info, escalation, lead capture, and action/skill triggers.

Do not use analytics or conversation stats as quality evidence for newly created test bots unless the data clearly belongs to that bot after creation. In shared validation environments, compare `createdAt` and topic/history dates; if the stats appear inherited, copied, or unrelated, ignore them and say so.

If a bot/settings read returns signature, API key, signed URL, secret binding, or other sensitive material, do not quote it. Note "sensitive fields were present and omitted" and continue with redacted evidence.

Use generated retrieval/search endpoints carefully. If an Admin MCP operation or generated OpenAPI operation is marked as `sideEffect: write`, treat it as a write-like verification step and do not run it during read-only judging unless explicitly authorized.

If work remains outside MCP, provide the exact dashboard link and the minimum instructions: connect OAuth, select files, paste secret, approve Slack install, or upload local files.
