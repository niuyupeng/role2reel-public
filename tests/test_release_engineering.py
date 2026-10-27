import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts import build_release as builder
from scripts import install_release as installer
from scripts import publish_release as publisher


COMMIT = "a" * 40


def payload(version="1.2.3", body=b"Example skill\n"):
    return {"SKILL.md": b"---\nname: role2reel-public\n---\n" + body,
            "VERSION": (version + "\n").encode(), "references/example.md": b"Public reference.\n",
            "scripts/helper.py": b"VALUE = 42\n",
            "scripts/check_example.py": b"import helper\nassert helper.VALUE == 42\n"}


def bundle(directory, version="1.2.3", body=b"Example skill\n"):
    directory.mkdir(parents=True, exist_ok=True)
    raw, manifest = builder.release_bytes(version, COMMIT, payload(version, body))
    archive = directory / manifest["archive"]["name"]
    archive.write_bytes(raw)
    manifest_name = archive.name.removesuffix(".zip") + ".manifest.json"
    manifest_raw = installer.json_bytes(manifest)
    (directory / manifest_name).write_bytes(manifest_raw)
    (directory / "SHA256SUMS.txt").write_text(
        f"{installer.sha256(raw)}  {archive.name}\n{installer.sha256(manifest_raw)}  {manifest_name}\n",
        encoding="ascii", newline="\n")
    return archive, installer.sha256(raw)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skills = self.root / "skills"
        self.skills.mkdir()
        self.destination = self.skills / installer.PACKAGE
        self.archive, self.checksum = bundle(self.root / "release")

    def install(self):
        return installer.install(self.archive, self.checksum, self.destination)

    def changed_archive(self, name, data=b"untrusted", mode=None, replace=None):
        out = io.BytesIO()
        with zipfile.ZipFile(self.archive) as source, zipfile.ZipFile(out, "w") as target:
            for info in source.infolist():
                if info.filename != replace:
                    target.writestr(info, source.read(info))
            info = zipfile.ZipInfo(name)
            if mode is not None:
                info.create_system = 3
                info.external_attr = mode << 16
            target.writestr(info, data)
        path = self.root / "changed.zip"
        path.write_bytes(out.getvalue())
        return path, installer.sha256(out.getvalue())

    def test_install_verify_same_release_noop_update_rollback(self):
        self.assertIsNone(self.install())
        before = (self.destination / installer.INSTALL_META).read_bytes()
        self.assertIsNone(self.install())
        self.assertEqual(before, (self.destination / installer.INSTALL_META).read_bytes())
        archive, checksum = bundle(self.root / "new", "1.2.4", b"Changed skill\n")
        backup = installer.install(archive, checksum, self.destination)
        self.assertEqual(backup.parent, self.root / "role2reel-backups")
        self.assertEqual((self.destination / "VERSION").read_text().strip(), "1.2.4")
        restored_backup = installer.rollback(self.destination, backup)
        self.assertEqual((self.destination / "VERSION").read_text().strip(), "1.2.3")
        self.assertEqual((restored_backup / "VERSION").read_text().strip(), "1.2.4")
        installer.verify_install(self.destination)

    def test_wrong_checksum_writes_nothing(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            installer.install(self.archive, "0" * 64, self.destination)
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.skills.iterdir()), [])

    def test_cli_unicode_update_and_rollback_with_legacy_redirect_encoding(self):
        unicode_root = self.root / "中文路径"
        unicode_skills = unicode_root / "skills"
        unicode_skills.mkdir(parents=True)
        destination = unicode_skills / installer.PACKAGE
        script = Path(installer.__file__).resolve()
        env = dict(os.environ, PYTHONIOENCODING="cp1252")

        def cli(*args):
            result = subprocess.run([sys.executable, str(script), *args],
                                    env=env, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
            return result.stdout.decode("utf-8")

        cli("install", "--archive", str(self.archive), "--sha256", self.checksum,
            "--destination", str(destination))
        archive, checksum = bundle(self.root / "new-unicode", "1.2.4")
        output = cli("install", "--archive", str(archive), "--sha256", checksum,
                     "--destination", str(destination))
        backup_line = next(line for line in output.splitlines() if line.startswith("Backup: "))
        backup = Path(backup_line.removeprefix("Backup: "))
        self.assertTrue(backup.is_dir())
        self.assertIn("中文路径", str(backup))
        output = cli("rollback", "--destination", str(destination), "--backup", str(backup))
        self.assertIn("中文路径", output)
        self.assertEqual((destination / "VERSION").read_text().strip(), "1.2.3")
        installer.verify_install(destination)

    def test_unmanaged_and_private_destination_remain_untouched(self):
        self.destination.mkdir()
        private = self.destination / "work.txt"
        private.write_bytes(b"keep")
        with self.assertRaisesRegex(ValueError, "Unmanaged"):
            self.install()
        self.assertEqual(private.read_bytes(), b"keep")
        with self.assertRaisesRegex(ValueError, "separate directory"):
            installer.install(self.archive, self.checksum, self.skills / "role2reel")
        self.assertFalse((self.skills / "role2reel").exists())

    def test_modified_added_and_deleted_files_block_updates(self):
        self.install()
        original = (self.destination / "SKILL.md").read_bytes()
        (self.destination / "SKILL.md").write_bytes(b"my edit")
        with self.assertRaisesRegex(ValueError, "modified"):
            self.install()
        self.assertEqual((self.destination / "SKILL.md").read_bytes(), b"my edit")
        (self.destination / "SKILL.md").write_bytes(original)
        extra = self.destination / "my-project.txt"
        extra.write_bytes(b"preserve")
        with self.assertRaisesRegex(ValueError, "added"):
            self.install()
        extra.unlink()
        (self.destination / "VERSION").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            self.install()
        self.assertFalse((self.root / "role2reel-backups").exists())

    def test_unsafe_paths_duplicate_and_symlink_archive_entries_are_rejected(self):
        names = ["../escape", "/absolute", "role2reel-public/../../escape", "role2reel-public/a\\b",
                 "role2reel-public/C:stream", "role2reel-public/NUL.txt", "role2reel-public/file.",
                 "role2reel-public//bad", "role2reel-public/skill.md", "role2reel-public/COM¹.log", "other/SKILL.md"]
        for name in names:
            with self.subTest(name=name):
                path, checksum = self.changed_archive(name)
                with self.assertRaises(ValueError):
                    installer.install(path, checksum, self.destination)
                self.assertFalse(self.destination.exists())
        path, checksum = self.changed_archive("role2reel-public/link", b"target", stat.S_IFLNK | 0o777)
        with self.assertRaisesRegex(ValueError, "non-regular"):
            installer.install(path, checksum, self.destination)

    def test_valid_checksum_does_not_hide_modified_member_or_unlisted_file(self):
        name = "role2reel-public/SKILL.md"
        path, checksum = self.changed_archive(name, b"changed", replace=name)
        with self.assertRaisesRegex(ValueError, "integrity"):
            installer.install(path, checksum, self.destination)
        path, checksum = self.changed_archive("role2reel-public/unlisted.txt")
        with self.assertRaisesRegex(ValueError, "member list"):
            installer.install(path, checksum, self.destination)

    def test_invalid_metadata_is_rejected_before_installing(self):
        name = "role2reel-public/" + installer.RELEASE_META
        with zipfile.ZipFile(self.archive) as archive:
            original = json.loads(archive.read(name))
        bad_size = json.loads(json.dumps(original))
        bad_size["files"]["SKILL.md"]["size"] = True
        wrong_identity = {**original, "package": "internal-skill"}
        for metadata in ([], {}, bad_size, wrong_identity):
            path, checksum = self.changed_archive(name, json.dumps(metadata).encode(), replace=name)
            with self.assertRaises(ValueError):
                installer.install(path, checksum, self.destination)
            self.assertFalse(self.destination.exists())

    def test_expanded_archive_limit_is_checked_before_writes(self):
        with patch.object(installer, "MAX_FILE_BYTES", 8):
            with self.assertRaises(ValueError):
                self.install()
        self.assertFalse(self.destination.exists())

    def test_generated_python_bytecode_does_not_block_update(self):
        self.install()
        environment = dict(os.environ)
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        subprocess.run([sys.executable, str(self.destination / "scripts/check_example.py")],
                       check=True, env=environment)
        caches = list((self.destination / "scripts/__pycache__").glob("*.pyc"))
        self.assertTrue(caches)
        installer.verify_install(self.destination)
        archive, checksum = bundle(self.root / "new", "1.2.4")
        backup = installer.install(archive, checksum, self.destination)
        self.assertTrue((backup / "scripts/__pycache__" / caches[0].name).is_file())
        unknown = self.destination / "scripts/__pycache__/private.cpython-311.pyc"
        unknown.parent.mkdir(exist_ok=True)
        unknown.write_bytes(b"not a generated cache for a packaged source")
        with self.assertRaisesRegex(ValueError, "added"):
            installer.verify_install(self.destination)

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_junction_ancestor_is_rejected(self):
        target = self.root / "junction-skills"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(target), str(self.skills)], capture_output=True)
        if result.returncode:
            self.skipTest("Filesystem does not support Windows junctions")
        with self.assertRaisesRegex(ValueError, "Linked"):
            installer.install(self.archive, self.checksum, target / installer.PACKAGE)
        self.assertFalse(self.destination.exists())
        target.rmdir()

    def test_installed_symlink_and_ancestor_link_are_rejected(self):
        self.install()
        target = self.root / "outside.txt"
        target.write_text("outside")
        link = self.destination / "link"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"OS does not allow symlink creation: {exc}")
        with self.assertRaisesRegex(ValueError, "Linked"):
            self.install()
        link.unlink()
        ancestor = self.root / "linked-skills"
        ancestor.symlink_to(self.skills, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Linked"):
            installer.install(self.archive, self.checksum, ancestor / installer.PACKAGE)
        self.assertEqual(target.read_text(), "outside")

    def test_failed_swap_restores_previous_installation(self):
        self.install()
        archive, checksum = bundle(self.root / "new", "1.2.4")
        original = Path.rename

        def failing_rename(path, target):
            if path.name.startswith(".role2reel-stage-"):
                raise OSError("Simulated rename failure")
            return original(path, target)

        with patch.object(Path, "rename", failing_rename), self.assertRaises(OSError):
            installer.install(archive, checksum, self.destination)
        installer.verify_install(self.destination)
        self.assertEqual((self.destination / "VERSION").read_text().strip(), "1.2.3")
        self.assertFalse(any(p.name.startswith(".role2reel-stage-") for p in self.skills.iterdir()))

    def test_changed_backup_blocks_rollback_and_keeps_current(self):
        self.install()
        archive, checksum = bundle(self.root / "new", "1.2.4")
        backup = installer.install(archive, checksum, self.destination)
        (backup / "SKILL.md").write_bytes(b"edited backup")
        with self.assertRaises(ValueError):
            installer.rollback(self.destination, backup)
        self.assertEqual((self.destination / "VERSION").read_text().strip(), "1.2.4")

    def test_failed_rollback_restores_current_and_keeps_selected_backup(self):
        self.install()
        archive, checksum = bundle(self.root / "new", "1.2.4")
        backup = installer.install(archive, checksum, self.destination)
        original = Path.rename

        def failing_rename(path, target):
            if path == backup:
                raise OSError("Simulated rollback rename failure")
            return original(path, target)

        with patch.object(Path, "rename", failing_rename), self.assertRaises(OSError):
            installer.rollback(self.destination, backup)
        installer.verify_install(self.destination)
        installer.verify_install(backup)
        self.assertEqual((self.destination / "VERSION").read_text().strip(), "1.2.4")
        self.assertEqual((backup / "VERSION").read_text().strip(), "1.2.3")

    def test_deterministic_bytes_ignore_input_order(self):
        files = payload()
        first = builder.release_bytes("1.2.3", COMMIT, files)
        second = builder.release_bytes("1.2.3", COMMIT, dict(reversed(list(files.items()))))
        self.assertEqual(first, second)
        builder.verify_bundle(self.archive.parent, "v1.2.3")

    def test_real_git_tag_clean_state_and_build_idempotency(self):
        repo = self.root / "repo"
        repo.mkdir()
        def git(*args):
            return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)
        git("init")
        git("config", "user.name", "Release Test")
        git("config", "user.email", "release@example.invalid")
        git("config", "core.autocrlf", "false")
        for name, data in payload().items():
            target = repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        git("add", ".")
        git("commit", "-m", "Synthetic fixture")
        git("tag", "v1.2.3")
        output = self.root / "built"
        with patch.object(builder.package_skill, "RELEASE_FILES", tuple(payload())):
            first = builder.build(repo, "v1.2.3", output)
            self.assertEqual(first, builder.build(repo, "v1.2.3", output))
            with self.assertRaisesRegex(ValueError, "tag must equal"):
                builder.build(repo, "v9.9.9", output)
            (repo / "SKILL.md").write_bytes(b"uncommitted")
            with self.assertRaisesRegex(ValueError, "clean"):
                builder.build(repo, "v1.2.3", output)
            git("checkout", "--", "SKILL.md")
            (output / "SHA256SUMS.txt").write_bytes(b"existing different bytes")
            with self.assertRaisesRegex(ValueError, "Refusing to replace"):
                builder.build(repo, "v1.2.3", output)
            self.assertEqual((output / "SHA256SUMS.txt").read_bytes(), b"existing different bytes")
            (repo / "extra.txt").write_bytes(b"Another commit")
            git("add", "extra.txt")
            git("commit", "-m", "Different head")
            with self.assertRaisesRegex(ValueError, "tag does not point"):
                builder.build(repo, "v1.2.3", self.root / "wrong-head")


