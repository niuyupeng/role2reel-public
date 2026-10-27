#!/usr/bin/env python3
"""Build a verified, byte-reproducible allowlisted release from a clean Git tag."""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

try:
    from . import package_skill
    from .install_release import PACKAGE, RELEASE_META, json_bytes, read_archive, safe_relative, sha256
except ImportError:
    import package_skill
    from install_release import PACKAGE, RELEASE_META, json_bytes, read_archive, safe_relative, sha256

ROOT = Path(__file__).resolve().parents[1]


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def committed_payload(root: Path, tag: str) -> tuple[str, str, dict[str, bytes]]:
    # Match release_paths() normalization, including Windows 8.3 aliases.
    root = root.resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+){2,3}", version) or tag != "v" + version:
        raise ValueError("Release tag must equal v + VERSION")
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    tagged = git(root, "rev-parse", "--verify", "refs/tags/" + tag + "^{commit}").decode().strip()
    if tagged != commit:
        raise ValueError("Release tag does not point to the checked-out commit")
    files = package_skill.release_paths(root)
    names = [path.relative_to(root).as_posix() for path in files]
    if len(set(name.casefold() for name in names)) != len(names):
        raise ValueError("Duplicate release allowlist member")
    # Ignore unrelated untracked files: the allowlist is the publication boundary.
    if git(root, "status", "--porcelain", "--untracked-files=all", "--", *names):
        raise ValueError("Release files must be clean and committed before building")
    payload = {}
    for name in sorted(names):
        safe_relative(name)
        mode = git(root, "ls-tree", commit, "--", name).split(b" ", 1)[0]
        if mode != b"100644":
            raise ValueError(f"Release member is not an ordinary tracked file: {name}")
        # Git blobs provide canonical bytes even in CRLF working trees.
        payload[name] = git(root, "show", commit + ":" + name)
    if payload["VERSION"].decode("utf-8").strip() != version:
        raise ValueError("Working VERSION differs from the tagged version")
    return version, commit, payload


def release_bytes(version: str, commit: str, payload: dict[str, bytes]) -> tuple[bytes, dict]:
    meta = {"schema": 1, "package": PACKAGE, "version": version, "tag": "v" + version,
            "commit": commit, "files": {
                name: {"sha256": sha256(data), "size": len(data)}
                for name, data in sorted(payload.items())
            }}
    members = dict(payload)
    if RELEASE_META in members:
        raise ValueError("Reserved release metadata in payload")
    members[RELEASE_META] = json_bytes(meta)
    buffer = io.BytesIO()
    # Stored entries avoid zlib-version-dependent compression differences.
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(members.items()):
            safe_relative(name)
            info = zipfile.ZipInfo(PACKAGE + "/" + name, (2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)
    raw = buffer.getvalue()
    manifest = dict(meta)
    manifest["archive"] = {"name": PACKAGE + "-v" + version + ".zip",
                           "sha256": sha256(raw), "size": len(raw)}
    return raw, manifest


def write_once(path: Path, data: bytes) -> None:
    if path.exists():
        if path.is_symlink() or path.read_bytes() != data:
            raise ValueError(f"Refusing to replace different release bytes: {path.name}")
        return
    with path.open("xb") as stream:
        stream.write(data)


def verify_bundle(directory: Path, tag: str) -> dict[str, bytes]:
    if not re.fullmatch(r"v[0-9]+(?:\.[0-9]+){2,3}", tag):
        raise ValueError("Invalid release tag")
    stem = PACKAGE + "-" + tag
    manifest_name = stem + ".manifest.json"
    manifest_raw = (directory / manifest_name).read_bytes()
    manifest = json.loads(manifest_raw)
    if not isinstance(manifest, dict):
        raise ValueError("Invalid external release manifest")
    archive_name = stem + ".zip"
    archive_raw = (directory / archive_name).read_bytes()
    if manifest.get("archive") != {"name": archive_name, "sha256": sha256(archive_raw), "size": len(archive_raw)}:
        raise ValueError("Release archive differs from external manifest")
    meta, _ = read_archive(directory / archive_name, sha256(archive_raw))
    if meta != {key: value for key, value in manifest.items() if key != "archive"} or meta["tag"] != tag:
        raise ValueError("Internal/external release manifest mismatch")
    checksums = (f"{sha256(archive_raw)}  {archive_name}\n"
                 f"{sha256(manifest_raw)}  {manifest_name}\n").encode("ascii")
    if (directory / "SHA256SUMS.txt").read_bytes() != checksums:
        raise ValueError("Release checksums differ from assembled files")
    return {archive_name: archive_raw, manifest_name: manifest_raw, "SHA256SUMS.txt": checksums}


def build(root: Path, tag: str, output: Path) -> dict[str, bytes]:
    version, commit, payload = committed_payload(root, tag)
    raw, manifest = release_bytes(version, commit, payload)
    archive_name = manifest["archive"]["name"]
    manifest_name = archive_name.removesuffix(".zip") + ".manifest.json"
    manifest_raw = json_bytes(manifest)
    artifacts = {archive_name: raw, manifest_name: manifest_raw, "SHA256SUMS.txt": (
        f"{sha256(raw)}  {archive_name}\n{sha256(manifest_raw)}  {manifest_name}\n"
    ).encode("ascii")}
    output.mkdir(parents=True, exist_ok=True)
    # Check every existing artifact before writing any absent files.
    for name, data in artifacts.items():
        path = output / name
        if path.exists() and (path.is_symlink() or path.read_bytes() != data):
            raise ValueError(f"Refusing to replace different release bytes: {name}")
    for name, data in artifacts.items():
        write_once(output / name, data)
    return verify_bundle(output, tag)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        artifacts = build(ROOT, args.tag, args.output_dir)
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Release build failed: {exc}\n")
    for name, data in artifacts.items():
        print(f"{sha256(data)}  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
