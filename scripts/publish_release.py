#!/usr/bin/env python3
"""Publish verified release assets through gh; never replace existing bytes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

try:
    from .build_release import verify_bundle
except ImportError:
    from build_release import verify_bundle


class GitHub:
    def __init__(self, repository: str):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Use an explicit owner/repository")
        self.repository = repository
        self.api = "repos/" + repository

    def run(self, *args: str) -> bytes:
        result = subprocess.run(["gh", *args], capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError("GitHub command failed: " + result.stderr.decode("utf-8", errors="replace").strip())
        return result.stdout

    def tag_commit(self, tag: str) -> str:
        item = json.loads(self.run("api", self.api + "/git/ref/tags/" + tag))["object"]
        for _ in range(10):
            if item["type"] == "commit":
                return item["sha"]
            if item["type"] != "tag":
                break
            item = json.loads(self.run("api", self.api + "/git/tags/" + item["sha"]))["object"]
        raise ValueError("Remote tag does not resolve to a commit")

    def release(self, tag: str) -> dict | None:
        # Listing with the publishing token includes drafts, so interrupted runs
        # can resume even when the tag-specific endpoint only exposes a release.
        pages = json.loads(self.run("api", self.api + "/releases?per_page=100", "--paginate", "--slurp"))
        matches = [item for page in pages for item in page if item["tag_name"] == tag]
        if not matches:
            return None
        if len(matches) != 1:
            raise ValueError("Multiple releases share this tag; inspect them manually")
        release = matches[0]
        # Pagination prevents silently ignoring assets beyond the first API page.
        pages = self.run("api", self.api + "/releases/" + str(release["id"]) + "/assets?per_page=100",
                         "--paginate", "--slurp")
        release["assets"] = [asset for page in json.loads(pages) for asset in page]
        return release

    def download(self, asset: dict) -> bytes:
        return self.run("api", self.api + "/releases/assets/" + str(asset["id"]),
                        "-H", "Accept: application/octet-stream")

    def create(self, tag: str, commit: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            notes = Path(directory) / "notes.md"
            notes.write_text(f"Source commit: `{commit}`.\n\nDownload the versioned ZIP and verify it with `SHA256SUMS.txt`. "
                             "The manifest records the commit, version and per-file hashes. "
                             "Install and update instructions are in `docs/installation.md`.\n", encoding="utf-8")
            self.run("release", "create", tag, "--repo", self.repository, "--verify-tag", "--draft",
                     "--title", "Role2Reel Public " + tag, "--notes-file", str(notes))

    def upload(self, tag: str, path: Path) -> None:
        # Intentionally no --clobber: GitHub rejects a concurrent name collision.
        self.run("release", "upload", tag, str(path.resolve()), "--repo", self.repository)

    def publish(self, tag: str) -> None:
        self.run("release", "edit", tag, "--repo", self.repository, "--draft=false")


def check_existing(release: dict, artifacts: dict[str, bytes], remote) -> set[str]:
    names = set()
    for asset in release["assets"]:
        name = asset["name"]
        if name in names or name not in artifacts or asset.get("state") != "uploaded":
            raise ValueError("Unexpected, duplicate or incomplete release asset; inspect the draft manually")
        names.add(name)
        if remote.download(asset) != artifacts[name]:
            raise ValueError(f"Existing release bytes differ: {name}; use a new version, never overwrite")
    return names


def publish(directory: Path, tag: str, remote) -> str:
    artifacts = verify_bundle(directory, tag)
    manifest = json.loads(artifacts[next(name for name in artifacts if name.endswith(".manifest.json"))])
    commit = manifest["commit"]
    if remote.tag_commit(tag) != commit:
        raise ValueError("Remote tag differs from the manifest commit")
    release = remote.release(tag)
    existing = set() if release is None else check_existing(release, artifacts, remote)
    if release is not None and not release["draft"]:
        if existing != set(artifacts):
            raise ValueError("Published release is incomplete; refuse to mutate published assets")
        return "Already published; all remote asset bytes match."
    if release is None:
        remote.create(tag, commit)
    for name in sorted(set(artifacts) - existing):
        remote.upload(tag, directory / name)
    release = remote.release(tag)
    if release is None or check_existing(release, artifacts, remote) != set(artifacts):
        raise ValueError("Uploaded assets did not verify; leave the release as a draft")
    if remote.tag_commit(tag) != commit:
        raise ValueError("Remote tag moved during publishing; leave the release as a draft")
    if release["draft"]:
        remote.publish(tag)
    return "Release published after uploaded bytes were verified."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    args = parser.parse_args()
    try:
        print(publish(args.directory, args.tag, GitHub(args.repo)))
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(1, f"Release publication stopped: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
