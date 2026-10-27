# Optional tools and development

[English home](../README.en.md) · [Usage](usage.en.md) · [Install/update](installation.en.md) · [中文工具说明](development.md)

Use the skill directly for ordinary prose, compact storyboards and prompt enrichment. The tools below are optional helpers for persistent projects, deterministic checks and release maintenance. They do not run a creative model or render a film.

Commands assume you are in the skill/repository root unless an absolute script path is given. Use your deliberately selected Python 3.11+ interpreter and environment. The examples use `python3`; on Windows this may be `python` or an explicit interpreter path. Check `python3 --version` rather than assuming a launcher chooses the intended installation.

## Keep projects outside the installation

Initialize only when a persistent project is useful. This creates editable templates; it does not approve a story, fabricate references or complete production contracts.

macOS/Linux:

```bash
python3 scripts/init_project.py "$HOME/Documents/role2reel-projects/my-film" --characters "Mira,Tomas" --scene scene-001
```

Windows PowerShell:

```powershell
python scripts/init_project.py "$env:USERPROFILE\Documents\role2reel-projects\my-film" --characters "Mira,Tomas" --scene scene-001
```

The initializer writes character, scene, storyboard, continuity and adapter templates. Repeating an ordinary initialization preserves existing files and reports them as skipped. Newly created placeholders still need real source material and the decisions required for the selected workflow.

To add a standalone character profile without changing an existing scene's participant/relationship contracts:

```bash
python3 scripts/init_project.py "/absolute/path/to/my-film" --profiles-only --characters "Jules"
```

Then edit the actual scene and relationship files if Jules should join that scene. **Do not use `--force` for this.** It overwrites managed templates for the run, including edited drafts such as `main.fountain`. Reserve it for an explicitly intended reset after preserving the project. File preservation by the initializer is not a backup strategy.

When working from another directory, call the script through the installed skill's absolute path. Do not resolve `scripts/` against the user's screenplay directory and accidentally call a different file.

## Dependencies and deterministic checks

Only the YAML-related helpers need PyYAML; the development dependency file pins the version used for the checks. Initializing a project, packaging, release installation, dialogue checks and CSV/JSON timing work use the standard library where applicable.

