from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.audit_dialogue import audit_text
from scripts.audit_storyboard import audit_rows, load_rows
from scripts.init_project import initialize
from scripts.package_skill import RELEASE_FILES, package
from scripts.validate_repo import validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class InitializerTests(unittest.TestCase):
    def test_cli_rejects_unlinked_participant_without_traceback_or_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            initialize(target, ["Mara"], "scene", False)
            draft = target / "04-screenplay" / "main.fountain"
            draft.write_text("Title: Saved draft\n\nMARA\nKeep this line.\n", encoding="utf-8")
            before = {path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()}

            result = subprocess.run(
                [sys.executable, "-X", "utf8", "-B", str(ROOT / "scripts" / "init_project.py"),
                 str(target), "--characters", "Mara,Ellis", "--scene", "scene"],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr.startswith("ERROR New characters"))
            self.assertIn("not an incremental character update", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            after = {path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()}
            self.assertEqual(after, before)

    def test_cli_reports_filesystem_error_but_library_still_raises(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "existing-file"
            target.write_text("keep this file", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-X", "utf8", "-B", str(ROOT / "scripts" / "init_project.py"), str(target)],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr.startswith("ERROR "))
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "keep this file")
            with self.assertRaises(OSError):
                initialize(target, [], "scene", False)

    def test_cli_force_help_explains_full_overwrite_scope(self) -> None:
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(ROOT / "scripts" / "init_project.py"), "--help"],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(result.returncode, 0)
        help_text = " ".join(result.stdout.split())
        self.assertIn("Overwrite every existing managed template file", help_text)
        self.assertIn("including edited drafts", help_text)
        self.assertIn("not an incremental character update", help_text)

    def test_initializes_unicode_characters_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            created, skipped = initialize(target, ["角色甲", "角色乙"], "场景一", False)
            self.assertGreaterEqual(len(created), 18)
            self.assertEqual(skipped, [])
            self.assertTrue((target / "02-characters" / "角色甲" / "character.yaml").is_file())
            self.assertTrue((target / "02-characters" / "角色乙" / "memories.yaml").is_file())
            self.assertTrue((target / "02-characters" / "角色乙" / "life-path-workbench.yaml").is_file())
            self.assertTrue((target / "02-characters" / "角色乙" / "life-path-reading.md").is_file())
            self.assertTrue((target / "02-characters" / "角色乙" / "speech-corpus.yaml").is_file())
            self.assertTrue((target / "03-scene" / "场景一" / "scene-contract.yaml").is_file())
            self.assertTrue((target / "01-humanized").is_dir())
            self.assertTrue((target / "01-humanized" / "meaning-ledger.yaml").is_file())
            self.assertTrue((target / "01-humanized" / "humanized-draft.md").is_file())
            self.assertTrue((target / "06-continuity" / "visual-bible.yaml").is_file())
            self.assertTrue((target / "07-adapter" / "video-task.yaml").is_file())
            first_content = (target / "02-characters" / "角色甲" / "character.yaml").read_text(encoding="utf-8")
            self.assertIn('name: "角色甲"', first_content)
            scene_content = (target / "03-scene" / "场景一" / "scene-contract.yaml").read_text(encoding="utf-8")
            beat_content = (target / "03-scene" / "场景一" / "beat-map.yaml").read_text(encoding="utf-8")
            turn_content = (target / "03-scene" / "场景一" / "turn-state.yaml").read_text(encoding="utf-8")
            speech_content = (target / "02-characters" / "角色乙" / "speech-corpus.yaml").read_text(encoding="utf-8")
            relationship_content = (target / "02-characters" / "relationship-ledger.yaml").read_text(encoding="utf-8")
            life_path_content = (target / "02-characters" / "角色乙" / "life-path-workbench.yaml").read_text(encoding="utf-8")
            self.assertIn('  - id: "角色甲"', scene_content)
            self.assertIn('  - id: "角色乙"', scene_content)
            self.assertNotIn("character_id: null", turn_content)
            self.assertIn('character_id: "角色乙"', speech_content)
            self.assertIn('from_character: "角色甲"', relationship_content)
            self.assertIn('to_character: "角色乙"', relationship_content)
            self.assertIn('character_sources:\n      - character_id: "角色甲"', relationship_content)
            self.assertIn('package_context_id: "character-package-角色乙"', relationship_content)
            self.assertIn('character_id: "角色乙"', life_path_content)
            self.assertIn('package_context_id: "character-package-角色乙"', life_path_content)
            self.assertIn("mode: unclassified", life_path_content)
            self.assertIn("shared_memory_contracts:", relationship_content)
            self.assertIn("first_impulse: null", turn_content)
            self.assertIn("decision_traces:", turn_content)
            self.assertIn("character_runtime_scopes:", scene_content)
            self.assertIn('beat_map_id: "场景一-beats"', beat_content)

            created_again, skipped_again = initialize(target, ["角色甲", "角色乙"], "场景一", False)
            self.assertEqual(created_again, [])
            self.assertEqual(len(skipped_again), len(created))

    def test_extend_disambiguates_existing_slug_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            initialize(target, ["A B"], "scene", False)
            with self.assertRaises(ValueError):
                initialize(target, ["A/B"], "scene", False)
            self.assertFalse((target / "02-characters" / "a-b-2").exists())
            created, _ = initialize(target, ["A/B"], "scene", False, profiles_only=True)
            second_profile = target / "02-characters" / "a-b-2" / "character.yaml"
            self.assertTrue(
                any(path.name == "character.yaml" and path.parent.name == "a-b-2" for path in created)
            )
            self.assertTrue(second_profile.is_file())
            self.assertIn('name: "A/B"', second_profile.read_text(encoding="utf-8"))

    def test_reserved_windows_components_are_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            initialize(target, ["COM1"], "NUL", False)
            self.assertTrue((target / "02-characters" / "id-com1" / "character.yaml").is_file())
            self.assertTrue((target / "03-scene" / "id-nul" / "scene-contract.yaml").is_file())

    def test_v01_workspace_remains_usable_without_retroactive_life_path_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "legacy-project"
            legacy_dir = target / "02-characters" / "legacy"
            legacy_dir.mkdir(parents=True)
            (target / "project.yaml").write_text("schema_version: 1\n", encoding="utf-8")
            legacy_profile = legacy_dir / "character.yaml"
            legacy_content = 'schema_version: 1\ncharacter:\n  id: "legacy"\n  name: "旧角色"\n'
            legacy_profile.write_text(legacy_content, encoding="utf-8")

            created, skipped = initialize(target, ["新增角色"], "unused", False, profiles_only=True)

            self.assertEqual(skipped, [])
            self.assertTrue(any(path.name == "life-path-workbench.yaml" for path in created))
            self.assertEqual(legacy_profile.read_text(encoding="utf-8"), legacy_content)
            self.assertFalse((legacy_dir / "life-path-workbench.yaml").exists())
            self.assertEqual(audit_text("旧角色\n原样保留。\n"), [])

    def test_rejects_symlinked_destination_parent_without_external_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "project"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            sentinel = outside / "keep.txt"
            sentinel.write_text("outside stays unchanged", encoding="utf-8")
            linked_parent = target / "02-characters"
            try:
                linked_parent.symlink_to(outside, target_is_directory=True)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"Symlinks unavailable: {exc}")

            with self.assertRaises(ValueError):
                initialize(target, ["角色甲"], "scene", False)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside stays unchanged")
            self.assertEqual({path.name for path in outside.iterdir()}, {"keep.txt"})

    def test_force_rejects_hard_linked_template_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "project"
            target.mkdir()
            external = root / "external-project.yaml"
            external.write_text("external: unchanged\n", encoding="utf-8")
            os.link(external, target / "project.yaml")

            with self.assertRaises(ValueError):
                initialize(target, [], "scene", True)

            self.assertEqual(external.read_text(encoding="utf-8"), "external: unchanged\n")

    def test_force_rejects_hard_linked_speech_samples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "project"
            initialize(target, ["A"], "scene", False)
            speech_path = target / "02-characters" / "a" / "speech-samples.md"
            speech_path.unlink()
            external = root / "external-speech.md"
            external.write_text("private external speech\n", encoding="utf-8")
            os.link(external, speech_path)

            with self.assertRaises(ValueError):
                initialize(target, ["A"], "scene", True)

            self.assertEqual(external.read_text(encoding="utf-8"), "private external speech\n")

    def test_force_still_replaces_an_existing_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project"
            initialize(target, [], "scene", False)
            project_file = target / "project.yaml"
            project_file.write_text("custom: stale\n", encoding="utf-8")

            created, skipped = initialize(target, [], "scene", True)

            self.assertIn(project_file, created)
            self.assertEqual(skipped, [])
            self.assertNotEqual(project_file.read_text(encoding="utf-8"), "custom: stale\n")


