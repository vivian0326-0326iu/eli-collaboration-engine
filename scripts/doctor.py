#!/usr/bin/env python3
"""Offline preflight only. Does not inspect secrets, logins or perform installation."""
from __future__ import annotations
import argparse
import json
import platform
import shutil
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description='eli collaboration: noninvasive local preflight')
    p.add_argument('--project', default='.')
    args = p.parse_args()
    root = Path(args.project).expanduser().resolve()
    mac = platform.system() == 'Darwin'
    git = shutil.which('git') is not None
    codex = shutil.which('codex') is not None
    mac_mcp = shutil.which('mac-mcp') is not None or (Path.home() / '.local/bin/mac-mcp').exists()
    py_ok = tuple(__import__('sys').version_info[:2]) >= (3, 10)
    repo = False
    if git and root.is_dir():
        try:
            r = subprocess.run(['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'],
                               capture_output=True, text=True, timeout=5)
            repo = r.returncode == 0 and r.stdout.strip() == 'true'
        except (OSError, subprocess.TimeoutExpired):
            pass
    result = {'os': platform.system(), 'apple_silicon': platform.machine() == 'arm64' if mac else None,
              'python_310_or_newer': py_ok, 'git_cli': git, 'git_project': repo,
              'codex_cli': codex, 'mac_mcp_cli': mac_mcp,
              'chatgpt_mcp_plugin_available': 'NOT_VERIFIABLE_FROM_LOCAL_SHELL',
              'account_write_permissions': 'NOT_VERIFIABLE_FROM_LOCAL_SHELL',
              'codex_signin': 'NOT_CHECKED', 'public_https': 'NOT_CHECKED',
              'sensitive_configuration_read': False, 'external_model_calls': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not (mac and py_ok and git and repo):
        print('NOTICE: this Mac Git project has unmet local prerequisites; see docs/01-从零安装.md')
    print('Local CLI presence never proves ChatGPT connector permission or Codex sign-in.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
