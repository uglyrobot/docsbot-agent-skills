# Admin MCP Operation Reference

Use Admin MCP `search` before `execute`. The exact schemas can change; this file records stable operation names and field guardrails verified against the DocsBot Admin MCP catalog and local code.

## Entry Points

| Task | Operation ID | Notes |
| --- | --- | --- |
| List accessible teams | `get_teams` | First call in most workflows. OAuth identifies a user, not a fixed team. |
| Get team details | `get_teams_teamid` | Use after choosing `teamId`; responses are sanitized. |
| List bots | `get_teams_teamid_bots` | Use to find existing bots and avoid duplicates. |
| Get bot settings | `get_teams_teamid_bots_botid` | Read before updating; preserves existing settings and action config. |
| Create bot | `post_teams_teamid_bots` | Requires `name`; for agent bots include valid `agentPrompt`. |
| Update bot | `put_teams_teamid_bots_botid` | Use minimal bodies containing only intended settings. |
| Delete bot | `delete_teams_teamid_bots_botid` | Destructive except research-job mode. Confirm unless the user already explicitly authorized that exact deletion. |

## Bot Creation Guardrails

Observed live behavior on 2026-07-03:

- `language` must be the inferred DocsBot locale key for the bot's primary answer language, such as `en`, `es`, or `jp`; do not send natural-language names like `English` or browser locale strings like `en-US` unless the live catalog explicitly supports them.
- Choose `language` before `post_teams_teamid_bots` from user instructions, source/documentation language, website/help-center language, and brand analysis. If those signals conflict, ask before creating the bot instead of defaulting to English.
- Omit `model` during normal bot creation so the API uses the current DocsBot default. Set `model` only when the user explicitly requests a specific supported model or the workflow requires one and you have verified it is allowed by the team plan.
- Omit rate-limit and IP-recording fields during normal bot creation: do not send `rateLimitMessages`, `rateLimitSeconds`, `rateLimitIPAllowlist`, or `recordIP` as `null`, `false`, `0`, empty string, or empty array. The API treats defined values as writes; omitting the keys preserves the default/null state, matching onboarding-style creation.
- `isAgent: true` requires `agentPrompt` during create. The prompt must include the literal string `search_documentation`.
- Default create can enable `human_escalation` and `followup_rating`; inspect the created bot before replacing `tools`.
- Bot create/update responses can include inherited analytics plus bot signature material. Never quote secrets, signature keys, or large history payloads in user-facing output.
- Public bots force `tools.web_search.live` to `false` on update.
- `tools.customButtons[]` entries must include `enabled`, `name`, `functionKey`, `instructions`, `buttonText`, `icon`, and `url`; saved function keys do not include the internal `button_` prefix.
- `leadCollect.mode` must be `before_response` or `before_escalation`; field keys must be unique. Standard+ supports custom fields beyond `name` and `email`.
- `leadCollect.fields[].options` for select fields may be normalized on save; verify saved option labels before handoff and prefer simple option labels when exact spacing matters.

Good create skeleton:

```json
{
  "name": "Acme Support Bot",
  "description": "Answers product and support questions for Acme customers.",
  "privacy": "public",
  "language": "en",
  "region": "US",
  "isAgent": true,
  "agentPrompt": "<closest exact prompt asset with placeholders filled and minimal additions>"
}
```

Onboarding-style create shape intentionally does not include `rateLimitMessages`, `rateLimitSeconds`, `rateLimitIPAllowlist`, `recordIP`, `allowedDomains`, or similar safety/limit toggles. Configure those later only when the user explicitly asks or the deployment has a concrete requirement, and then verify the saved bot read.

For final-product builds, use `post_teams_teamid_bots` plus explicit follow-up updates. Do not invoke adjacent demo-bot skills, public demo/pilot endpoints, or onboarding bot creation endpoints as the primary build path; those can create scaffolded source titles, broad auto-sources, copied demo analytics, or disposable naming. If an onboarding/demo endpoint is used only to inspect suggested branding or source ideas, clean up all scaffold artifacts before handoff: rename/delete rough sources, assign all tags, remove demo/test naming, and clearly identify any source still pending/indexing in the final handoff.

