# Using Role2Reel Public

[English home](../README.en.md) · [Installation](installation.en.md) · [Optional tools](development.en.md)

Start with the material you already have. A short scene can be written in the conversation; an approved prompt can receive camera detail without being rewritten. You do not need to initialize a project, create biographies or run Python before either task.

Invoke `$role2reel-public`, provide the source or an accessible file, and say what should be delivered. Name the choices already settled: dialogue and speaker, story outcome, character identity, duration, shot boundaries, camera basis, sound restrictions and output format. If something is not settled, say so. The skill should distinguish a reversible production assumption from a change that requires the author's decision.

The examples on this page are **suggested requests and explanatory specifications**, not recorded model runs. Actual outputs and their review limits are linked separately below.

## 1. Script → assets → complete generation segments

Use this route when you want to prepare references first, then receive complete prompts without reviewing an internal shot table.

### First delivery: a usable asset plan

Supply the script and whichever existing references you can actually provide:

```text
$role2reel-public
Use the attached script as the current source. First give me the characters,
locations, props and necessary sound references needed for the whole story.
For each item, state its role, what can be reused, what is missing and a complete
image-making prompt only where a new image is needed. Reuse the approved
character identities; do not redesign them or create an expression pack by default.
This turn is planning only; do not generate or upload media.

Final film: [duration]. Approved dialogue and speaker: [source/file].
Aspect ratio and camera basis: [existing choices, or say they are undecided].
Sound: [allowed dialogue, ambient sound, music/narration/caption rules].
Available references: [actual files and their approved uses].
Image delivery target: [actual width × height, if relevant].
```

An asset entry should tell you what to make or select. For example, a character identity reference can preserve face, body proportions and established clothing; a location reference can establish doors, table placement and light direction; a prop reference can establish shape, count and initial state. A reference's unrelated pose, background or decorative text does not automatically belong in the film.

One picture may cover several duties if those duties are explicit. A four-view sheet is one character or object shown from several angles, not four people or four units of stock. A reference library is not an instruction to put every item in every shot.

If actual image work is requested and the host has suitable tools, the assistant can create or edit the missing assets, open the results and report specific defects. Otherwise it should deliver the plan and identify the missing tool or file. An image prompt, proposed filename or scheduled task is not a generated image. A requested 2K/4K output needs an agreed pixel size and checks of the actual file; a label alone does not establish resolution or realism.

### Second delivery: segments ready to copy as text

After making or selecting references, provide the actual files and the role of each:

```text
$role2reel-public
Continue from the same script and these selected assets. Plan shots internally;
do not add a shot-by-shot approval stage. Give each generation segment in this order:
its required assets, one complete copyable prompt, and the trim instructions.
Keep the approved dialogue, story, editorial duration and identities.
Use natural asset names in the prose unless the selected provider requires syntax.
Allow [specified] extra footage handles outside the final duration.
Deliver [editable Word / Markdown / conversation text].
These are local references; no provider upload or binding has happened yet.
```

Replace the bracketed fields with your choices; omit fields that are already clear from the supplied source. Do not invent approval or upload status to fill them.

The assistant should organize **narrative parts → shots → generation segments**. A segment can contain several shots and usually covers one or two related narrative parts. Shot count is not generation count. Do not split every shot into a separate task just to fill a template, or add cuts to an already approved single shot.

Each complete segment prompt should contain:

1. Its planned footage duration, local time origin, retained interval and final-film placement; the starting character and prop states; shared camera and sound rules.
2. **Front editing handle** — natural movement before the required event, with no indispensable dialogue or action hidden there.
3. **Core story and internal shots** — continuous local shot times, who does what to whom, exact lines and speakers, visible cause/contact/result, and camera choices in the same prose.
4. **Tail editing handle** — natural breathing, gaze or settling after the key action and final word have finished.
5. **Story-state handoff to the next segment** — what has already happened and what the next segment can assume. This is a continuity instruction, not another generated shot.

Use those four functional section headings even when translating the output. Put trim instructions after the complete prompt. If Word is requested, place the whole prompt under its own heading in editable ordinary paragraphs, rather than splitting the action and parameters across table cells. If you request a shot table, each real cut gets a row; the table and prose must use the same times.

Handles belong inside the first and last shot when the camera continues unchanged. They should not introduce black frames, freeze frames or extra cuts merely to fill time. A segment should finish its local event: complete the transfer, contact result or line before the tail window. The next segment can re-establish the scene from a stable state without reproducing the previous clip's exact end pose.

