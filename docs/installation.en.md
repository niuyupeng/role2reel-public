# Install, update and remove Role2Reel Public

[English home](../README.en.md) · [中文安装说明](installation.md) · [Usage](usage.en.md) · [Optional tools](development.en.md)

The skill is the **whole repository-root package**, installed under the name `role2reel-public`. Keep it separate from any internal `role2reel` edition. Ordinary text work does not require Python, API credentials or project initialization.

## Choose an installation route

| Route | Best fit | What to know |
|---|---|---|
| Codex's built-in skill installer | Install from the repository in a Codex conversation | Specify repository path `.` and name `role2reel-public`; an existing destination is not an update request |
| Named release ZIP, copied manually | A specific published snapshot without Git or Python | Verify the matching checksum, extract to staging, then install the single skill directory |
| Optional release helper | Checked ZIP installation, conservative updates and rollback | Requires Python 3.11+; accepts fresh paths or its own unchanged managed installations |
| Git checkout | Contributors or users maintaining local changes | Track the chosen branch/tag yourself; preserve local edits before updating |

### Codex installer

```text
$skill-installer Install the skill at the root of https://github.com/niuyupeng/role2reel-public with the name role2reel-public.
```

The root is path `.`. Copying only `SKILL.md` loses its references, templates and helpers. To pin a release, ask for the exact published tag shown on that release instead of the default branch. Use `$role2reel-public` on the next turn. If it is absent, check the directory below and start a new conversation. This is the intended Codex installation path; filesystem installation success is distinct from testing discovery in a particular app version.

## Find the correct directory

The bundled Codex installer uses `$CODEX_HOME/skills`; when `CODEX_HOME` is unset, it uses `~/.codex/skills`. Use the same `CODEX_HOME` that the running host uses, not a different value set only in a temporary shell. Do not change an established installation location just to follow an example.

| Host shell | Default if `CODEX_HOME` is unset | Public skill directory |
|---|---|---|
| Windows PowerShell | `$env:USERPROFILE\.codex` | `<Codex home>\skills\role2reel-public` |
| macOS/Linux shell | `$HOME/.codex` | `<Codex home>/skills/role2reel-public` |

**Windows PowerShell — fresh Git installation:**

```powershell
$skillHome = if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    Join-Path $env:USERPROFILE '.codex'
} else { $env:CODEX_HOME }
$skillDir = Join-Path (Join-Path $skillHome 'skills') 'role2reel-public'
if (Test-Path -LiteralPath $skillDir) { throw 'Destination exists; use the update instructions.' }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillDir) | Out-Null
git clone https://github.com/niuyupeng/role2reel-public.git "$skillDir"
```

**macOS/Linux — fresh Git installation:**

```bash
skill_home="${CODEX_HOME:-$HOME/.codex}"
skill_dir="$skill_home/skills/role2reel-public"
mkdir -p "$skill_home/skills"
git clone https://github.com/niuyupeng/role2reel-public.git "$skill_dir"
```

Use an absent destination for a fresh clone. The commands honor paths containing spaces. The shell examples describe filesystem operations; they do not claim that this project tested every macOS/Linux Codex UI or shell configuration.

The installed layout must be:

```text
<Codex home>/skills/
  role2reel-public/
    SKILL.md
    VERSION
    agents/
    references/
    assets/
    scripts/
    docs/
```

If you find `role2reel-public/role2reel-public/SKILL.md`, move the inner skill directory into the correct position. GitHub's automatic “Source code” archives have a repository/tag wrapper; those are different from the named release package and its checksums.

## Download and verify a release

