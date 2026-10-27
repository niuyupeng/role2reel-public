# Releasing Role2Reel Public

The tag workflow produces a versioned public archive, a commit-bound manifest and checksums. It does not publish project files, generate media or evaluate creative quality. A local source ZIP from `package_skill.py` is still useful for development; the verified installer requires the release bundle built by `build_release.py`.

## Maintainer release

1. Review the public export and update `VERSION`. Add intentional public files to `scripts/package_skill.py:RELEASE_FILES`; never add private project exports. Commit the reviewed changes to the default branch, including workflow changes, and wait for validation.
2. Create a tag exactly equal to `v` followed by `VERSION`, at that reviewed commit. Push the commit and tag using your normal maintainer credentials. Do not move an existing release tag. GitHub events created with a workflow's own `GITHUB_TOKEN` generally do not trigger another workflow; see [GitHub's trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
3. The tag workflow runs the public boundary audit, repository validation, unit tests and a verified release build on Linux and Windows with Python 3.11 and 3.13. Only after all four jobs pass does a separate job receive `contents: write` and publish the release.
4. Inspect the completed workflow and anonymous downloads. A configured matrix is not evidence that the latest commit passed. Keep creative/text trials and media acceptance separate from these software checks.

For a local rehearsal from a clean tagged checkout, choose a fresh output directory for each version:

```sh
python -m pip install -r requirements-dev.txt
python scripts/audit_public_export.py --tracked
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py --tag v1.2.3 --output-dir dist/v1.2.3
```

Replace `v1.2.3` with the actual tag. The builder requires that tag to exist, match `VERSION` and resolve to `HEAD`; every allowlisted member must be clean and tracked. It reads canonical Git blobs so checkout line-ending conversion does not alter the release. It writes entries in sorted order with fixed timestamps/permissions and no compression, avoiding platform and zlib differences. It then reopens the archive and verifies its exact member list and hashes.

The release assets are:

- `role2reel-public-v1.2.3.zip`: one `role2reel-public/` root, the explicit public allowlist and generated `.release.json` metadata.
- `role2reel-public-v1.2.3.manifest.json`: tag, version, Git commit, member sizes/hashes and final archive size/SHA-256.
- `SHA256SUMS.txt`: SHA-256 values for the ZIP and external manifest.

The internal metadata records member hashes without a circular hash of itself. The checksum of the complete ZIP protects that metadata. Neither checksums nor manifests alone authenticate a publisher; obtain them from the trusted repository release. This workflow does not claim a signature or provenance attestation.

## Retry and failure behavior

Publication uses a draft until every uploaded asset has been downloaded and compared with the local bytes. A retry resumes an incomplete draft only when its existing assets match. A published release with all matching bytes is a no-op. Different bytes, unknown assets, incomplete published releases or a moved tag stop publication. There is no deletion or `--clobber` route. Publish corrections under a new version and tag.

The workflow is serialized per tag. An interrupted upload can leave a draft or incomplete asset; inspect it manually if the next run refuses it. Re-run the failed workflow after a transient failure. If manual publication is necessary after the gates, the equivalent command is:

```sh
python scripts/publish_release.py --tag v1.2.3 --repo OWNER/REPOSITORY --directory dist/v1.2.3
```

It requires authenticated GitHub CLI access with release-write permission; no credentials belong in command arguments or files. GitHub may require additional workflow permission if a target commit changes workflow files relative to the default branch, so merge reviewed workflow changes first. See [GitHub's release API](https://docs.github.com/en/rest/releases/releases#create-a-release), [release asset API](https://docs.github.com/en/rest/releases/assets), and [`gh release upload`](https://cli.github.com/manual/gh_release_upload).

## Verified install, update and rollback

For complete platform instructions, see [installation](installation.md) / [English installation](installation.en.md). The helper uses Python 3.11+ standard library only. Download the versioned ZIP and checksums from a trusted release, verify the ZIP before extracting executable code, and run the helper from a trusted checkout or verified extraction outside the active skills directory.

```sh
python scripts/install_release.py install --archive /path/to/role2reel-public-v1.2.3.zip --sha256 TRUSTED_ZIP_SHA256 --destination /path/to/skills/role2reel-public
python scripts/install_release.py verify --destination /path/to/skills/role2reel-public
```

Create the parent `skills` directory first. The destination must be a separate directory named `role2reel-public`. A fresh directory is installed; an existing directory must already have the helper's installation record. Existing manual/Git installations are not adopted or overwritten. Preserve them outside the skills directory and install into a fresh destination, or continue using their original maintenance method. Never point the installer at an internal skill or project.

The same `install` command updates to another verified release. Changed, added or missing local files stop the update. Python bytecode caches corresponding to packaged source files are the only ignored generated files; unrelated files and every symlink/junction still cause refusal. Matching release bytes are a verified no-op. There is no force option. Preserve intentional edits outside the installation before proceeding.

Updates stage and verify the complete new installation, then move the previous one to `<skills-parent>/role2reel-backups/role2reel-public-<id>`, outside the active skills directory. The exact backup path is printed. A failed rename attempts to restore the previous installation. No old backup is automatically deleted. Rollback checks both installations for modifications, restores the selected backup and saves the current installation as a new backup:

```sh
python scripts/install_release.py rollback --destination /path/to/skills/role2reel-public --backup /path/to/role2reel-backups/role2reel-public-ID
```

Keep the installer process and editor operations separate: directory replacement is not a transaction across concurrent manual file edits. An exclusive installer lock prevents overlapping helper runs. After an abrupt process/power failure, inspect the destination, printed backups and `.role2reel-public.install.lock` before removing a stale lock; never delete a backup to clear it. Reload the agent after a successful install, update or rollback. File verification checks installation integrity, not skill discovery in every client or media quality.