### Keep footage time and final-film time separate

Suppose the approved film lasts 12 seconds and has two six-second segments. You authorize one extra second at each end of each generated clip:

| Segment | Generated footage | Front handle | Core and recommended keep | Tail handle | Final-film placement |
|---|---:|---|---|---|---|
| G01 | 8 s | 0–1 s | 1–7 s | 7–8 s | 0–6 s |
| G02 | 8 s | 0–1 s | 1–7 s | 7–8 s | 6–12 s |

The plan produces 16 seconds of footage and uses 12 seconds in the edit. These are illustrative durations, not a provider capability claim or a universal segment size. Every clip's shot intervals cover its complete local timeline from 0 to 8 seconds, including handles. A cut at final-film time 9 seconds becomes local time `9 − 6 + 1 = 4` seconds in G02. Required actions stay inside the retained window.

If the locked content does not fit, the assistant should identify the specific timing conflict and smallest possible change for your decision. It should not silently enlarge the film, delete a locked line, accelerate speech or claim a provider accepts an unverified duration.

## 2. Approved prompt → camera and execution enrichment

Use this route when the story and segmentation are already settled:

```text
$role2reel-public
Enrich the attached approved prompts in place. Preserve every line, speaker,
segment, cut, time interval, action result and character identity. Do not rebuild
the story, regenerate assets or add shots. Keep the existing camera system.

Put the common camera basis at the start of each complete segment. Inside each
timed shot, add only missing framing, focal length, working aperture, focus/depth
of field, camera position/movement and motivated lighting. Label estimated
distances. Give one workable camera choice per shot, not a menu.
Return complete revised prompts in [format], with the existing asset lists and
trim instructions. If a locked choice conflicts with the action, flag that exact
conflict instead of silently replacing it.
```

For a first pass, the default **simple** camera treatment is enough: framing/task, actual focal length and sensor basis, aperture, primary focus and required depth, position/movement and the result the shot must show. Request **enhanced** treatment when you also need a specific body/mode, frame rate, shutter, ISO starting point and white balance. These are working intentions and estimates; they are not measured EXIF, proof of a hardware setup or guarantees of model control.

Camera choices follow the viewing task:

| Shot's job | What needs to remain readable |
|---|---|
| Establish a relationship | Actor, target, route and relevant surroundings; enough depth for the relationship |
| Show an emotional response | Eyes and face, with speech visible when needed; no distracting focus jumps to background lights |
| Show a hand/foot/paw operation | Contact point, support and completed physical result; distant scenery need not be equally sharp |
| Show a prop state | The relevant surface, orientation, opening or change; do not invent contents or damage |

The same focal length can make different framings at different distances. A close-up does not imply one mandatory lens, and camera brands are not genre rules. Preserve the effective sensor area and distinguish actual from equivalent focal length. Do not rename an f-number as a T-stop. A locked-off camera can follow focus without becoming a tracking shot.

Lighting should have a source and match the approved place. Correct plastic-looking fur, uniform gloss or impossible shadows on the actual image when image editing is requested; adding more camera words to a prompt does not establish that the image was fixed. Do not introduce rain, haze, furniture or neon solely to create a cinematic label.

## 3. A small story or dialogue task

You can ask for a scene directly:

```text
$role2reel-public
Write a compact scene in English, about half a page. Two adult siblings are
closing their repair shop. Mira has decided to leave; Tomas knows only that she
has packed her tools. She wants him to ask, but will not announce it unprompted.
Use only the workbench and existing tool roll. End when he makes room beside him
and she sits. No new emergency, new visitor, flashback or speech explaining their
entire history. This is an exploratory draft; propose details only within this scene.
```

Expect playable actions, attention, pauses and lines shaped by what each person can know. A purposeful repeated line, joke or long speech can remain; natural dialogue does not mean deleting everything that fails to deliver new plot information. If a line is locked, the skill preserves it. If you ask only for typo correction, it should not convert the task into dramatic rewriting.

For an uncertain fictional past, ask for several possibilities first:

```text
$role2reel-public
From these established fictional facts, propose three different possible pasts.
For each, separate what is known from what you propose, explain the present
behavior it would support, and say what remains unexplained. Include a serious
counter-reading. Do not choose, rank or approve a path for me.
Facts: [your fictional facts]. World constraints: [your story material].
```

