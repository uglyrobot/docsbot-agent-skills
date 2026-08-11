# Response Quality Operation Reference

Use Admin MCP `search` before `execute`. Schemas can change; this file records stable operation names and field guardrails for log analysis and response-quality fixes.

## Entry Points

| Task | Operation ID | Notes |
| --- | --- | --- |
| List bots | `get_teams_teamid_bots` | Resolve `botId` when current context is missing. |
| Get bot settings | `get_teams_teamid_bots_botid` | Prompt, model, tags, tools, privacy, labels. |
| List question logs | `get_teams_teamid_bots_botid_questions` | Filters: `couldAnswer`, `escalated`, `rating`, `startDate`/`endDate`, `page`, `perPage`, optional `ip`. |
| Semantic search question logs | `post_teams_teamid_bots_botid_questions_search` | Body requires `query`. Useful for topic clusters across history. Catalog may mark this a write because it embeds the query. |
| Mark question revised | `put_teams_teamid_bots_botid_questions_questionid` | After creating/merging the Q&A FAQ, set `{ "revised": true }` so the log shows as corrected. |
| Delete a question log | `delete_teams_teamid_bots_botid_questions_questionid` | Destructive; confirm unless already authorized. |
| List conversations | `get_teams_teamid_bots_botid_conversations` | Filters include resolved/escalated/IP as supported. |
| Get conversation transcript | `get_teams_teamid_bots_botid_conversations_conversationid` | Full multi-turn history for dialogue-dependent answers. |
| Delete a conversation | `delete_teams_teamid_bots_botid_conversations_conversationid` | Destructive; confirm unless already authorized. |
| Semantic search training data | `post_teams_teamid_bots_botid_search` | Primary retrieval debugger. See [semantic-search.md](semantic-search.md). |
| List sources | `get_teams_teamid_bots_botid_sources` | Coverage, types, tags, status. |
| Get one source | `get_teams_teamid_bots_botid_sources_sourceid` | Inspect FAQs for `qa`, page/chunk evidence, failures. |
| Create/merge Q&A or other source | `post_teams_teamid_bots_botid_sources` | For revise-answer: `type: "qa"` + `faqs: [{ question, answer }]`. A second qa source may merge into the existing one and queue reingest. |
| Update Q&A FAQs | Live-search the QA update/patch operation | Replaces/merges FAQs and queues reingest; verify with catalog search. |
| Update bot settings | `put_teams_teamid_bots_botid` | Prompt, model, tags, tools. Minimal bodies; preserve unrelated settings. |
| Bot report / stats | `get_teams_teamid_bots_botid_reports` and related stats ops from search | Aggregate quality before deep dives. |

## Question Log Fields That Matter

When reading question objects, prefer evidence in this order:

1. `sources` — chunks actually supplied as model context for that answer.
2. `standaloneQuestion` — rewritten query used for retrieval when present; use it for semantic search reproduction.
3. `question` / `answer` — what the user asked and what the bot said.
4. `couldAnswer`, `rating`, `escalated` / `escalation` — outcome signals.
5. `conversationId` — read the linked conversation and use only its top-level `channel` to select the prompt surface. Do not infer channel from question or conversation metadata.
6. `revised` — `true` when the revise-answer workflow already created/merged a Q&A item for this log.

Do not dump entire source chunk arrays into the user reply. Summarize titles/URLs and quote the few lines that prove the diagnosis.

## Revise Answer → Q&A (durable)

Dashboard **Revise answer** improves future responses by writing a Q&A source, then flagging the log:

1. `post_teams_teamid_bots_botid_sources` with:

```json
{
  "type": "qa",
  "scheduleInterval": "none",
  "faqs": [
    {
      "question": "<standalone or clarified question>",
      "answer": "<corrected answer>"
    }
  ]
}
```

2. `put_teams_teamid_bots_botid_questions_questionid` with `{ "revised": true }`.

| Goal | Use |
| --- | --- |
| Explain a past answer | Question + conversation reads + semantic search |
| Correct future answers for a known logged Q | Q&A source create/merge, then mark `revised: true` |
| Add missing knowledge broadly | New/updated non-QA sources |
| Change tone, refusals, escalation copy | Prompt / `agentPrompt` update |
| Improve extraction when context already contains the answer | Stronger model, clearer prompt, or more context items |

Never mark `revised: true` alone when the user wants better future answers—the Q&A `faqs` write is what trains retrieval.

## Semantic Search Guardrails

Full matrix and interpretation: [semantic-search.md](semantic-search.md).

- Operation: `post_teams_teamid_bots_botid_search` on the same bot that produced the log.
- Start with `standaloneQuestion` when present; also try the raw user question and paraphrases.
- Use `top_k: 6`, the Semantic Search default, to reproduce the default window; raise to 10–16 to see if the chunk exists but ranks low.
- When retriever tags exist, compare unrestricted vs `tags` + `include_untagged: false`.
- For proprietary names, acronyms, industry terms, or non-standard translations, compare the exact same query with `use_glossary: false` and `true`; see [glossary.md](glossary.md).
- Failed, zero-chunk, or still-indexing sources explain missing retrieval even when the public URL looks correct.
- Do not conclude "indexed fine" from source status alone—require a successful semantic search hit.

## Dashboard Deep Links

When navigation is available, prefer these pages after diagnosis:

| Page key / path pattern | When |
| --- | --- |
| `bot_questions` → `/app/bots/{botId}/configure/questions` | Review logs the user should inspect |
| Bot chat / search UI | Manually verify retrieval for a query |
| `bot_sources` → configure/sources | Missing, failed, or Q&A source work |
| Configure / system (prompt) | Prompt or model changes |
| Configure / glossary | Cross-language, brand, acronym, or industry-term query rewriting |
| Widget / API docs links in product docs | `contextItems` / `context_items` for embed or API callers |

Never invent IDs. Use IDs returned by MCP or the current page context.
