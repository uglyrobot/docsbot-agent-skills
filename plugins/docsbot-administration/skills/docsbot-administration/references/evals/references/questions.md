# Build useful questions

1. Read the bot and selected question set. Preserve existing case IDs, categories, notes, required actions, and scoring settings. Use the append operation for a single addition; a set update replaces cases, so fresh-read before composing the entire payload.
2. Inspect relevant indexed sources. For history-based tasks, inspect a bounded sample of recurring, poorly rated, unanswered, or escalated conversations. Remove names, account identifiers, secrets, and other personal details. A previous bot answer is evidence of behavior, not an authoritative expected answer.
3. Cover realistic common questions, known failures, ambiguous/edge cases, useful paraphrases, and action requirements. Prefer a small useful first set over filler. Avoid near-duplicates and questions the knowledge cannot answer reliably.
4. Write a natural customer question, a concise source-backed expected answer, and optional evidence notes. Expected answers should express the necessary meaning, not require exact phrasing. Where policy is missing, surface the gap or test appropriate uncertainty rather than inventing facts.
5. Use the supported categories: common, known_failure, edge_case, action_needed, paraphrase. Preserve other tags. Require only actions actually enabled for the tested channel, using catalog/tool IDs from current bot configuration. Do not add action assertions to every case merely to raise coverage.
6. Present additions/edits for review with question, expected behavior, category, and any required action. Clarify substantive unknowns. On authorization save through Evals CRUD, then read back the exact set. Do not start a run automatically unless authorized.

Search for `Evals question sets` and inspect create/read/update/append contracts. Supported promptTarget values are agent and helpscout. Voice instruction work is separate. A set supports up to 250 cases; keep IDs when editing and avoid silently dropping cases at the limit.
