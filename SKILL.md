---
name: role2reel-public
description: Develop fictional characters and natural dialogue, turn scripts into purposeful storyboards, and deliver asset-aware timed video prompts with matched camera choices. Use for 人物小传、命线反演、对白改写、分镜、资产规划、摄影参数快补 and AI video direction. Supports optional music-IP and visual-asset workflows; not generic copyediting or factual profiling of real people.
---

# Role2Reel Public

Build the person, make the scene playable, then design the shots. Enter at the stage the user supplies: an approved prompt needing camera parameters does not need a new biography or screenplay.

This independent public skill is invoked as `$role2reel-public`. Keep its directory separate from internal `role2reel` installations. Use project context supplied for this task; do not import sibling skills or internal history merely because they exist locally.

## Choose the requested output

Identify the artifact and protected source before drafting. A screenplay, compact storyboard, full multi-shot segment prompt and visual asset are different outputs; Word or Excel selects the container, not the content. Read [output contracts](references/output-contracts.md) when format matters.

- Preserve approved dialogue, speaker, duration, shot boundaries, story facts and identities unless the user authorizes a change. Execution detail must serve the existing event.
- Use the narrowest matching route below and read only the relevant references. Do not run the whole pipeline for a small revision.
- Text-only tasks can proceed with declared missing assets. Image creation or provider execution requires the requested workflow and available tools; a reference filename is not an uploaded or inspected asset.
- Use the requested language and delivery format. Ask one focused question only when an unresolved choice would change the story, author decision or execution mode; otherwise label a reasonable reversible assumption.

## Common routes