## Compact Field Map

Use this to map skill language to common `put_teams_teamid_bots_botid` and source fields. Search the live catalog for full schemas before unusual writes.

| Skill concept | Field(s) |
| --- | --- |
| Public/private bot | `privacy: "public"` or `"private"` |
| Agent mode | `isAgent: true`, `agentPrompt` containing `search_documentation` |
| Locale/language | `language` locale key inferred before creation, such as `en`, `es`, `jp`; verify live catalog support for uncommon locales |
| Brand color/logo/header | `color`, `logo`, `icon`, `botIcon`, `headerAlignment`, `brandAnalysis` |
| First message/starter questions/labels | `labels.firstMessage`, `questions`, other `labels.*` |
| Support/contact route | `supportLink`; helpdesk widget handoff uses embed `supportCallback` outside MCP |
| Public safety | `linkSafetyEnabled`, `piiRedaction`, `recordIP`, `imageUploads`, `audioUploads`, `allowedDomains`; omit from initial create unless explicitly configuring |
| Retrieval tags | `retrieverTags: [{ key, description }]`, source `tags: ["key"]` |
| Source freshness | source `scheduleInterval` as `monthly`, `weekly`, `daily`, or `none` when supported |
| Lead form | `leadCollect`, `labels.leadCollectMessage` |
| Human escalation/follow-up rating | `tools.human_escalation`, `tools.followup_rating` |
| Scheduling tools | `tools.calendly`, `tools.calcom`, `tools.tidycal` with `{ enabled, instructions, url }` |
| Custom buttons | `tools.customButtons[]` with `{ enabled, name, functionKey, instructions, buttonText, icon, url }` |
| Web search | `tools.web_search` with `{ enabled, live, allowed_domains }` |
| Stripe customer billing | `tools.stripe` with `recent_billing`, `billing_portal`, `refund`, `cancellation` subkeys |
| External MCP servers | `mcpServers[]` with `serverLabel`, `serverUrl`, `serverDescription`, `enabled`, `tools`, optional auth/header fields |
| Help Scout prompt | `helpscoutPrompt` |

Preserve existing `tools`, `mcpServers`, `labels`, and `retrieverTags` entries when updating one part of the bot.

## Branding And Onboarding

| Task | Operation ID | Notes |
| --- | --- | --- |
| Analyze website | `post_teams_teamid_bots_analyze` | Takes `siteURL`; returns suggested bot config, brand colors/logos, screenshot, language, support/widget hints. Does not create a bot. |
| Draft prompt | `post_teams_teamid_bots_botid_prompt` | Use `activeTab: "agent"` for agent prompts. Review before persisting with bot update. |
| Debug prompt | `post_teams_teamid_bots_botid_prompt_debug` | Use when current behavior is off; persist accepted edits with bot update. |
| Bot image upload URL | `get_teams_teamid_bots_botid_image_upload_url` | Signed upload URL plus public `cdnUrl` for widget `logo`, `icon`, or `botIcon` images. Upload bytes to `uploadUrl`, then save `cdnUrl` in bot settings. |
| Suggest source tag | `post_teams_teamid_bots_botid_retriever_tags_suggest` | Drafts tag key/description; save accepted tags through bot update. |
| Draft custom button | `post_teams_teamid_bots_botid_custom_button_draft` | Drafts metadata only; add `url` before saving in `tools.customButtons`. |

After `post_teams_teamid_bots_analyze`, persist the returned analysis into bot create/update as `brandAnalysis: { domain, url, ...analysisResult }` along with selected `color`, `logo`, `widgetType`, and `supportLink`. Saved `brandAnalysis.colors` and `brandAnalysis.logos` power dashboard brand presets and discovered bot icons; omitting the field is a configuration defect. If live MCP schema search or execution rejects `brandAnalysis`, flag the Admin MCP/API mismatch and use dashboard/onboarding or propose a helper endpoint rather than dropping the field.

