# Dynamic shot timing

Dynamic timing is a production contract, not a fixed-length formatting trick. Estimate each shot from what the audience must be able to see, hear, understand, and feel, then keep the editorial cut length separate from the provider's generation length.

## Three clocks

- **Performance clock**: the time a person, object, line, reaction, or camera move needs to happen credibly.
- **Editorial clock**: the time the finished cut holds the shot. It may include a readable reveal, a reaction, a transition, or a deliberate hold.
- **Provider clock**: the duration requested from a video model. It may be longer than the editorial shot and later trimmed; it must never stretch a short action into a different dramatic event.

When the user requests editing handles outside the final cut, count the leading and trailing handles in the generated-media duration only. Declare the total generation length, lead/core/tail media intervals, recommended retained interval and its global editorial interval. Natural dynamic handles are often 1–2 seconds at each end, but their length follows the action and editing need rather than a fixed template. Complete all protected action, dialogue and necessary reaction inside the core; the handles must be genuinely removable without deleting the story. Do not use black frames, freeze frames or repeated frames as substitutes. The user-confirmed final runtime is the sum of retained editorial intervals, not the sum of raw generated clips. Permission for longer source media is not permission for a longer final film.

Never impose a universal 3-second, 5-second, or provider-default shot length. A shot can be shorter than a model's minimum generation duration when the delivery record explicitly declares long-generation/short-trim. A long spoken thought or physical consequence must not be compressed merely to fit a template.

## Hard floor

For each shot, record the following lower bounds in seconds:

1. `dialogue_floor`: measured or estimated natural speech plus breath where audible;
2. `action_floor`: prepare or judge → approach → contact/trigger → force/state change → recovery/end;
3. `visual_floor`: enough time to identify space, subjects, text, or a decisive prop;
4. `camera_floor`: time for the declared pan, track, rack, crane, or reveal to complete;
5. `performance_hold`: comprehension, involuntary response, or aftermath that would otherwise be cut off.

Calculate `hard_floor` from the longest causal path through the scheduled beats: add steps that cannot overlap, and take the longer path only for duties that actually run in parallel. Do not add the same reaction or hold twice when it is already included in an action estimate. The maximum of the five category bounds is a lower-bound check, not proof that several sequential duties fit. Record the schedule and overlap assumptions in `timing_beats` and `timing_reason`. Use:

`recommended_duration = hard_floor + rhythm_slack + evidence_adjustment`.

If the requested target is below the hard floor, emit `DURATION_INFEASIBLE` and propose a narrow repair: shorten the duty, split the shot, change the camera task, or move information to a neighboring shot. Do not silently speed-ramp dialogue or erase the result of contact.

## Beat and relation fields

Declare whether dialogue, action, visual reveal, and reaction are `sequential`, `parallel`, `mixed`, `voiceover`, or `none`. State the shot's beat duty and its `state_in`/`state_out`. A slow reveal may have no dialogue; a dialogue shot may stay on the listener. Add `REACTION_MISSING`, `READABILITY_TOO_SHORT`, `ACTION_UNDERCRANKED`, `DIALOGUE_TOO_FAST`, `SPLIT_RECOMMENDED`, or `RELATION_UNCLEAR` when the evidence shows a risk.

## Faster rhythm with the same total duration

An explicitly user-confirmed final-cut duration is a hard constraint. Do not expand the final cut without the user's explicit change, including when the original source called that duration approximate. Authorized removable generation handles can extend the source media while leaving this editorial duration unchanged. An initial timing estimate or added blocking detail does not authorize a longer final artifact. First use genuinely parallel speech/action, causal editorial ellipsis, and removal of redundant holds or unnecessary staging; preserve the protected story and exact dialogue. Do not time-stretch audio, mechanically accelerate delivery, or swallow words to force a fit. If an irreducible conflict remains, identify its exact causal path and propose the smallest adjustment instead of silently changing the final runtime.

Lock the requested total and protected events first. Budget their credible causal paths, then reclaim time from duplicated information, unnecessary lead-ins or holds that no longer serve the scene. Reallocate that time to readable action details, reactions or a deliberate pause after a fast passage. Do not shorten every shot equally or equate more cuts with better rhythm. Dialogue may overlap an action only when the performance and meaning allow it; a trigger still precedes its result.

Protected events include purposeful verbal callbacks and requested nonverbal aftermaths; do not reclaim their time merely because words repeat or nobody speaks. For long lists or dense dialogue, time a read-through in the intended delivery, including articulation and meaningful pauses, or label the duration as an estimate. A segment heading's claimed seconds are not timing evidence. An added movement followed by speech changes the causal floor; recompute the local schedule and the whole-film total rather than preserving the old duration by assertion.

Add cuts only when requested or within the editing scope and when each cut has a clear duty. Keep the event order and state handoffs; a montage of mechanism details must still explain how the object reaches its usable state. Map inserted/split shots to stable source IDs, apply the atomic-shot gate, then sum actual editorial intervals on one numeric timeline. A one-based display label is not an extra second of footage. Include transitions, readable final holds and any other occupied intervals in that same total. If the necessary duties still exceed it, report the specific conflict and offer a scoped tradeoff instead of hiding missing steps behind “fast.”

## Evidence and calibration

Keep the source evidence visible. Use these weights only as priors, never as automatic truth: `final_cut 1.00`, `director_approved 0.85`, `edited_accepted 0.70`, `planned 0.25`, `rejected 0.00`. A user-uploaded planned or re-estimated board is useful evidence but is not a final-cut measurement. Mark low evidence as `CALIBRATION_LOW_EVIDENCE` and request human confirmation for production lock.

## Timing handoff

The timing plan owns editorial duration, generation duration, floors, evidence, flags, and confidence. The paste-ready prompt owns only the executable shot description and time-coded beats. The downstream provider adapter may choose a compliant generation duration and trim plan, but may not rewrite plot, character behavior, shot duty, or upstream timing rationale.

Use [copy-paste-prompt-contract.md](copy-paste-prompt-contract.md) for the fixed Chinese output shape and [workbook-delivery-profile.md](workbook-delivery-profile.md) for the spreadsheet layout.
