import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_public_export import audit, main


def synthetic_payload(length):
    # Build test data at runtime so the release scanner can audit its own tests.
    alphabet = 'Ab7Cd9Ef2Gh4Jk6Mn8Pq0Rs3Tu5Vw1Xy'
    return (alphabet * (length // len(alphabet) + 1))[:length]


def synthetic_chat_id():
    return '-'.join(('12345678', 'abcd', '4abc', '9def', '123456789abc'))


class ExportTests(unittest.TestCase):
    def test_unlisted_project_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit(Path(d), ['private-story.txt']), [('private-story.txt', 'outside-release-allowlist')])

    def test_confidential_match_is_redacted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SKILL.md').write_text('Synthetic confidential marker: OrchardExperiment42')
            result = audit(root, ['SKILL.md'], ['OrchardExperiment42'])
            self.assertEqual(result, [('SKILL.md', 'private-term')])
            self.assertNotIn('OrchardExperiment42', repr(result))

    def test_generic_content_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SKILL.md').write_text('Preserve identity; derive wardrobe from the local script.')
            self.assertEqual(audit(root, ['SKILL.md']), [])

    def test_user_paths_are_detected_without_disclosing_the_path(self):
        backslash = chr(92)
        profile = 'Synthetic Profile-42'
        cases = [
            backslash.join(['C:', 'Users', profile, 'draft.txt']),
            (backslash * 2).join(['C:', 'Users', profile, 'draft.txt']),
            'd:' + backslash + 'uSeRs/' + profile + backslash + 'draft.txt',
            backslash.join(['E:', 'Users', '合成用户', 'draft.txt']),
            '/'.join(['C:', 'Users', 'SyntheticProfile42', 'draft.txt']),
            '/'.join(['', 'Users', 'SyntheticProfile42', 'draft.txt']),
            '/'.join(['', 'home', 'SyntheticProfile42', 'draft.txt']),
        ]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for content in cases:
                with self.subTest(content=content):
                    (root/'SKILL.md').write_text(content, encoding='utf-8')
                    result = audit(root, ['SKILL.md'])
                    self.assertEqual(result, [('SKILL.md', 'absolute-user-path')])
                    self.assertNotIn(content, repr(result))

    def test_generic_path_examples_are_not_concrete_user_profiles(self):
        backslash = chr(92)
        cases = [
            backslash.join(['C:', 'Users', '<username>', 'project']),
            '/'.join(['C:', 'Users', '<username>', 'project']),
            backslash.join(['D:', 'workspace', 'project']),
            backslash.join(['Users', 'SyntheticProfile42', 'project']),
        ]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for content in cases:
                with self.subTest(content=content):
                    (root/'SKILL.md').write_text(content, encoding='utf-8')
                    self.assertEqual(audit(root, ['SKILL.md']), [])

    def test_common_api_credentials_are_detected_and_redacted(self):
        cases = {
            'openai-legacy': 'sk-' + synthetic_payload(48),
            'openai-project': 'sk-proj-' + synthetic_payload(140),
            'openai-service-account': 'sk-svcacct-' + synthetic_payload(140),
            'anthropic': 'sk-ant-api03-' + synthetic_payload(95),
            'github-classic': 'ghp_' + synthetic_payload(36),
            'github-oauth': 'gho_' + synthetic_payload(36),
            'github-fine-grained': 'github_pat_' + synthetic_payload(82),
            'hugging-face': 'hf_' + synthetic_payload(34),
            'service-api-token': 'ak_' + synthetic_payload(24),
            'google': 'AIza' + synthetic_payload(35),
            'slack': 'xoxb-' + '-'.join(('123456789012', '345678901234', synthetic_payload(24))),
            'stripe': 'sk_live_' + synthetic_payload(32),
            'aws': 'AKIA' + synthetic_payload(16).upper(),
        }
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for provider, credential in cases.items():
                with self.subTest(provider=provider):
                    (root/'SKILL.md').write_text('api_key = "' + credential + '"', encoding='utf-8')
                    result = audit(root, ['SKILL.md'])
                    self.assertEqual(result, [('SKILL.md', 'api-credential')])
                    self.assertNotIn(credential, repr(result))

    def test_documentation_placeholders_and_task_ids_are_not_credentials(self):
        cases = [
            'sk-<YOUR_API_KEY>',
            'sk-proj-${OPENAI_API_KEY}',
            'sk-' + 'x' * 48,
            'sk-proj-' + '-'.join(('your', 'openai', 'api', 'key', 'placeholder', 'here')),
            'ghp_' + 'X' * 36,
            'hf_' + 'example_' * 6,
            'ak_<YOUR_API_KEY>',
            'ak_' + 'X' * 24,
            'AIza' + '0' * 35,
            'task-' + synthetic_payload(48),
            'mytask-' + synthetic_payload(48),
            'task-sk-' + synthetic_payload(48),
            'task-ak_' + synthetic_payload(32),
            'https://github.com/example/public-repository/issues/123',
            'https://chatgpt.com/share/<conversation-id>',
            'https://copilot.microsoft.com/shares/your-conversation-id',
            'chatgpt-conversation://<conversation-id>',
        ]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for index, content in enumerate(cases):
                with self.subTest(case=index):
                    (root/'SKILL.md').write_text(content, encoding='utf-8')
                    self.assertEqual(audit(root, ['SKILL.md']), [])

    def test_private_chat_links_are_detected_without_exposing_identifiers(self):
        chat_id = synthetic_chat_id()
        cases = [
            'https://chatgpt.com/share/' + chat_id,
            'https://chatgpt.com/c/' + chat_id + '?model=example',
            'https://chat.openai.com/share/' + chat_id,
            'https://claude.ai/share/' + chat_id,
            'https://claude.ai/chat/' + chat_id,
            'https://gemini.google.com/share/' + '12ab' * 3,
            'https://g.co/gemini/share/' + '34cd' * 3,
            'https://copilot.microsoft.com/shares/' + synthetic_payload(24),
            'https://grok.com/share/' + chat_id,
            'chatgpt-conversation://' + chat_id,
        ]
        cases.append(cases[0].replace('/', chr(92) + '/'))
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for index, url in enumerate(cases):
                with self.subTest(case=index):
                    (root/'SKILL.md').write_text(url, encoding='utf-8')
                    result = audit(root, ['SKILL.md'])
                    self.assertEqual(result, [('SKILL.md', 'private-chat-url')])
                    self.assertNotIn(url, repr(result))
                    self.assertNotIn(chat_id, repr(result))

    def test_matching_word_inside_a_credential_does_not_hide_it(self):
        content = 'sk-' + synthetic_payload(20) + 'example' + synthetic_payload(20)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SKILL.md').write_text(content, encoding='utf-8')
            self.assertEqual(audit(root, ['SKILL.md']), [('SKILL.md', 'api-credential')])

    def test_existing_missing_binary_and_private_key_checks_remain_active(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(audit(root, ['SKILL.md']), [('SKILL.md', 'missing-or-symlink')])
            (root/'SKILL.md').write_bytes(bytes((255, 254, 0)))
            self.assertEqual(audit(root, ['SKILL.md']), [('SKILL.md', 'binary-requires-review')])
            (root/'SKILL.md').write_text('-' * 5 + 'BEGIN PRIVATE KEY' + '-' * 5, encoding='utf-8')
            self.assertEqual(audit(root, ['SKILL.md']), [('SKILL.md', 'private-key')])

    def test_cli_reports_only_paths_and_categories(self):
        credential = 'sk-proj-' + synthetic_payload(96)
        url = 'https://chatgpt.com/share/' + synthetic_chat_id()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SKILL.md').write_text(credential + '\n' + url, encoding='utf-8')
            output = io.StringIO()
            with patch('audit_public_export.RELEASE_FILES', ('SKILL.md',)), \
                    patch.object(sys, 'argv', ['audit_public_export.py', '--root', d]), \
                    contextlib.redirect_stdout(output):
                self.assertTrue(main())
            report = output.getvalue()
            self.assertIn('api-credential: SKILL.md', report)
            self.assertIn('private-chat-url: SKILL.md', report)
            self.assertNotIn(credential, report)
            self.assertNotIn(url, report)
            self.assertNotIn(d, report)

    def test_scanner_and_its_synthetic_test_source_pass_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(audit(root, ['scripts/audit_public_export.py', 'tests/test_public_export.py']), [])

    def test_cli_reads_chinese_private_rules_explicitly_as_utf8(self):
        private_term = '合成隐私测试标记'
        original_read_text = Path.read_text
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            rules = root/'private-rules.json'
            rules.write_text(json.dumps([private_term], ensure_ascii=False), encoding='utf-8')
            (root/'SKILL.md').write_text(private_term, encoding='utf-8')
            output = io.StringIO()
            with patch('audit_public_export.RELEASE_FILES', ('SKILL.md',)), \
                    patch.object(sys, 'argv', ['audit_public_export.py', '--root', d,
                                              '--private-rules', str(rules)]), \
                    patch.object(Path, 'read_text', autospec=True,
                                 side_effect=original_read_text) as read_text, \
                    contextlib.redirect_stdout(output):
                self.assertTrue(main())
                read_text.assert_any_call(rules, encoding='utf-8')
            report = output.getvalue()
            self.assertIn('private-term: SKILL.md', report)
            self.assertNotIn(private_term, report)
            self.assertNotIn(str(rules), report)
