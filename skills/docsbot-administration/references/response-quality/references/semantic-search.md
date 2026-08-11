# Semantic Search Debugging

Use Admin MCP `post_teams_teamid_bots_botid_search` to test what the bot's indexed training data returns for a query. This is the same retrieval surface the dashboard Search UI uses next to Chat. It is the primary tool for debugging retrieval rank, missing index coverage, tag filters, and whether a source is actually searchable after ingest.

Catalog may mark this operation as a write because it proxies/embeds; it does not mutate bot settings or sources.

## When To Run It

- After reading a bad question log: compare live hits to the logged `sources` context.
- When a source was just added, reingested, or marked ready: confirm chunks are findable.
- When diagnosing tag routing: search with and without `tags` / `include_untagged`.
- When a user says "the answer is in our docs but the bot misses it": prove whether retrieval fails or generation fails.
- After adding a Q&A pair: confirm the FAQ text ranks for realistic phrasings.

## Request Shape

Search the live catalog before execute. Stable body fields:

| Field | Purpose |
| --- | --- |
| `query` | Required search text. Prefer `standaloneQuestion` from the log, then the raw user question, then paraphrases. |
| `top_k` | How many matches to return. Use ~5 to mimic default chat context; raise to 10–20 when checking whether the right chunk exists but ranks below the default window. |
| `tags` | Optional retriever tag keys. Use when the bot routes by product/version/procedure. |
| `include_untagged` | When tags are set, defaults to including untagged sources unless explicitly `false`. |
| `autocut` | Optional API autocut; use only when diagnosing score cutoffs. |
| `alpha` | Optional hybrid weighting when relevant to the bot embedding setup. |
| `use_glossary` | Optional glossary expansion. |

Example bodies to try for one incident:

```json
{ "query": "<standaloneQuestion or user question>", "top_k": 5 }
```

```json
{ "query": "<same>", "top_k": 16 }
```

```json
{ "query": "<same>", "top_k": 10, "tags": ["<tagKey>"], "include_untagged": false }
```

```json
{ "query": "<paraphrase a customer would type>", "top_k": 5 }
```

## Debug Matrix

Run a short matrix instead of a single lucky query:

1. **Logged standalone question** at `top_k: 5` — closest to what chat likely used.
2. **Raw user question** at `top_k: 5` — catches rewrite/standalone issues.
3. **Same query at higher `top_k`** (10–16) — detects "present but below context cutoff."
4. **One or two paraphrases** — detects brittle wording / missing Q&A coverage.
5. **Tagged vs untagged** when `retrieverTags` exist — detects wrong product/version routing.
6. **Expected document title/URL phrase** as a query — if even that fails, the source is not indexed/searchable yet (failed ingest, zero chunks, wrong bot, or non-text content).

Record for each run: whether the expected source/chunk appears, its approximate rank, and whether chunk text actually contains the fact.

## How To Read Results

| Observation | Interpretation |
| --- | --- |
| Expected chunk in top 5 and was in logged `sources`, but answer was still wrong | Context-present / prompt / model issue — not indexing |
| Expected chunk in top 5 live, missing from logged `sources` | Time skew (source added later), different query rewrite, or tag/filter difference at answer time |
| Expected chunk only appears at high `top_k` | Increase context items and/or clean noisy higher-ranked sources; consider Q&A so the fact ranks easily |
| Expected chunk absent for all phrasings | Missing/failed/unreadable source or still indexing |
| Wrong product/version chunks dominate | Tag routing or noisy overlapping sources |
| Title/URL query finds nothing for a "ready" source | Inspect that source status/chunk counts; reingest or replace |

Do not claim indexing is healthy from source `status` alone. Semantic search is the proof that chunks are retrievable.

## Tie-Back To Logs

Always pair search debugging with the question log:

1. Read logged `sources` (what the model actually got).
2. Reproduce with `post_teams_teamid_bots_botid_search`.
3. If needed, list/get the suspected source for status, page/chunk counts, and type.
4. Only then choose remediation: reingest/source fix, Q&A, tags, context items, or prompt/model.

## After A Fix

Re-run the same query matrix after Q&A create/merge or source reingest. If the source is still indexing, say verification is pending and retest once chunk counts are non-zero. Prefer realistic customer phrasings over only the exact FAQ question string.