## Sources

| Task | Operation ID | Notes |
| --- | --- | --- |
| Add source | `post_teams_teamid_bots_botid_sources` | URL/file/website/sitemap/RSS/Q&A/cloud connector source creation. |
| List sources | `get_teams_teamid_bots_botid_sources` | Supports pagination and tag filters. |
| Get source | `get_teams_teamid_bots_botid_sources_sourceid` | Inspect status and normalized fields. |
| Count source status | `get_teams_teamid_bots_botid_sources_counts` | Useful after queuing ingest. |
| Count source tags | `get_teams_teamid_bots_botid_sources_tag_counts` | Confirms tag assignment totals. |
| Map website URLs | `post_teams_teamid_bots_botid_sources_map` | Discovers candidate URLs before website source creation; usually finds quickly accessible top-level/obvious links, not every URL. Prefer sitemaps for complete docs/KB/product coverage. Observed source create needs root `url` plus selected `urls`. |
| Bulk update source tags | `post_teams_teamid_bots_botid_sources_tags` | `sourceIds`, plus `set` or `add`/`remove`; max 100 source IDs. |
| Signed file upload URL | `get_teams_teamid_bots_botid_upload_url` | MCP cannot upload bytes; upload with HTTP PUT, then create a single-file document source using returned `file`, or derive a shared pending batch prefix for multi-file `fileDir`. |
| Draft source title | `post_teams_teamid_bots_botid_source_title_draft` | Optional helper for naming uploaded multi-file batches from filenames. |
| Rename source label | `patch_teams_teamid_bots_botid_sources_sourceid` | Dashboard label only for supported source types. |
| Retry failed ingest | `put_teams_teamid_bots_botid_sources_sourceid` | Only for failed sources, not general editing. |
| Reingest source | `post_teams_teamid_bots_botid_sources_sourceid_reingest` | Queues reingest where source type/status allows. |
| Schedule refresh | `put_teams_teamid_bots_botid_sources_sourceid_reingest` | Sets `scheduleInterval`, including `none`. Important web sources should default to monthly refresh when scheduling is supported. |
| Download source archive | `get_teams_teamid_bots_botid_sources_sourceid_download` | Signed download URL for source archive; use only when export/download is requested. |
| Download source file | `get_teams_teamid_bots_botid_sources_sourceid_download_file` | Signed URL for one source file; do not print signed URLs unless user explicitly needs the download link. |
| Export Q&A source | `get_teams_teamid_bots_botid_sources_sourceid_export_qa` | Exports Q&A source content. |
| Delete source | `delete_teams_teamid_bots_botid_sources_sourceid` | Source must be ready/failed, not indexing. |

If a source cannot be renamed and has a scaffold title such as `undefined Website` or `undefined Sitemap`, replace it with an explicitly named source. If a broad scaffold sitemap is still indexing, do not build final-product scope around it; narrow the prompt or replace it with curated ready sources.

`get_teams_teamid_bots_botid_upload_url` is for source files only. Do not use its returned signed URL, `file`, or `user/{userId}/team/{teamId}/bot/{botId}/...` path for widget `logo`, `icon`, or `botIcon` settings. Use `get_teams_teamid_bots_botid_image_upload_url` for widget branding image uploads; see [branding/widget.md](branding/widget.md).

Source tags are two-step:

1. Define bot vocabulary with `retrieverTags` on `put_teams_teamid_bots_botid`.
2. Assign keys on source create via `tags`, or later through `post_teams_teamid_bots_botid_sources_tags`.

Prefer defining tags before source creation when products, editions, major versions, regions, or same-audience procedure families differ. This lets each sitemap, website, URL-list, document, or connector source carry the correct `tags` value from creation instead of requiring repair later. Do not use tags for public/internal or customer/staff isolation; create separate bots and source sets instead.

