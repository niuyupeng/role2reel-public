# Role2Reel Public

**Turn characters, scripts and approved storyboards into playable scenes and complete video prompts.**

[中文](README.md) · [Install](docs/installation.en.md) · [English usage guide](docs/usage.en.md) · [Evidence](EVALS.md) · [Downloads](https://github.com/niuyupeng/role2reel-public/releases)

[![Validation](https://github.com/niuyupeng/role2reel-public/actions/workflows/validate.yml/badge.svg)](https://github.com/niuyupeng/role2reel-public/actions/workflows/validate.yml) [![MIT](https://img.shields.io/badge/license-MIT-317873.svg)](LICENSE)

A standalone **Codex Skill** for writing, shot planning and AI-video preparation. Enter at the stage you need. An approved prompt needing lens and focus choices does not need a new screenplay; a small dialogue draft does not need a production database.

| What you have | What to ask for | What you receive |
|---|---|---|
| A script and established designs | Assets first, then internal shot planning | Relevant assets → complete timed prompt → trim ranges for each generation segment |
| Approved shots or segment prompts | Camera and execution enrichment | Complete revised prompts preserving dialogue, timing, cuts, identity and action results |
| A scene or dialogue draft | Playable behavior, knowledge and relationship work | Actions and speech shaped by what each character can know and wants to change |
| Sparse fictional character clues | Several possible pasts | Distinct proposals for the author to select, change, combine or reject |

## Install and try a small task

In Codex, if the built-in installer is available:

```text
$skill-installer Install the skill at the root of https://github.com/niuyupeng/role2reel-public with the name role2reel-public.
```

Invoke `$role2reel-public` on the next turn. If it is not discovered, check the actual installation directory and open a new conversation. [Installation](docs/installation.en.md) covers `CODEX_HOME`, manual/Git and release ZIP options, checksum verification, updates, rollback and removal. Keep the entire skill folder together.

Try this text-only request; no photos, Python or project initialization are needed:

```text
$role2reel-public
Give me a compact three-shot storyboard in English, totaling 9 seconds.
A florist at a plain table lifts the only empty vase and says, "Still empty."
Her friend replies, "Still empty." Both laugh, then she sets the vase down.
Preserve both lines exactly, no other dialogue or new props, natural room sound,
no music or captions. This is a quick text board for discussing the scene.
We have no photos or formal production documents yet.
```

Expect a readable three-shot table totaling nine seconds, correctly assigned lines, one vase and a completed placement. The absent photos should be acknowledged without inventing files or preventing a discussion draft. See the [actual compact English output](docs/examples/compact-board.md) and its disclosed limits.

## From a script to a usable handoff

The [English usage guide](docs/usage.en.md) gives complete request templates and explains all three common entry points. For asset-first production:

1. Provide the current script, protected decisions and actual reference files. Receive the whole-story asset list and any needed image-making prompts. Approved character identities are reused.
2. Make or select the required assets with the tools you choose, then provide the actual files and their intended uses. A plan is not an image; a local file is not a provider upload.
3. Receive each segment's relevant assets, one complete copyable prompt and precise trim instructions. Shot planning remains internal unless you ask to see it.

A segment can contain several shots. Its prompt includes the shared camera and sound basis, local shot times, action, exact dialogue/speaker, camera changes, focus and physical results. Four functional sections describe the front editing handle, core story/internal shots, tail editing handle and story-state handoff. Key actions finish before the tail window; the next segment starts from a clear state without requiring a frame-perfect pose match.

Keep **generated-footage time** separate from **editorial time**. Two clips generated for eight seconds each and trimmed to seconds 1–7 provide twelve seconds of finished film. Extra handles do not authorize enlarging a locked film. Camera numbers are working intentions, not proof that a provider reproduced the optics or acting.

If Word is requested, the full prompt belongs in ordinary editable paragraphs so it can be copied in one selection. Word delivery, image creation and video execution depend on the host's available tools; the repository does not bundle those services or model credits.

## Complete examples

- [Workshop handoff — English complex case](docs/examples/workshop-handoff.md): complete input and artifact involving multiple characters, rooms and prop ownership. The [complex trial record](docs/complex-trials-2026-10-27.md) reports execution, revisions and review limits.
- [The empty vase — English compact storyboard](docs/examples/compact-board.md): a small discussion draft with protected repetition and a single prop.
- [The repair-room key — Chinese complete segments](docs/examples/camera-segments.md): two independent multi-shot prompts, camera choices and trim ranges; 16 seconds of footage planning for a 12-second film.
- [Postal worker and returned letter — Chinese character paths](docs/examples/life-paths.md): several fictional readings with facts, proposals and author choices kept separate.

The [original text-trial record](docs/text-trials-2026-10-27.md) names source revisions, raw outputs and review scope. These are disclosed examples, not cross-model statistics or film-quality validation.

## What the skill protects

- **Author decisions:** approved dialogue, speaker, relationships, story outcome, identity, duration and cuts remain in force. Proposed character histories do not become canon automatically.
- **Cause and perception:** characters react after cues they can see or hear. A camera's view does not grant a character the same knowledge.
- **Physical continuity:** count, ownership, position, support, contact and result stay consistent across cuts and segments.
- **Camera purpose:** relationship views, performance close-ups and hand/prop operations need different focus and depth. Preserve the chosen camera basis; a brand is not a genre.
- **Reference scope:** inherit only specified identity, wardrobe, setting, material, camera or sound properties. A multi-view sheet does not multiply cast or inventory.
- **Evidence boundaries:** planned, generated, inspected, approved, provider-bound and dynamically tested are separate claims. A validator cannot certify natural acting.

Music, subtitles, narration, aspect ratio and output format follow your project. The no-music/no-caption choice in the quick example is not a universal style rule. The skill also has scoped routes for music-IP/MV planning, covers, character assets and video repair; see [extended routing](references/workflow-routing.md). Most specialist reference files remain in Chinese; the English usage guide covers the common workflows without requiring you to assemble their instructions yourself.

## Requirements and maintenance

The intended host is Codex with local-skill access. Other assistants can read the methods as text, but automatic discovery, invocation and tools on other hosts are not established compatibility claims. Python is optional for prose work; the bundled development helpers target Python 3.11+, with PyYAML for YAML audits. The repository's software CI matrix covers Windows/Ubuntu and Python 3.11/3.13; check the exact run and [EVALS](EVALS.md) before attributing a pass to a revision. This does not establish macOS host discovery or media quality.

- [Install, update, rollback and uninstall](docs/installation.en.md)
- [Use the skill and troubleshoot creative handoffs](docs/usage.en.md)
- [Optional tools and development](docs/development.en.md)
- [Contribute a reproducible failure](CONTRIBUTING.md) · [Security](SECURITY.md) · [Attribution](THIRD_PARTY_NOTICES.md)

The public invocation and directory are `role2reel-public`, separate from any internal `role2reel` edition. Keep projects outside the installed skill directory. Initializer `--force` resets managed templates, including existing drafts; it is not a way to add one character safely.

Private projects, conversations, media and credentials stay outside this repository. Package version: [VERSION](VERSION). [MIT licensed](LICENSE); no affiliation with or endorsement by OpenAI, ByteDance or the referenced projects.
