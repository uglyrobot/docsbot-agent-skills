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

On authorization, use the advertised `update_bot` schema to write only the intended prompt field. For nested voice configuration, fresh-read and preserve unrelated settings if the API requires a whole map. Saving through the bot API creates an instruction history entry. Read back both the bot and newest version; report exactly which channel changed.

For restoration, call `list_instruction_versions`, paginate with nextCursor when needed, and inspect before/after values. A saved version's after text is the saved state; before means undo that edit. Preview the target text, scope `fields` to the intended channel, and call `restore_instruction_version` with `expectedCurrent` set to current values. A 409 means someone changed the instructions: read the new state and reconsider; do not retry blindly. Restoring creates another history entry and must not change unrelated voice or agent settings.

Evals snapshots can restore the captured text for that run. Do not describe a text-only Evals run as a voice test. Verify restored/improved voice instructions with representative phone and widget conversations, including silence, interruptions, escalation, and enabled actions when those are relevant to the change.


## Bring agent changes into voice

For the dashboard `sync-voice-instructions` workflow, the source is `agentPrompt` and the only destination is `voiceAgent.instructions`. Fresh-read both current prompts, recent instruction history, authoritative business policies, and channel-specific tool availability. Use agent history to understand changes, then compare their meaning with current voice instructions; do not assume that every agent edit belongs in voice or that a missing sentence is an omission.

Identify applicable policies, behavior rules, and escalation guidance missing or outdated in voice. Adapt these for spoken interaction, avoid duplicating rules already present, and preserve deliberate voice-specific choices: short turns, one question at a time, confirmation, interruption handling, transfer and end-call rules, and differences between phone and widget tools. Do not import web-only presentation, unsupported tools, markdown, or instructions to read long URLs. Highlight contradictions for review rather than silently overriding voice intent.

Present a focused voice-only diff with what carries over, what stays, and what needs a decision. If there are no applicable changes, report that without saving a duplicate version. Reuse explicit authorization for the reviewed change. Before applying, fresh-read again and reconsider if either prompt changed. Update only voice instructions through the normal bot update contract, preserving all unrelated voice settings and the entire agent prompt. Read back the saved instructions and new history entry. Do not claim this establishes call quality without representative voice checks.
