# Seedance long-form prompt compilation

Use when the author requests one detailed prompt for a complete multi-shot clip, especially with supplied audio and an explicit text budget. This extends, rather than replaces, the provider adapter, copy-paste shot contract, music clocks and source/atomicity gates.

## Three independent limits

Record the product surface, visible model/version, generation duration and prompt counter separately. A large text field does not establish a longer video capability. An API limit does not prove the consumer editor's limit. Identify whether a displayed budget counts characters, UTF-16 code units, bytes or tokens. If unknown, report the chosen local counting method and leave headroom; never call 15,000 tokens 15,000 Chinese characters.

Treat a user-reported interface limit as user-provided context until inspected or matched to a current primary source. Provider-specific numbers stay dated and surface-scoped. A community skill's model line must not become a limit for another line. Keep the author's requested complete sequence as one deliverable; if the selected service cannot render it in one call, state that conflict outside the creative prompt rather than silently shortening the story or promising a nonexistent mode.

## First pass: complete the direction

Bind the source audio interval and reference roles before expanding prose. For a source song, preserve the recording, lyric order, rests and tail; do not estimate phrase timing by distributing characters across the target duration. Forced alignment is an estimate and can force nonexistent words into a crop. Check coverage and endpoint separately. Missing listening evidence permits a labeled editorial plan, not claims of verified lip synchronization.

Build the smallest complete event sequence: opening state, main action, contact or discovery, response, result and next-shot state. Choose cuts for new information or a changed viewing task. One prompt may contain multiple explicitly cut shots; do not label it a one-take scene. A montage may change locations when authorized, while preserving identity and indicating deliberate cuts instead of accidental background mutation.

For each shot, state what is visible from the actual camera location, the main motion, relevant light sources, acting target, active speaker or singer and the end state. Keep position, facing, prop ownership and unresolved movement across cuts. Distinguish stable identity from changing expression and costume accessories. Describe animal speech with its actual anatomy; masks and helmets cannot be both opaque and reveal lips. Do not ban the requested singing to simplify the task.

The source image carries visible details. Add prose for discriminating identity anchors, permitted changes, motion and likely ambiguities, rather than exhaustively describing every pixel. Use short reinforcement at genuinely risky cuts; do not repeat a complete global rulebook under every shot.

## Second pass: compile and normalize

Deliver one coherent block when requested. Inside that block retain the established `shotN｜`, `景别与运镜：`, `拍摄方式：`, `画面与动线：` structure. Maintain one declared global timeline across shots, not repeated local zeroes. Explicit time ranges describe the editorial plan; verify how the current provider interprets them before calling them enforced model controls. Do not copy restrictions on timestamp syntax from an older model line without rechecking.

Normalize in this order:

1. **Source and scope:** only the requested interval; exact authorized words; no future clip instructions hidden in the current prompt; separate supplied facts from authored staging.
2. **Media binding:** identify each real attachment and what it controls; keep character sheets out of ordinary first-frame roles; do not invent UI tokens. If exact tokens are unknown, use unambiguous descriptive attachment names and label routing as awaiting binding.
3. **Clock consistency:** planned windows are ordered and cover the requested clip without overlap or gaps. The source audio remains one continuous clock. Do not move sung words to make the camera schedule appear accurate.
4. **Physical and performance consistency:** no simultaneous contradictory cameras, unexplained prop transfers, masked lip-sync, duplicate characters, missing contact results or reactions before their cues.
5. **Prompt economy:** remove alternative takes, analysis, internal IDs, rationales, duplicate adjectives, failed experiments and contradictory negatives from the executable text. A long prompt should add observable distinctions, not new simultaneous tasks in every second.
6. **Budget and endpoint:** count the actual final block, including headers, punctuation and whitespace. Check the final pose and sound handoff. Report its measured length and review status outside the copyable block.

An upper limit is not a universal quota. When the author explicitly asks for a near-limit detailed version, honor that requested deliverable and use the budget for material choices, action mechanics, spatial handoffs and performance distinctions; do not silently substitute a brief prompt. Do not claim greater length proves better rendering. If a full plan is shorter than the budget, state the actual count rather than padding or inventing a claimed count.

## Release and focused repair

Run the existing text-format auditor, then separately check cross-shot continuity and the whole-clip clock. Passing syntax or a character counter is not audio listening, dynamic video review or user acceptance. Record unknown interface controls and unverified audio timing without burying them in boilerplate. Only a returned video can demonstrate that the model obeyed the cuts, mouth movements and object interactions.

On failure, repair the observed dependency: reference conflict, ambiguous action, overloaded shot, audio crop, scene geography or unsupported operation. A larger negative list or longer prompt is not the default repair. Do not overwrite unrelated project assets or install/execute a researched third-party skill without authorization.

## Research used, and limits

Reviewed on 2026-10-02; independently summarized methods, not copied prompt templates:

- [ByteDance agentkit prompt-to-video example](https://github.com/bytedance/agentkit-samples/blob/main/skills/byted-ind-ecom-prompt-to-video/SKILL.md): separate conditioning media and actual operation parameters; its 2.0-era numerical examples are not universal limits. No scripts executed.
- [Emily2040 multi-shot grammar](https://github.com/Emily2040/seedance-2.0/blob/main/references/multishot-grammar.md) and [prompt compiler](https://github.com/Emily2040/seedance-2.0/blob/main/references/prompt-compiler.md): distinguish one submission from one take and isolate the current clip from future material. Authored shot-load heuristics and version-specific restrictions were not adopted as established facts.
- [Emily2040 literal direction notes](https://github.com/Emily2040/seedance-2.0/blob/main/references/direct-for-the-model.md): use observable performance and readable prop contact. Do not impose its per-shot action count or word-for-word repetition as universal rules.
- [Official Seedance 2.5 prompt guide](https://docs.volcengine.com/docs/ark/seedance-2-5-prompt-guide?lang=zh): use current first-party guidance when choosing long-clip and reference modes; check the actual host interface separately.

These sources inform prompt construction, not a measured comparison of video quality. Project-specific songs, characters, files, generated prompts and audit logs remain outside the general skill.
