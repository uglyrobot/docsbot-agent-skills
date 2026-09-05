# Improve and restore instructions

Choose the exact surface that produces the behavior:

| Surface | Stored field | Check |
| --- | --- | --- |
| Chat agent | agentPrompt | Website/API agent answer |
| Legacy instructions | customPrompt | Legacy bot behavior |
| Help Scout | helpscoutPrompt | Ticket drafting and replies |
| Voice | voiceAgent.instructions | Phone and widget spoken behavior |

Read current bot instructions, related source facts, enabled channel tools, and relevant history. If the user has unsaved dashboard edits, do not overwrite them: review the draft as evidence and have them save or discard before applying a persisted change. Ask about the desired behavior only when it cannot be inferred.

For improvement, preserve useful existing rules and propose a focused before/after change tied to the actual failure. Do not put missing business knowledge into invented policies. For voice, use short spoken turns, one question at a time, explicit confirmation of names/numbers/transfers, tool wait acknowledgments, and no visual-only markdown or URL reading. Phone and widget action availability differ; verify the actual enabled tools before naming them.

On authorization, use the current bot update contract to write only the intended prompt field. For nested voice configuration, fresh-read and preserve unrelated settings if the API requires a whole map. Saving through the bot API creates an instruction history entry. Read back both the bot and newest version; report exactly which channel changed.

For restoration, search `instruction version history`, paginate with nextCursor when needed, and inspect before/after values. A saved version's after text is the saved state; before means undo that edit. Preview the target text, scope `fields` to the intended channel, and submit `expectedCurrent` with current values. A 409 means someone changed the instructions: read the new state and reconsider; do not retry blindly. Restoring creates another history entry and must not change unrelated voice or agent settings.

Evals snapshots can restore the captured text for that run. Do not describe a text-only Evals run as a voice test. Verify restored/improved voice instructions with representative phone and widget conversations, including silence, interruptions, escalation, and enabled actions when those are relevant to the change.
