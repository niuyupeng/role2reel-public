#!/usr/bin/env python3
"""Audit the explicit release inventory; optional confidential terms stay local."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from package_skill import RELEASE_FILES


# Match recognizable provider formats, not arbitrary long IDs or task names.
# Capture only the payload so obvious documentation placeholders can be ignored.
_TOKEN_BOUNDARY = r'(?<![A-Za-z0-9_-])'
_TOKEN_END = r'(?![A-Za-z0-9_-])'
_CREDENTIAL_PATTERNS = tuple(re.compile(_TOKEN_BOUNDARY + pattern + _TOKEN_END) for pattern in (
    r'sk-(?:(?:proj|svcacct)-|ant-(?:api|admin)\d{2}-)?(?P<payload>[A-Za-z0-9_-]{32,})',
    r'gh[pousr]_(?P<payload>[A-Za-z0-9]{36,})',
    r'github_pat_(?P<payload>[A-Za-z0-9_]{60,})',
    r'hf_(?P<payload>[A-Za-z0-9]{30,})',
    r'ak_(?P<payload>[A-Za-z0-9]{24,})',
    r'AIza(?P<payload>[A-Za-z0-9_-]{35})',
    r'xox[baprs]-(?P<payload>[A-Za-z0-9-]{24,})',
    r'(?:sk|rk)_live_(?P<payload>[A-Za-z0-9]{24,})',
    r'(?:AKIA|ASIA)(?P<payload>[A-Z0-9]{16})',
))
_PLACEHOLDER_WORDS = frozenset((
    'your', 'api', 'access', 'secret', 'key', 'token', 'placeholder', 'example',
    'sample', 'test', 'dummy', 'replace', 'this', 'here', 'with', 'insert',
    'redacted', 'masked', 'value', 'openai', 'anthropic', 'github', 'google',
    'huggingface', 'stripe', 'slack', 'project', 'service', 'account', 'public',
    'conversation', 'chat', 'share', 'id', 'link',
))


def _is_placeholder(payload):
    # Do not suppress a real token merely because it contains an example word.
    lowered = payload.casefold()
    if len(set(lowered.replace('-', '').replace('_', ''))) <= 1:
        return True
    words = [word for word in re.split(r'[-_]+', lowered) if word]
    return bool(words) and all(word in _PLACEHOLDER_WORDS for word in words)


_UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
_PRIVATE_CHAT_PATTERNS = tuple(re.compile(pattern, re.I) for pattern in (
    r'chatgpt-conversation://' + _UUID,
    r'https?://(?:www\.)?(?:chatgpt\.com|chat\.openai\.com)/(?:share|c)/' + _UUID,
    r'https?://(?:www\.)?claude\.ai/(?:share|chat)/' + _UUID,
    r'https?://(?:gemini\.google\.com/share|g\.co/gemini/share)/[0-9a-f]{8,}',
    r'https?://(?:www\.)?copilot\.microsoft\.com/shares/[A-Za-z0-9_-]{12,}',
    r'https?://(?:www\.)?grok\.com/share/' + _UUID,
))


def _contains_private_chat_url(content):
    # JSON exports may escape URL separators; never return the matched URL.
    for pattern in _PRIVATE_CHAT_PATTERNS:
        for match in pattern.finditer(content.replace(r'\/', '/')):
            if not _is_placeholder(match.group().rsplit('/', 1)[-1]):
                return True
    return False


def audit(root, names, private_terms=()):
    findings = []
    allowed = set(RELEASE_FILES)
    for name in names:
        path = root / name
        if name not in allowed:
            findings.append((name, 'outside-release-allowlist'))
            continue
        if path.is_symlink() or not path.is_file():
            findings.append((name, 'missing-or-symlink'))
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            findings.append((name, 'binary-requires-review'))
            continue
        if any(term and term.casefold() in content.casefold() for term in private_terms):
            findings.append((name, 'private-term'))
        unix_user_path = re.search(r'(?:/Users/|/home/)[A-Za-z0-9_.-]+/', content)
        # Accept native, mixed and JSON-escaped separators; an angle-bracket
        # username placeholder is not evidence of a concrete local profile.
        windows_user_path = re.search(
            r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/\r\n:*?"<>|]+[\\/]',
            content,
            re.I,
        )
        if unix_user_path or windows_user_path:
            findings.append((name, 'absolute-user-path'))
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', content):
            findings.append((name, 'private-key'))
        if any(not _is_placeholder(match.group('payload'))
               for pattern in _CREDENTIAL_PATTERNS for match in pattern.finditer(content)):
            findings.append((name, 'api-credential'))
        if _contains_private_chat_url(content):
            findings.append((name, 'private-chat-url'))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--tracked', action='store_true')
    parser.add_argument('--private-rules', type=Path)
    args = parser.parse_args()
    names = list(RELEASE_FILES)
    if args.tracked:
        names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=args.root).decode().strip('\0').split('\0')
    terms = json.loads(args.private_rules.read_text(encoding='utf-8')) if args.private_rules else []
    if not isinstance(terms, list) or not all(isinstance(t, str) for t in terms):
        parser.error('private rules must be a JSON array of strings')
    findings = audit(args.root, names, terms)
    for name, category in findings:
        print(f'{category}: {name}')
    print(f'Audited {len(names)} files; {len(findings)} findings. Semantic review remains required.')
    return bool(findings)


if __name__ == '__main__':
    raise SystemExit(main())