class DialogueAuditTests(unittest.TestCase):
    def test_clean_dialogue_has_no_configured_warnings(self) -> None:
        text = (FIXTURES / "clean-dialogue.fountain").read_text(encoding="utf-8")
        self.assertEqual(audit_text(text), [])

    def test_problem_dialogue_flags_exposition_summary_and_duplicate(self) -> None:
        text = (FIXTURES / "problem-dialogue.fountain").read_text(encoding="utf-8")
        codes = {item.code for item in audit_text(text)}
        self.assertTrue({"as-you-know", "generic-summary", "duplicate-line"}.issubset(codes))


class StoryboardAuditTests(unittest.TestCase):
    def test_empty_storyboard_is_an_error(self) -> None:
        findings = audit_rows([])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].code, "no-shots")
        self.assertEqual(findings[0].severity, "error")

    def test_valid_storyboard_passes(self) -> None:
        self.assertEqual(audit_rows(load_rows(FIXTURES / "valid-storyboard.csv")), [])

    def test_invalid_storyboard_reports_hard_and_soft_failures(self) -> None:
        findings = audit_rows(load_rows(FIXTURES / "invalid-storyboard.csv"))
        codes = {item.code for item in findings}
        self.assertTrue({"duplicate-shot-id", "nonpositive-duration", "timeline-overlap", "missing-field", "generic-duty"}.issubset(codes))
        self.assertTrue(any(item.severity == "error" for item in findings))

    def test_nonfinite_time_and_tolerance_are_errors(self) -> None:
        row = {
            "shot_id": "S001",
            "start_s": "nan",
            "end_s": "inf",
            "duty": "Reveal the decision",
            "visual": "She closes the case",
            "framing": "medium",
            "movement": "static",
            "performance": "hand releases",
            "dialogue_sound": "room tone",
            "continuity": [],
        }
        self.assertIn("invalid-time", {item.code for item in audit_rows([row])})
        self.assertEqual(audit_rows([row], tolerance=float("inf"))[0].code, "invalid-tolerance")
        self.assertEqual(audit_rows([row], expected_duration=float("nan"))[0].code, "invalid-expected-duration")

    def test_canonical_storyboard_aliases_pass_json_loading(self) -> None:
        shot = {
            "shot_id": "S001",
            "start_s": 0,
            "end_s": 8,
            "duty": "Let the audience see her decision land",
            "visual_event": "She closes the case",
            "framing_and_angle": "medium eye-level",
            "camera_behavior": "static",
            "movement_motive": None,
            "blocking": [],
            "performance_cause": "doorbell makes her release the handle",
            "dialogue_sound": "doorbell, then room tone",
            "continuity": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "storyboard.json"
            path.write_text(json.dumps({"shots": [shot]}), encoding="utf-8")
            self.assertEqual(audit_rows(load_rows(path), expected_duration=8), [])

    def test_canonical_storyboard_aliases_pass_yaml_loading(self) -> None:
        yaml_text = """shots:
  - shot_id: S001
    start_s: 0
    end_s: 8
    duty: Let the audience see her decision land
    visual_event: She closes the case
    framing_and_angle: medium eye-level
    camera_behavior: static
    movement_motive: null
    blocking: []
    performance_cause: doorbell makes her release the handle
    dialogue_sound: doorbell, then room tone
    continuity: []
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "storyboard.yaml"
            path.write_text(yaml_text, encoding="utf-8")
            self.assertEqual(audit_rows(load_rows(path), expected_duration=8), [])

    def test_exact_duration_mode_escalates_gaps_and_checks_final_end(self) -> None:
        rows = [
            dict(load_rows(FIXTURES / "valid-storyboard.csv")[0]),
            dict(load_rows(FIXTURES / "valid-storyboard.csv")[1]),
        ]
        rows[1]["start_s"] = "9"
        rows[1]["end_s"] = "12"
        findings = audit_rows(rows, expected_duration=14)
        errors = {item.code for item in findings if item.severity == "error"}
        self.assertTrue({"timeline-gap", "duration-mismatch"}.issubset(errors))


class RepositoryTests(unittest.TestCase):
    def test_validator_missing_yaml_reports_only_the_dependency_error(self) -> None:
        result = subprocess.run(
            [sys.executable, "-I", "-S", "-B", str(ROOT / "scripts" / "validate_repo.py"), str(ROOT)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("ERROR PyYAML is required"))
        self.assertIn("python -m pip install -r requirements-dev.txt", lines[0])
        self.assertEqual(lines[1], "Validation failed: 1 error(s).")

    def test_repository_contract(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_public_archive_install_preserves_internal_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            install_root = Path(directory) / "skills"
            internal = install_root / "role2reel" / "SKILL.md"
            internal.parent.mkdir(parents=True)
            internal.write_text("private customization", encoding="utf-8")
            _, archive_path = package(Path(directory) / "public.zip")
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(install_root)
            self.assertEqual(internal.read_text(encoding="utf-8"), "private customization")
            self.assertEqual(validate(install_root / "role2reel-public"), [])

    def test_public_validator_rejects_internal_or_ambiguous_identity(self) -> None:
        variants = [
            ("SKILL.md", "name: role2reel-public", "name: role2reel", "name must be"),
            ("agents/openai.yaml", "$role2reel-public", "$role2reel", "default_prompt"),
            ("agents/openai.yaml", "$role2reel-public", "$role2reel-public-extra", "default_prompt"),
            ("agents/openai.yaml", 'display_name: "Role2Reel Public"', 'display_name: "Role2Reel"', "display_name"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "role2reel-public"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            for relative, old, new, error in variants:
                with self.subTest(relative=relative, identity=new):
                    target = clone / relative
                    original = target.read_text(encoding="utf-8")
                    self.assertIn(old, original)
                    try:
                        target.write_text(original.replace(old, new), encoding="utf-8")
                        self.assertTrue(any(error in item for item in validate(clone)))
                    finally:
                        target.write_text(original, encoding="utf-8")

    def test_package_contains_skill_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            count, archive_path = package(Path(directory) / "role2reel-public.zip")
            self.assertGreater(count, 20)
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            expected = {f"role2reel-public/{name}" for name in RELEASE_FILES}
            self.assertEqual(count, len(RELEASE_FILES))
            self.assertEqual(names, expected)

    def test_package_allowlist_excludes_unlisted_private_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            for relative in RELEASE_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            (root / ".env").write_text("SECRET=value", encoding="utf-8")
            private = root / "test-results" / "private-output.txt"
            private.parent.mkdir(parents=True)
            private.write_text("private", encoding="utf-8")
            archive_path = Path(directory) / "release.zip"
            count, _ = package(archive_path, root=root)
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            self.assertEqual(count, len(RELEASE_FILES))
            self.assertNotIn("role2reel-public/.env", names)
            self.assertNotIn("role2reel-public/test-results/private-output.txt", names)

    def test_package_rejects_source_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            for relative in RELEASE_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            with self.assertRaises(ValueError):
                package(root / "README.md", root=root)

    def test_package_rejects_hard_link_to_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            for relative in RELEASE_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            output = Path(directory) / "release.zip"
            os.link(root / "README.md", output)
            with self.assertRaises(ValueError):
                package(output, root=root)
            self.assertEqual((root / "README.md").read_text(encoding="utf-8"), "fixture")

    def test_package_rejects_symlinked_member(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            for relative in RELEASE_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            external = Path(directory) / "external-skill.md"
            external.write_text("private external material", encoding="utf-8")
            member = root / "SKILL.md"
            member.unlink()
            try:
                member.symlink_to(external)
            except OSError as exc:
                self.skipTest(f"Symlinks unavailable: {exc}")
            with self.assertRaises(ValueError):
                package(Path(directory) / "release.zip", root=root)

    def test_validator_handles_external_root_under_ignored_named_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "dist" / "role2reel-public"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            self.assertEqual(validate(clone), [])
            broken = clone / "scripts" / "broken.py"
            broken.write_text("def broken(:\n", encoding="utf-8")
            errors = validate(clone)
            self.assertTrue(any("Python syntax error in scripts" in error for error in errors))

    def test_validator_ignores_local_forward_run_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "role2reel-public"
            shutil.copytree(
                ROOT,
                clone,
                ignore=shutil.ignore_patterns(".git", "dist", "test-results", "__pycache__"),
            )
            results = clone / "test-results"
            results.mkdir()
            (results / "private-run.py").write_text("def not_valid(:\n", encoding="utf-8")
            self.assertEqual(validate(clone), [])

    def test_validator_rejects_malformed_yaml_and_template_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "role2reel-public"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            metadata = clone / "agents" / "openai.yaml"
            metadata.write_text(metadata.read_text(encoding="utf-8") + "\nmalformed: [\n", encoding="utf-8")
            template = clone / "assets" / "templates" / "project.yaml"
            template.unlink()
            template.mkdir()
            errors = validate(clone)
            self.assertTrue(any("Invalid YAML in agents" in error for error in errors))
            self.assertIn("Missing regular template file: assets/templates/project.yaml", errors)

    def test_validator_reports_invalid_utf8_yaml_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "role2reel-public"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            (clone / "bad.yaml").write_bytes(b"key: \xff\n")
            errors = validate(clone)
            self.assertTrue(any("Unreadable UTF-8 file in bad.yaml" in error for error in errors))

    def test_validator_reports_invalid_utf8_skill_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "role2reel-public"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            (clone / "SKILL.md").write_bytes(b"---\nname: \xff\n---\n")
            errors = validate(clone)
            self.assertTrue(any("Unreadable UTF-8 file in SKILL.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