You can select, alter, combine compatible parts, reject all or retain uncertainty. Selecting a path and asking for a biography permits a draft; it does not mean you have approved every new fact in that draft. Formal canon-bound projects can record exact source versions and separate biography approval. Ordinary exploratory writing does not require you to fabricate approval hashes or fill a full production schema. Fictional possibilities are not evidence about a real person's hidden life.

## Continuity checks that change the result

For interaction scenes, the assistant should check a compact set of facts internally, then fix the actual prompt rather than giving you only an audit report:

| Check | Practical question |
|---|---|
| Role and speaker | Is this the same established person, and does only the assigned speaker say the protected line? |
| Knowledge and perception | Did this character actually hear or see the cue before reacting? Could the target be hidden from their position even though the camera sees it? |
| Prop state | How many physical objects exist, who holds each, where is it supported, and what state is it in? Moving one from table to hand does not reduce the total count. |
| Space and direction | Are positions, doorways, routes, axis and movement directions understandable? A new viewpoint does not move furniture. |
| Contact and result | Is grasping, transferring, opening or setting down completed visibly where the source requires it? Does sound occur at the actual contact? |
| Between cuts | If routine preparation was omitted, are the old end state and new starting state clear without replaying the event? |
| Segment handoff | Has the local event ended, and does the next segment begin from what is now true without borrowing future knowledge? |

Keep story facts distinct from reference properties. A material sample does not establish how many props exist or who owns them. Furniture visible in a style reference does not automatically belong in the story's location. A person looking toward another room has not moved into it.

## Reference, approval and execution are separate facts

| Evidence available | Accurate statement | What it does not establish |
|---|---|---|
| Written requirements | Asset planned | File created |
| Openable file | File exists at this version | Visual quality or user approval |
| Recorded visual inspection | Named properties were inspected | Every dimension passed, or the user approved it |
| Explicit user approval | This version and use were approved | Future edits inherit approval |
| Selected file in the actual provider input | Bound for that execution | An unselected local path was uploaded, or quality passed |
| Examined generated video | Stated dynamic properties were checked | Other versions, models or scenes will work |

Do not create new approval checkpoints merely because these distinctions exist. Preserve approval the author actually gave, state which checks occurred and continue within the authorized work. Missing references can still permit a clearly labeled text draft; they cannot support a claim that a provider-bound generation package is complete.

## Troubleshooting the handoff

| Symptom | Useful correction to request |
|---|---|
| The result is a parameter table only | “Put those choices back into every timed shot and return each complete copyable segment.” |
| Every shot became a separate video task | “Keep internal shots, but group complete local events into generation segments without changing approved cuts or duration.” |
| A fixed close-up now contains invented cuts | “Preserve the approved continuous shot; describe action phases inside it.” |
| The film grew because handles were added | “Restore the locked editorial total; list footage, keep ranges and film placement separately.” |
| A character reacts too early | “Identify the first available visual or audible cue and move only the unapproved reaction detail after it.” |
| The model promises nonexistent assets or uploads | “Report actual files and tool actions separately from planned assets; mark the missing inputs.” |
| A provider rejects the planned duration or mode | “Check that provider's current interface; show the incompatibility and a source-preserving option before changing the plan.” |
| A generated result fails | Supply the exact executed prompt, selected references, mode and failed output. Ask for a scoped diagnosis; don't attribute an old failure to a prompt that was never executed. |

For discovery, package, dependency and update problems, use [installation](installation.en.md) and [optional tooling](development.en.md).

## Inspect complete examples and evidence

- [The empty vase](examples/compact-board.md): an actual compact English storyboard output.
- [Workshop handoff](examples/workshop-handoff.md): the complete English complex-case artifact, with its input, provenance and limits. Consult the [complex trial record](complex-trials-2026-10-27.md) for what was executed and reviewed.
- [The repair-room key](examples/camera-segments.md): an actual Chinese two-segment prompt output; 16 seconds of generated-footage planning yields 12 editorial seconds.
- [Postal worker and returned letter](examples/life-paths.md): actual Chinese fictional-path exploration, leaving the choice with the author.

[Evaluation status](../EVALS.md) separates software checks, text trials and pending media/production evidence. Example text being complete does not mean images or video were generated, references bound, or a film approved.
