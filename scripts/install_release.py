#!/usr/bin/env python3
"""Verify and install a checksummed public release; preserve updates as backups."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import uuid
import zipfile

PACKAGE = "role2reel-public"
RELEASE_META = ".release.json"
INSTALL_META = ".role2reel-install.json"
MAX_FILES = 2500
MAX_BYTES = 64 * 1024 * 1024
MAX_FILE_BYTES = 16 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def safe_relative(name: str) -> str:
    """Use the same portable path rules on Windows and Unix, before extraction."""
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Unsafe archive path")
    parts = name.split("/")
    if PurePosixPath(name).is_absolute() or any(
        not part or part in (".", "..") or part[-1] in ". "
        or any(ord(char) < 32 or char in '<>"|?*' for char in part)
        or re.fullmatch(r"(?i:con|prn|aux|nul|com[1-9¹²³]|lpt[1-9¹²³])(?:\..*)?", part)
        for part in parts
    ):
        raise ValueError("Unsafe archive path")
    return name


def validate_metadata(meta: dict) -> None:
    if (not isinstance(meta, dict) or meta.get("schema") != 1
            or meta.get("package") != PACKAGE
            or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){2,3}", str(meta.get("version", "")))
            or meta.get("tag") != "v" + meta["version"]
            or not re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})", str(meta.get("commit", "")))
            or not isinstance(meta.get("files"), dict)):
        raise ValueError("Invalid public release metadata")
    files = meta["files"]
    if not {"SKILL.md", "VERSION"}.issubset(files) or not 2 <= len(files) <= MAX_FILES:
        raise ValueError("Release does not contain the public skill")
    seen = set()
    for name, item in files.items():
        safe_relative(name)
        if name.casefold() in (RELEASE_META, INSTALL_META) or name.casefold() in seen:
            raise ValueError("Duplicate or reserved release member")
        seen.add(name.casefold())
        if (not isinstance(item, dict) or not re.fullmatch(r"[a-f0-9]{64}", str(item.get("sha256", "")))
                or type(item.get("size")) is not int or not 0 <= item["size"] <= MAX_FILE_BYTES):
            raise ValueError("Invalid release member metadata")


def read_archive(path: Path, expected_sha256: str) -> tuple[dict, dict[str, bytes]]:
    if not re.fullmatch(r"[a-fA-F0-9]{64}", expected_sha256):
        raise ValueError("A trusted 64-character SHA-256 checksum is required")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Archive exceeds size limit")
    raw = path.read_bytes()
    if sha256(raw) != expected_sha256.lower():
        raise ValueError("Archive SHA-256 mismatch; no files changed")
    files: dict[str, bytes] = {}
    seen = set()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES + 1 or sum(info.file_size for info in infos) > MAX_BYTES:
            raise ValueError("Archive exceeds extraction limits")
        for info in infos:
            safe_relative(info.filename)
            if not info.filename.startswith(PACKAGE + "/"):
                raise ValueError("Archive must contain only role2reel-public")
            name = info.filename[len(PACKAGE) + 1:]
            safe_relative(name)
            mode = info.external_attr >> 16
            if (info.is_dir() or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                    or info.flag_bits & 1 or info.file_size > MAX_FILE_BYTES
                    or name.casefold() in seen):
                raise ValueError("Duplicate, encrypted, non-regular, or oversized archive member")
            seen.add(name.casefold())
            files[name] = archive.read(info)
    try:
        meta = json.loads(files[RELEASE_META])
    except (KeyError, ValueError) as exc:
        raise ValueError("Missing or invalid release metadata") from exc
    validate_metadata(meta)
    if set(files) != set(meta["files"]) | {RELEASE_META}:
        raise ValueError("Archive member list differs from manifest")
    for name, item in meta["files"].items():
        if item != {"sha256": sha256(files[name]), "size": len(files[name])}:
            raise ValueError(f"Release member integrity failure: {name}")
    if files["VERSION"].decode("utf-8").strip() != meta["version"]:
        raise ValueError("VERSION differs from release metadata")
    header = files["SKILL.md"].decode("utf-8").split("---", 2)
    if len(header) != 3 or "name: role2reel-public" not in header[1].splitlines():
        raise ValueError("Archive skill identity is not role2reel-public")
    return meta, files


def reject_links(path: Path) -> None:
    """Reject symlinks and Windows reparse points, including ancestor junctions."""
    for current in (path, *path.parents):
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Linked paths are not supported: {current.name}")


def destination_path(path: Path) -> Path:
    path = Path(os.path.abspath(path.expanduser()))
    if path.name != PACKAGE:
        raise ValueError("Destination must be a separate directory named role2reel-public")
    reject_links(path)
    if not path.parent.is_dir():
        raise ValueError("Create the destination parent directory first")
    return path


def verify_install(path: Path) -> dict:
    reject_links(path)
    reject_links(path / INSTALL_META)
    reject_links(path / RELEASE_META)
    try:
        state = json.loads((path / INSTALL_META).read_bytes())
        meta_raw = (path / RELEASE_META).read_bytes()
        meta = json.loads(meta_raw)
    except (OSError, ValueError) as exc:
        raise ValueError("Unmanaged directory; preserve it and choose a fresh public installation") from exc
    validate_metadata(meta)
    expected = dict(meta["files"])
    expected[RELEASE_META] = {"sha256": sha256(meta_raw), "size": len(meta_raw)}
    if (not isinstance(state, dict) or state.get("schema") != 1 or state.get("files") != expected
            or not re.fullmatch(r"[a-f0-9]{64}", str(state.get("archive_sha256", "")))):
        raise ValueError("Installation record is invalid or modified")
    actual = set()
    for member in path.rglob("*"):
        reject_links(member)
        if member.is_file():
            name = member.relative_to(path).as_posix()
            if name == INSTALL_META:
                continue
            cache = re.fullmatch(r"(.+)\.(?:cpython|pypy)-[0-9]+(?:\.opt-[0-9]+)?\.pyc", member.name)
            if member.parent.name == "__pycache__" and cache:
                source = member.parent.parent / (cache[1] + ".py")
                if source.relative_to(path).as_posix() in expected:
                    # Ordinary Python imports create these derived files. Links
                    # were rejected above; unrelated files remain protected.
                    continue
            actual.add(name)
            data = member.read_bytes()
            if expected.get(name) != {"sha256": sha256(data), "size": len(data)}:
                raise ValueError(f"Local file added or modified: {name}; preserve it before updating")
        elif not member.is_dir():
            raise ValueError("Non-regular file in installation")
    if actual != set(expected):
        raise ValueError("Local files are missing; preserve the installation before updating")
    return state


@contextmanager
def install_lock(destination: Path):
    lock = destination.parent / ("." + PACKAGE + ".install.lock")
    try:
        with lock.open("x", encoding="utf-8") as stream:
            stream.write(str(os.getpid()))
    except FileExistsError as exc:
        raise ValueError("An installation lock exists; check for a running installer before removing it") from exc
    try:
        yield
    finally:
        lock.unlink()


def backup_location(destination: Path) -> Path:
    directory = destination.parent.parent / "role2reel-backups"
    reject_links(directory)
    directory.mkdir(exist_ok=True)
    return directory / (PACKAGE + "-" + uuid.uuid4().hex)


def swap_install(staged: Path, destination: Path) -> Path | None:
    backup = None
    if destination.exists():
        verify_install(destination)
        backup = backup_location(destination)
        destination.rename(backup)
    try:
        staged.rename(destination)
    except BaseException:
        if backup is not None:
            backup.rename(destination)
        raise
    return backup


def install(archive: Path, expected_sha256: str, destination: Path) -> Path | None:
    meta, files = read_archive(archive, expected_sha256)
    destination = destination_path(destination)
    with install_lock(destination):
        if destination.exists():
            current = verify_install(destination)
            if current["archive_sha256"] == expected_sha256.lower():
                return None
        staged = Path(tempfile.mkdtemp(prefix=".role2reel-stage-", dir=destination.parent))
        try:
            for name, data in files.items():
                target = staged / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            state = {"schema": 1, "archive_sha256": expected_sha256.lower(), "files": {
                name: {"sha256": sha256(data), "size": len(data)} for name, data in files.items()
            }}
            (staged / INSTALL_META).write_bytes(json_bytes(state))
            verify_install(staged)
            return swap_install(staged, destination)
        finally:
            if staged.exists():
                # Only remove the fresh temporary directory, never an installation/backup.
                if staged.parent != destination.parent or not staged.name.startswith(".role2reel-stage-"):
                    raise ValueError("Unexpected staging path")
                shutil.rmtree(staged)


def rollback(destination: Path, backup: Path) -> Path:
    destination = destination_path(destination)
    backup = Path(os.path.abspath(backup.expanduser()))
    if (backup.parent != destination.parent.parent / "role2reel-backups"
            or not re.fullmatch(PACKAGE + r"-[a-f0-9]{32}", backup.name)):
        raise ValueError("Choose an installer-created backup for this installation")
    with install_lock(destination):
        verify_install(backup)
        verify_install(destination)
        result = swap_install(backup, destination)
        assert result is not None
        return result


def main() -> int:
    # Redirected Windows streams can otherwise fail after a successful swap
    # when the printed backup path contains characters outside the ANSI page.
    # Keep this CLI contract out of the importable installation functions.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "verify", "rollback"):
        command = sub.add_parser(name)
        command.add_argument("--destination", type=Path, required=True)
        if name == "install":
            command.add_argument("--archive", type=Path, required=True)
            command.add_argument("--sha256", required=True)
        if name == "rollback":
            command.add_argument("--backup", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "install":
            backup = install(args.archive, args.sha256, args.destination)
            print("Public release installed and verified.")
            if backup:
                print(f"Backup: {backup}")
        elif args.command == "verify":
            verify_install(destination_path(args.destination))
            print("Installed files match the recorded release.")
        else:
            print(f"Restored backup. Previous installation saved at: {rollback(args.destination, args.backup)}")
    except (ValueError, OSError, zipfile.BadZipFile, UnicodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