| Request | Read and apply | Deliver |
|---|---|---|
| Existing script/prompt, only add camera and execution detail | [Parameter enrichment](references/asset-first-production.md#已有稿与词库的参数快补), [camera matching](references/shot-camera-matching.md) | Complete revised prompt with parameters inside each timed shot; preserve content and timing |
| Assets first, internal shot planning, direct segmented handoff | [Asset-first production](references/asset-first-production.md), [segment contract](references/segmented-prompt-delivery.md) | Needed assets → complete timed prompt → trim ranges; keep the internal table out unless requested |
| Multi-shot segment prompts with a compact table | [Segmented delivery](references/segmented-prompt-delivery.md) | Narrative parts containing shots; several shots may share one generated clip |
| Simple/professional storyboard or shot-list repair | [Storyboard](references/storyboard.md), [source truth](references/source-truth-gate.md), [atomic shots](references/atomic-shot-gate.md) | Motivated cuts with readable space, causes, reactions and results; choose compact or persistent contract appropriately |
| Scene or dialogue writing | [Scene/dialogue](references/scene-dialogue.md), [prose craft](references/story-prose-craft.md), [natural dialogue](references/natural-dialogue-repair.md) | Playable behavior and necessary lines; read [character engine](references/character-engine.md) when character knowledge or judgment needs work |
| Faithful cleanup of rough notes, interview or narration | [Humanization](references/humanization.md) | Preserve authorship, uncertainty and meaning; do not turn typo-only cleanup into dramatic rewriting |
| Several possible fictional pasts from sparse present clues | [Life-path exploration](references/fatecasting.md), [life-path contracts](references/life-paths.md), [character engine](references/character-engine.md) | Distinct plausible paths for the author to choose; keep proposals separate from established facts |
| Build or repair an established character/biography | [Character engine](references/character-engine.md), [growth review](references/biography-growth-review.md); for prose also [prose craft](references/story-prose-craft.md) | Requested character material; no automatic visual asset pack |
| Plan or create image assets from a script | [Script-to-assets](references/script-to-assets.md), [shot references](references/shot-reference-planning.md) | Scoped asset plan, or actual images only when requested; inherit approved identity and verify actual dimensions |
| Camera, focus, lighting or scene geography | [Camera matching](references/shot-camera-matching.md), [cinematography](references/cinematography-lighting.md); for spatial drift [spatial layout](references/spatial-layout-design.md) | One coherent camera/lighting basis, shot-specific focus and lens choices, physically usable space |
| Adapt references to a named video mode/provider | [Video adapters](references/video-adapters.md); for Seedance [provider guidance](references/providers/seedance.md) | One selected mode, explicit reference duties and exclusions; verify current provider capabilities when they matter |
| Audit, calibration or evaluation | [Quality gates](references/quality-gates.md), [evaluation status](EVALS.md) | Evidence, concrete defects and scope of verification; no artistic score from lint results |

For music IP/MV, posters/covers, visual character packs, local video repair, audio continuity, whitebox experiments, series learning, title work or project-memory organization, use the matching entry in [extended routing](references/workflow-routing.md). A request to create a fictional character in text does not imply a request for images. An existing fictional universe also needs [world grounding](references/world-grounding.md) before inventing history.

## Protect the story and physical event

1. **Facts, proposals and knowledge differ.** Preserve the source's uncertainty and the limits of each character's perception. A character reacts only after the cue is available to them. Do not promote a proposed past to canon or invent an author decision.
2. **Behavior before explanation.** Let memory, relationship and current risk shape what the person does or withholds. Use the mute pass to diagnose redundant exposition while preserving dialogue with a character, relationship, rhythmic, comic or lyrical purpose. Do not remove locked source dialogue.
3. **Cuts need an audience task.** Establish the relevant geography, then make contact and result visible. Maintain identity, direction, prop count/ownership and known events. Multiple beats within one continuous shot, multiple shots within one segment, and multiple segments within a story are separate levels.
4. **Keep the clocks separate.** Lock the editorial duration. Generated footage may include separately authorized natural handles. Shot intervals must cover the full generated timeline without gaps or overlap; selected trim lengths must sum to the locked final duration. A provider limit does not authorize rewriting the source.
5. **Parameters are working intentions.** Match framing, subject scale, effective sensor area, distance, focus and depth of field before choosing focal length/aperture. Preserve the selected camera basis. Do not treat a camera brand as a genre or a number in a prompt as measured EXIF, hardware control or visual proof.
6. **References carry only named properties.** Identity, wardrobe, pose, background, camera, sound and style are separate responsibilities. Multi-view sheets do not multiply characters or inventory. Preserve task-specific bans on music, subtitles, narration and additional dialogue; a restriction from one project is not a universal style rule.

For source-bound production or formal CharacterOS/life-path compilation, read the relevant sections of [production contracts](references/production-contracts.md). They preserve explicit author choice, separate path lock from exact-biography approval, and bind persistent artifacts to actual source revisions. Compact drafts do not need fabricated hashes or a new approval process. A production lock is a different evidence claim from a useful draft.

## Complete the handoff

Deliver the requested artifact first. Use the selected segmented contract for full prompts; do not replace it with the per-shot clipboard schema. Keep editable text together so the user can copy a whole generation segment without assembling fragments from several tables.

Resolve bundled scripts relative to this `SKILL.md`, not the user's current directory. Script selection and their limits are in [production contracts](references/production-contracts.md#use-the-included-resources). Initialize user projects outside the installed skill directory and preserve existing files. A project is not required for a one-off text request.

Before delivery, cross-check source dialogue, timestamps, asset roles, focus and final states across the output. Report independently what was planned, actually generated, visually inspected, explicitly approved, bound to an input or tested as dynamic video. Tests and validators check their declared contracts; they do not prove natural acting, cinematic quality or platform success.

## Maintain and publish

For skill edits, branch consolidation or exports, read [maintenance](references/skill-maintenance.md) and [publication boundary](references/publication-boundary.md). Keep private scripts, company information, media, credentials, research and raw conversations outside this repository. Public and internal editions update independently; review reusable improvements individually rather than synchronizing whole directories.