class FakeRemote:
    def __init__(self):
        self.current = None
        self.files = {}
        self.mutations = []
        self.commit = COMMIT

    def tag_commit(self, tag):
        return self.commit

    def release(self, tag):
        if self.current is None:
            return None
        return {"draft": self.current, "assets": [{"name": name, "id": name, "state": "uploaded"} for name in self.files]}

    def download(self, asset):
        return self.files[asset["id"]]

    def create(self, tag, commit):
        self.current = True
        self.mutations.append("create")

    def upload(self, tag, path):
        if path.name in self.files:
            raise ValueError("Duplicate upload")
        self.files[path.name] = path.read_bytes()
        self.mutations.append("upload:" + path.name)

    def publish(self, tag):
        self.current = False
        self.mutations.append("publish")


class PublishTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        bundle(self.directory)
        self.remote = FakeRemote()

    def publish(self):
        return publisher.publish(self.directory, "v1.2.3", self.remote)

    def test_publish_then_identical_rerun_has_no_mutations(self):
        self.publish()
        self.assertEqual(len(self.remote.files), 3)
        before = list(self.remote.mutations)
        self.assertIn("Already published", self.publish())
        self.assertEqual(before, self.remote.mutations)

    def test_existing_different_bytes_are_never_replaced(self):
        self.publish()
        name = next(iter(self.remote.files))
        self.remote.files[name] = b"previous released bytes"
        before = list(self.remote.mutations)
        with self.assertRaisesRegex(ValueError, "Existing release bytes differ"):
            self.publish()
        self.assertEqual(self.remote.files[name], b"previous released bytes")
        self.assertEqual(before, self.remote.mutations)

    def test_incomplete_draft_resumes_but_published_release_does_not(self):
        self.remote.current = True
        self.remote.files["SHA256SUMS.txt"] = (self.directory / "SHA256SUMS.txt").read_bytes()
        self.publish()
        self.assertEqual(len(self.remote.files), 3)
        self.assertFalse(self.remote.current)
        del self.remote.files["SHA256SUMS.txt"]
        before = list(self.remote.mutations)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            self.publish()
        self.assertEqual(before, self.remote.mutations)

    def test_wrong_remote_commit_does_not_create_release(self):
        self.remote.commit = "b" * 40
        with self.assertRaisesRegex(ValueError, "Remote tag differs"):
            self.publish()
        self.assertEqual(self.remote.mutations, [])

    def test_bad_download_after_upload_leaves_draft(self):
        with patch.object(self.remote, "download", return_value=b"corrupt transfer"):
            with self.assertRaisesRegex(ValueError, "bytes differ"):
                self.publish()
        self.assertTrue(self.remote.current)
        self.assertNotIn("publish", self.remote.mutations)


if __name__ == "__main__":
    unittest.main()