## Integrations, Actions, MCP, Skills

| Task | Operation ID | Notes |
| --- | --- | --- |
| List team integrations | `get_teams_teamid_integrations` | Read before connect/configure. Use `type=helpscout` or `type=slack` when relevant. |
| Connect/reconnect integration | `put_teams_teamid_integrations` | Primarily Help Scout via `type`, `appID`, `appSecret`; confirm secrets out of band. |
| Configure Help Scout | `post_teams_teamid_integrations_helpscout` | Assign tags/mailboxes to bots; set note/save/publish behavior. |
| Refresh Help Scout | `post_teams_teamid_integrations_helpscout_refresh` | Poll/list after refresh. |
| Slack authorize URL | `get_teams_teamid_integrations_slack_authorize` | User must complete OAuth outside Admin MCP. |
| Read Slack workspaces | `get_teams_teamid_integrations_slack` | Returns sanitized workspace routing and bot/channel mappings. |
| Update Slack routing | `patch_teams_teamid_integrations_slack` | Sets `defaultBotId`, `channelBotMap`, and `adminsOnly` per workspace. |
| Disconnect Slack workspace | `delete_teams_teamid_integrations_slack` | Requires `slackTeamId`; destructive integration change, confirm first outside disposable tests. |
| List Slack bot mapping | `get_teams_teamid_integrations_slack_bots` | Use before selecting bot for Slack. |
| List bot webhooks | `get_teams_teamid_bots_botid_webhooks` | Read configured outgoing subscriptions before create/update/test. |
| Create bot webhook | `post_teams_teamid_bots_botid_webhooks` | Supports `lead.created`, `conversation.escalated`, `conversation.rated`, and `deep_research.done`. |
| Get bot webhook | `get_teams_teamid_bots_botid_webhooks_webhookid` | Verify a specific webhook by id. |
| Update bot webhook | `patch_teams_teamid_bots_botid_webhooks_webhookid` | Update label, status, target URL, events, or expiration. |
| Delete bot webhook | `delete_teams_teamid_bots_botid_webhooks_webhookid` | Destructive; confirm before deleting non-test hooks. |
| Preview webhook payloads | `get_teams_teamid_bots_botid_webhooks_perform_list` | Returns sample payloads without delivery. |
| Test lead webhook | `post_teams_teamid_bots_botid_webhooks_deliver_lead` | Sends sample or selected lead payload. |
| Test escalation webhook | `post_teams_teamid_bots_botid_webhooks_deliver_escalated` | Sends `conversation.escalated` sample payload. |
| Test rating webhook | `post_teams_teamid_bots_botid_webhooks_deliver_rated` | Sends `conversation.rated` sample payload. |
| Test research webhook | `post_teams_teamid_bots_botid_webhooks_deliver_research` | Sends `deep_research.done` sample payload. |
| Start bot Stripe OAuth | `post_teams_teamid_bots_botid_stripe_oauth_authorize` | Returns a Stripe authorization URL for bot customer-billing tools, not DocsBot account billing. |
| Discover external MCP tools | `post_teams_teamid_bots_botid_mcp_discover` | Use when the server is reachable or discovery supports the auth mode. If OAuth or private credentials are required, user must connect/authorize in dashboard. |
| Draft MCP metadata | `post_teams_teamid_bots_botid_mcp_server_draft` | Draft safe server metadata and tool selection before saving in `mcpServers` with bot update. |
| List bot skills | `get_teams_teamid_bots_botid_skills` | Includes missing bindings and enablement state. |
| Search library skills | `get_teams_teamid_bots_botid_skills_library` | Search by vendor/task keywords. |
| Import library skill | `post_teams_teamid_bots_botid_skills_library_libraryskillid_import` | Creates a bot draft from a global library skill. |
| Read published skill settings | `get_teams_teamid_bots_botid_skills_id_settings` | Secret values are never returned. |
| Configure published skill | `patch_teams_teamid_bots_botid_skills_id_settings` | Operational settings only: `enabledWidget`, declared env/secret bindings. |
| Read worker logs | `get_teams_teamid_bots_botid_skills_workers_logs` | Useful after enabling a skill. |

