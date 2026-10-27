# Role2Reel Public

**Character-driven stories, purposeful shots, and complete camera-aware video prompts.**

[中文](README.md) · [Install](docs/installation.md) · [Examples](#see-the-output) · [Evidence](EVALS.md) · [Download](https://github.com/niuyupeng/role2reel-public/releases/latest)

A standalone **Codex Skill** for writers and AI filmmakers. Start from a character clue, screenplay, storyboard or approved prompt. It enters at the stage you need, preserving decisions already made.

| Starting material | Workflow | Deliverable |
|---|---|---|
| Script and established designs | Asset-first production, internal shot planning | Per-segment assets, complete timed prompts and trim ranges |
| Approved storyboard or prompt | Camera/execution enrichment | A full revised prompt with dialogue and timing preserved |
| Sparse character clues | Several possible fictional pasts | Distinct readings for the author to select, change or reject |
| Scene/dialogue draft | Knowledge, relationship and playable behavior | Natural action and necessary speech, including purposeful repetition |

## Start here

In Codex:

```text
$skill-installer Install the skill at the root of https://github.com/niuyupeng/role2reel-public with the name role2reel-public.
```

Invoke `$role2reel-public` on your next turn. If it is not discovered, check the installation path and open a new conversation. The ZIP and manual Git routes are in [installation](docs/installation.md). Keep the entire skill folder together.

Try this complete text-only request; no project initialization or reference photos are required:

```text
$role2reel-public
Give me a compact three-shot storyboard in English, totaling 9 seconds.
A florist at a plain table lifts the only empty vase and says, "Still empty."
Her friend replies, "Still empty." Both laugh, then she sets the vase down.
Preserve both lines exactly, no other dialogue or new props, natural room sound,
no music or captions. This is a quick text board for discussing the scene.
We have no photos or formal production documents yet.
```

Expected shape: a readable three-shot table totaling nine seconds, both lines assigned correctly, one vase, and completed placement. Missing photos should be stated rather than invented. This is a discussion draft, not a production lock or a verified performance.

## See the output

- [English compact board: the empty vase](docs/examples/compact-board.md) — actual output for the request above.
- [Two complete video prompts: the repair-room key](docs/examples/camera-segments.md) — Chinese input/output; 12 editorial seconds from two 8-second generated clips, each trimmed to 6 seconds. Asset roles, focus, lens, aperture, action and trim instructions stay inside a copyable segment.
- [Three possible pasts: a postal worker and returned letter](docs/examples/life-paths.md) — Chinese input/output; known facts remain distinct from fictional proposals and author choices.

[Trial records](docs/text-trials-2026-10-27.md) identify the source revisions, original outputs, review criteria and limits. These are a small set of actual text trials, not cross-model statistics or film-quality validation.

## Working principles

- Protect approved source dialogue, identity, duration and story facts.
- Establish perception, space and cause before reactions and results.
- Match camera choices to framing, scale, distance and depth of field; brand names are not genres.
- Separate individual shots from multi-shot generation segments and separate footage length from editorial length.
- Assign each reference an explicit purpose; asset existence, inspection, approval and provider binding are different facts.
- Preserve author choice in fictional life-path exploration. Formal persistent contracts are available when needed; a compact draft does not require fabricated hashes.

The skill also supports music-IP/MV planning, visual character assets, covers and scoped video repair through [specialized routes](references/workflow-routing.md). It does not initiate images for a text-only character request.

## Requirements and boundaries

Text work needs a Codex environment that can read local skills. Optional scripts require Python 3.11+; YAML checks also require PyYAML. See [tooling](docs/development.md). File, image and video delivery depends on tools actually available in the host. This repository does not bundle model credits or a video-generation service.

The CI matrix checks software on Windows/Ubuntu and Python 3.11/3.13. Text trials support only their disclosed review scope. No new image, audio or video quality result is claimed; see [EVALS](EVALS.md).

Public name and directory: `role2reel-public`. It installs independently of any internal `role2reel` edition. Keep projects outside the installation folder; updates and uninstall must not remove your scripts or media. **Do not use initializer `--force` to add a character:** it resets managed templates, including existing drafts. See the safer options in [tooling](docs/development.md).

Private project material, conversations and credentials stay outside this repository. [Contribute a reproducible failure](CONTRIBUTING.md), [report security issues](SECURITY.md), or inspect [third-party attribution](THIRD_PARTY_NOTICES.md). Package version: [VERSION](VERSION). [MIT licensed](LICENSE); no affiliation or endorsement by OpenAI, ByteDance or the referenced projects.
