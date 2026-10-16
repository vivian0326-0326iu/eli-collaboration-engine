#!/usr/bin/env python3
"""Conservative text scan for obvious secrets and private locations; not a security guarantee."""
from __future__ import annotations
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXCLUDE = {'__pycache__', '.git', '.eli-engine'}
CHECKS = {
    'private_absolute_mac_home': re.compile(r'/Users/(?!USERNAME\b|yourname\b|<)[A-Za-z0-9._-]{3,}/'),
    'openai_like_secret': re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    'github_personal_token': re.compile(r'\b(?:ghp|github_pat)_[A-Za-z0-9_]{16,}'),
    'actual_ngrok_domain': re.compile(r'\b[a-z0-9-]{9,}\.ngrok-free\.dev\b'),
}

def main() -> int:
    violations = []
    count = 0
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(x in path.parts for x in EXCLUDE) or path.suffix in {'.png','.jpg','.zip','.pyc'}:
            continue
        count += 1
        text = path.read_text(encoding='utf-8')
        for key, regex in CHECKS.items():
            for match in regex.finditer(text):
                violations.append(f'{path.relative_to(ROOT)}: {key}: bytes {match.start()}-{match.end()}')
    for v in violations: print('CHECK:', v, file=sys.stderr)
    print(f'Scanned {count} text files; flagged {len(violations)} patterns.')
    print('Note: This is a simple pattern scan, not proof no private data is present.')
    return 1 if violations else 0

if __name__ == '__main__': raise SystemExit(main())