Admin MCP may expose broader skill authoring operations, but for normal bot setup prefer library import plus published skill settings. Do not create or edit arbitrary skill source files unless the user explicitly asks to build a new DocsBot Skill.

## Verification, Tuning, And Access

Search the live catalog before using these because filters and payloads vary:

| Task | Operation ID | Notes |
| --- | --- | --- |
| Retrieval OpenAPI | `get_teams_teamid_bots_botid_openapi` | Verify search schema and source-tag enums for external retrieval handoff. |
| Test semantic retrieval | `post_teams_teamid_bots_botid_search` | Search bot knowledge with optional tags; catalog marks this write-like, so use only when verification is authorized. |
| List question logs | `get_teams_teamid_bots_botid_questions` | Use for behavior tuning; do not treat inherited demo logs as evidence. |
| Search question logs | `post_teams_teamid_bots_botid_questions_search` | Semantic search over historical questions. |
| Update saved answer | `put_teams_teamid_bots_botid_questions_questionid` | Writes curated Q&A/answer feedback; confirm before changing real bot history. |
| List conversations | `get_teams_teamid_bots_botid_conversations` | Use for escalation/lead/chat behavior diagnostics. |
| Get conversation | `get_teams_teamid_bots_botid_conversations_conversationid` | Full transcript details. |
| List leads | `get_teams_teamid_bots_botid_leads` | Verify lead capture after tests. |
| Export leads | `get_teams_teamid_bots_botid_leads_export` | Returns signed CSV URL; use only when requested. |
| Delete lead | `delete_teams_teamid_bots_botid_leads_leadid` | Destructive privacy cleanup. Confirm unless disposable test data. |
| Bot stats/reports | `get_teams_teamid_bots_botid_stats`, `get_teams_teamid_bots_botid_reports` | Diagnostics only; avoid inherited demo analytics as quality proof. |
| Team members | `get_teams_teamid_members` | Resolve members/invites before access changes. |
| Invite member | `post_teams_teamid_invite` | Invite or bot-scoped access; write action, confirm first. |
| Update team member | `put_teams_teamid_members` | Role change; write action, confirm first. |
| Bot member override | `put_teams_teamid_bots_botid_members` | Per-bot role override; verify with bot/member reads. |

DocsBot account billing operations such as add-ons, subscription changes, Stripe portal sessions, and cancellation are out of scope for ordinary bot setup. Use them only when the user explicitly asks to manage the DocsBot team subscription, and always follow preview/confirm and explicit-approval requirements from live MCP search.

## Useful Deep Links

Use these in handoff once `botId` is known:

- Dashboard chat: `https://docsbot.ai/app/bots/{botId}/chat`
- Bot system settings: `https://docsbot.ai/app/bots/{botId}/configure/system`
- Agent instructions: `https://docsbot.ai/app/bots/{botId}/configure/instructions`
- Sources: `https://docsbot.ai/app/bots/{botId}/configure/sources`
- Widget actions: `https://docsbot.ai/app/bots/{botId}/widget/actions`
- Widget design: `https://docsbot.ai/app/bots/{botId}/widget/design`
- Skills: `https://docsbot.ai/app/bots/{botId}/configure/skills`
- Webhooks: `https://docsbot.ai/app/bots/{botId}/configure/webhooks`
- MCP connections: `https://docsbot.ai/app/bots/{botId}/configure/mcp-connections`
- Help Scout integration: `https://docsbot.ai/app/api#helpscout-integration`
- Slack integration: `https://docsbot.ai/app/api#slack-settings`
- Public share/demo pattern: inspect current dashboard routes or bot response before promising a share URL; do not invent a URL if unsure.