Open [Releases](https://github.com/niuyupeng/role2reel-public/releases), choose a version and download its three matching assets:

- `role2reel-public-v<VERSION>.zip`
- `role2reel-public-v<VERSION>.manifest.json`
- `SHA256SUMS.txt`

Here `<VERSION>` means the literal version from that release's [VERSION](../VERSION) file, without adding another `v`. Older releases may use other filenames; follow the files attached to that exact release rather than mixing versions. Download all three into one otherwise empty staging directory, outside your skills and project directories.

On Linux, from that staging directory:

```bash
sha256sum -c SHA256SUMS.txt
```

On macOS:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

In Windows PowerShell, list the actual hashes and compare each file's value with its line in `SHA256SUMS.txt`:

```powershell
Get-ChildItem -File -Filter 'role2reel-public-v*' | Get-FileHash -Algorithm SHA256
Get-Content -LiteralPath .\SHA256SUMS.txt
```

A mismatch means stop and obtain the matching files again. Checksums detect changed bytes relative to the trusted release declaration; they are not a signature, a security audit or creative-quality evidence. The manifest records the package version, tag, source commit and member hashes. Check the release/tag provenance as well as the filename.

For a manual install, extract the ZIP into staging. Locate its `role2reel-public` directory and copy that **whole directory** into the chosen `skills` directory. If a public installation already exists, follow the update procedure below; do not overlay the new ZIP on it. Do not place reference media, screenplays or other project work inside the skill installation.

## Optional checked release helper

The release helper uses only the Python standard library. It is optional; normal use of the skill never requires it. Run it from the verified extracted package or a trusted checkout. Create the parent `skills` directory first, but leave the destination `role2reel-public` path absent for a fresh install. It accepts only the versioned release ZIP from `build_release.py`, including its `.release.json` metadata; a basic `package_skill.py` ZIP or GitHub source archive is not accepted. The following commands use placeholder paths and hashes: replace them with your actual values, and use `python3` instead of `python` if that is your selected Python 3.11+ command.

```text
python scripts/install_release.py install --archive "<absolute ZIP path>" --sha256 <trusted 64-hex ZIP hash> --destination "<Codex home>/skills/role2reel-public"
python scripts/install_release.py verify --destination "<Codex home>/skills/role2reel-public"
```

The `--sha256` value is the ZIP's hash from the trusted checksum record, not the manifest's hash. The final destination component must be exactly `role2reel-public`. An absent destination is accepted. An existing installation is accepted only if this helper manages it and its managed contents remain unchanged. The helper refuses an unmarked Git/manual directory, or local additions, deletions or edits; only narrowly recognized Python bytecode caches tied to packaged sources are ignored. It does not silently adopt or merge local work.

The same `install` command performs an update of an unchanged helper-managed installation. It saves the old installation outside the active `skills` directory, under `<Codex home>/role2reel-backups/`, and prints the exact backup path. Keep that path for rollback. Do not move backup directories back inside a skills discovery root, where their `SKILL.md` could be discovered as a duplicate.

## Updates that preserve your work

Before updating, inspect the installed `VERSION`, note the source/tag if available, and back up the **entire public skill directory** to a location outside all active skill roots. Keep user projects in their separate project locations. If you previously stored project files inside the skill directory, move and verify them before any replacement.

- **Helper-managed:** run `verify`, then install the newly verified ZIP. If verification reports local changes, preserve and inspect them first. There is no force-overwrite route for local changes. To replace a modified installation deliberately, archive the whole directory outside skill roots, install fresh at the now-absent public path, then selectively reapply reviewed changes.
- **Manual ZIP or Codex installer:** preserve the current directory outside skill roots, install the new version into the now-absent `role2reel-public` path, then review and reapply local customizations selectively. Avoid copying the whole old tree over the new one; that can restore removed files and old rules.
- **Git:** run `git status --short` in the public checkout and save or commit local work before updating. For an unchanged branch checkout, `git pull --ff-only` avoids an automatic merge. A detached release tag is updated by fetching tags and checking out the exact selected new tag. Do not use `reset --hard` or `clean` as a substitute for preserving changes. A branch with deliberate local commits needs an explicit merge/rebase decision, not a forced replacement.

Keep the internal `role2reel` directory untouched. Source updates do not rewrite your project or automatically regenerate its previous outputs. After replacement, check `SKILL.md` and `VERSION`, open a new conversation if needed, and run a small text-only request before resuming a large task.

### Rollback

For a helper-managed installation, use the exact backup path printed by the previous update:

```text
python scripts/install_release.py rollback --destination "<Codex home>/skills/role2reel-public" --backup "<printed backup path>"
```

The helper accepts its own generated backup names in that backup directory, checks both installations, and prints the path preserving the version it replaced. Do not bypass a local-change refusal. A manual rollback follows the same preservation principle: archive the current public directory outside skill roots, then restore the saved old directory to `role2reel-public`. A Git user can return to the recorded previous tag/commit after preserving local work. Rollback affects the skill installation, not projects or model outputs created with it.

### Uninstall and old-package migration

Locate and inspect the exact installed `role2reel-public` directory. Move it outside all skill roots to disable it reversibly, or delete **only that directory** after verifying it contains no project work you need. Remove any other public-edition duplicate only after identifying it. Do not delete the parent `skills` directory, an internal `role2reel`, project folders, model weights or application configuration. Backups are separate; retain or remove them deliberately.

The historical `public-2026-10-27` first package used a `role2reel/` root. A directory with that name may instead be an internal edition: inspect and preserve it before migration. Install the current public edition independently as `role2reel-public`; never assume every old `role2reel` directory can be removed.

## Troubleshooting and support boundaries

| Problem | What to check |
|---|---|
| `$role2reel-public` is not discovered | Running host's `CODEX_HOME`, one correctly named directory, `SKILL.md` directly inside it, then a new conversation |
| Two copies appear or rules conflict | Check every skill root you use; move obsolete copies and backups outside discovery locations |
| Missing references after installation | Reinstall the full package; don't copy only the entrypoint or flatten nested folders |
| Checksum fails | Matching ZIP/manifest/checksum from the same release; don't use the checksum for GitHub's automatic source archive |
| Helper refuses update | Read the reported local changes or unmanaged-directory reason; preserve the directory, don't delete the marker to bypass checks |
| Git pull fails | Inspect local changes, detached tag or divergent history; preserve work before choosing an update method |
| `yaml`/PyYAML is missing | Install the optional development dependencies with the selected interpreter; see [tooling](development.en.md). Prose use remains available |
| No Word/image/video output tool | Request an honest text plan or use an available tool; installation itself does not add a rendering service |

Codex local skills are the intended host. The software checks target the environments named in [EVALS](../EVALS.md) and the CI run; Windows/Ubuntu Python tests do not certify every Codex app version, macOS discovery or third-party assistants. The methods are readable as ordinary text elsewhere, but automatic invocation and tool compatibility would need separate verification. External services may need their own credentials and authorization; this package neither supplies credentials nor requires an independent API key for ordinary Codex text work.
