# Copy-paste shot prompt contract

First select the user's export format. This document's fixed five-field syntax applies when a per-shot clipboard export or the corresponding workbook profile is requested. For assets → concise storyboard → complete multi-shot segment prompt → editing-interval notes, use [segmented-prompt-delivery.md](segmented-prompt-delivery.md): preserve those four sections and do not force one prompt per shot or five-field blocks. A completed segment prompt declares its total planned generation duration, lead/core/tail media intervals, recommended retained interval, global editorial interval and contiguous local shot/action time ranges from zero to the end of its generated media. Use the four prompt headings specified by that profile; authorized editing handles belong to the generated media and do not automatically count toward the final cut. Its copyable prompt remains a complete text block, separate from its preparation list, concise table and editing notes.

This is the completed production-export contract. If inputs required for the selected task are missing, such as a source clip, approved text, actual edit timing or reference bindings, return a clearly labeled planning draft and the smallest needed input instead. An untimed, provider-neutral repair draft is valid at that stage; do not invent seconds, media tokens or capability verification merely to fill the final format. A text-only generation task does not require an edit source merely because an editing task would.

## Separate preparation from the executable block

When the user wants asset instructions before each segment, list actual required files/tokens, their roles and any missing input outside the copyable prompt. Keep tool-dependent reference bindings and the visual facts required for generation inside the executable task; separating the upload checklist must not remove the bindings. Include only references this segment uses. Each independent call carries its own applicable identity, space, voice, audio/text rules and boundary state; a prior chat message or “same as above” is not provider memory.

For sequential delivery, provide the requested segment while retaining its place in the approved plan; a request for segment 4 does not authorize a new segment 1. When the user asks for one combined prompt, preserve intentional cuts and local-to-global timing. One submission is not one continuous take. Check the current interface's limits; do not relabel a multi-shot montage as a one-shot scene or squeeze speech and movement to fit an assumed cap.

## Shot syntax

For the selected per-shot clipboard profile, every block uses this order:

```text
shot1｜
景别与运镜：
拍摄方式：
画面与动线：
【00:01-00:05】:（拍摄机位）（具体画面内容）
```

The local `shotN` label may restart inside each provider generation segment, while a project workbook keeps the original stable shot ID separately. When several segment prompts are concatenated for review, mark that export as allowing local restarts; a single segment must still have increasing labels. Time-code lines are ordered, non-overlapping, and contiguous within the block. Use one-based display time (`00:01`) when the delivery contract says so; store numeric seconds in the timing plan. In a per-shot clock the first time line begins at the declared display origin; when preserving an upstream segment-relative clock, declare that offset and keep it consistent rather than silently renumbering the source. Every end must be greater than its start, and the last end must equal the block's editorial duration when the block is on a per-shot clock.

`景别与运镜` names shot scale and motivated camera behavior. `拍摄方式` declares the practical or generated capture method, including any long-generation/short-trim instruction. `画面与动线` describes observable blocking, screen direction, state change, sound-relevant action, and the ending handoff. Time-coded lines describe atomic beats, not a prose summary or a list of intentions.

Keep nonverbal beats when the audience can read them. Do not add dialogue merely to fill a time range. If dialogue is present, preserve natural breath and listener reaction. If an action contains contact or force, show cause, approach, contact, result, and recovery across the current block or an explicitly linked neighboring block.

Within the existing fields, identify each audible line by speaker and exact authorized text. Separate spoken dialogue or approved narration from subtext, delivery analogies and action notes; quotation marks around an acting example do not authorize speaking it. Recaps supplied only to orient the generation are context, not audible; explicitly scripted recaps or replays remain bound to their assigned text and interval. Keep future lines outside the executable block until their assigned interval. Explicitly approved internal narration remains audible; an author's requested nonverbal ending must not acquire an explanatory line.

No placeholder, unbound character, invented asset, unexplained reference-image inheritance, or unresolved hard timing conflict may enter a production-locked block. The mechanical auditor checks syntax, timing continuity, duplicate labels, and obvious unfinished text; it cannot judge whether the image is good, the actor is playable, or the story meaning is preserved.