From a repository checkout:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
python3 scripts/audit_public_export.py --tracked
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py
```

For a release extraction with no `.git` directory, omit `--tracked`:

```bash
python3 scripts/audit_public_export.py
```

`--tracked` checks the Git-tracked export scope. Without it, the export auditor uses the explicit package allowlist. An optional `--private-rules` file can supply a local JSON array of sensitive terms; keep that file **outside** the public repository. Neither form establishes that all semantic privacy risks have been found.

A missing dependency is an environment problem, not evidence that the script, prompt or media is corrupt. Install into the selected environment with `python3 -m pip`; do not switch interpreters silently to make a test pass. See each tool's `--help` for its accepted inputs and modes.

## Pick the check that matches the artifact

| Need | Tool | What its result means |
|---|---|---|
| Dialogue review clues | `scripts/audit_dialogue.py` | Warning signals to inspect; not a taste or acting score |
| Compact/legacy timing or formal source-bound boards | `scripts/audit_storyboard.py` | Structural checking in the selected mode; modern formal checking requires the actual upstream files |
| Single-shot clipboard export | `scripts/audit_clipboard_prompts.py` | Fixed per-shot syntax and contiguous times; **not** the complete multi-shot segment format |
| Physical/timing readiness record | `scripts/audit_shot_readiness.py` | Declared blockers, source fields and feasibility rules; not proof that a source comparison is semantically correct |
| Character cognition/expression provenance | `scripts/audit_character_runtime.py` | Specified resource and state bindings; not proof of natural behavior |
| Fictional paths and formal compilation | `scripts/audit_life_paths.py` | Fact, branch, biography and compiled-source consistency; not proof that a human made a recorded choice |
| Asset/continuity or provider-task contracts | `scripts/audit_continuity.py`, `scripts/audit_video_task.py` | Required fields, modes and bindings; not evidence that a provider executed them successfully |
| Source-faithful transformation | `scripts/audit_humanization.py` | Real-file identity/revision/hash bindings; not a semantic fidelity judgment |
| Formal staged evaluation record | `scripts/audit_staged_eval.py` | Expected artifacts, bindings and recorded review fields; not proof that the recorded trials or human review occurred |

Do not force a compact draft through a formal production audit by inventing hashes, approvals or source files. Use the appropriate mode and report a draft as a draft. Formal locks need the real upstream material. The [production contracts](../references/production-contracts.md#use-the-included-resources) describe the boundaries; most detailed reference documents are in Chinese.

## Package and release

The basic packaging helper writes `dist/role2reel-public.zip` by default:

```bash
python3 scripts/package_skill.py
python3 scripts/package_skill.py --output "/absolute/path/to/role2reel-public.zip"
```

The archive root is always `role2reel-public/`, and its files come from the explicit allowlist in `scripts/package_skill.py`. This basic ZIP is useful for local inspection; it is not, by itself, a published GitHub release or a provenance manifest.

For a release, synchronize `VERSION`, the intended tag and the exact source commit. New files must be added to the allowlist and their links checked before committing. The release builder requires the matching version tag at `HEAD` and clean tracked allowlisted source bytes. Use a fresh output directory for each version; it refuses to overwrite different existing release bytes. Replace `<VERSION>` in this command with the actual version string:

```text
python scripts/build_release.py --tag v<VERSION> --output-dir dist/v<VERSION>
```

It produces the versioned ZIP, JSON manifest and `SHA256SUMS.txt` documented in [installation](installation.en.md#download-and-verify-a-release). The manifest records tag, commit, version, member sizes/hashes and the ZIP size/hash. The builder uses fixed ZIP metadata and verifies the assembled package. Determinism means the same declared inputs yield the same archive bytes; it does not make the contents safe or artistically useful.

The [release workflow](../.github/workflows/release.yml) runs for matching version tags. A tag push is a publication action: check the commit, version, tests, export inventory, license notices and release contents first. A locally generated ZIP, tag or workflow file is not proof that GitHub published the assets. Confirm the actual workflow result and attached release files before sharing a download link as the new release. See the [maintainer release guide](releasing.md) for exact gates, publication and retry behavior.

The optional `scripts/install_release.py` installs a verified ZIP and conservatively updates its own unchanged managed installations. It is not a development-tree synchronizer; Git/manual installations and modified trees require preservation and a deliberate migration. See [checked install, rollback and refusal behavior](installation.en.md#optional-checked-release-helper).

## Meaningful changes and evidence

Test the behavior affected by a change. For example, an initializer change should preserve edited files under ordinary reruns; a timing change should catch a real gap or a footage/editorial mix-up; a release change should inspect the extracted package, not only the source tree. Do not add tests that merely require preferred prose phrases.

The CI matrix declares Windows/Ubuntu and Python 3.11/3.13 software runs. Read the exact run for its result. This is separate from host skill discovery, independent model text trials, static image inspection, audio review, dynamic video and author adoption. Keep those evidence levels separate in reports. Current and historical limits are in [EVALS](../EVALS.md); an older passing snapshot does not prove a later revision passed.

For a model-behavior issue, retain the exact request, source revision, allowed inputs, actual output and specific expected difference. Mark synthetic examples as synthetic and distinguish raw output from editorially repaired demonstrations. Never turn a developer's review into a human author approval or claim a film was generated because its prompt passed a validator.

Contributions should use independent fictional fixtures. Keep private projects, local installation paths, media, credentials, raw conversations and confidential-term lists outside the public tree and release package. Review reusable improvements individually; do not synchronize an internal skill directory or copy its history wholesale. Preserve [MIT licensing](../LICENSE), [third-party notices](../THIRD_PARTY_NOTICES.md) and the [public contribution boundary](../CONTRIBUTING.md).
