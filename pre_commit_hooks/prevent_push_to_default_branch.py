from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


__REPO_PATH: str = ''


def _run_cmd(
    cmd: str,
) -> tuple[bool, str]:
    proc = subprocess.Popen(  # noqa: S603
        shlex.split(cmd),
        cwd=__REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_b, stderr_b = proc.communicate()
    stdout = stdout_b.decode().strip()
    stderr = stderr_b.decode().strip()
    if proc.returncode != 0:
        print(
            f'Failed to get current branch. Command: "{cmd}". '
            f'Return code {proc.returncode}. '
            f'Stderr: "{stderr}".',
            file=sys.stderr,
        )
        return False, stderr
    return True, stdout


def _get_origins() -> tuple[bool, list[str]]:
    ok, origins = _run_cmd('git remote')
    if not ok:
        return False, []
    return True, [o.strip() for o in origins.split('\n')]


def _get_current_branch_name() -> str:
    ok, current_branch_raw = _run_cmd(
            'git rev-parse --abbrev-ref HEAD',
        )
    if not ok:
        return ''
    current_branch = current_branch_raw.replace('\n', '')
    if not current_branch:
        print(
            f'Failed to parse current branch from "{current_branch}"',
            file=sys.stderr,
        )
        return ''
    return current_branch


def _get_default_branch_from_origin(origin: str) -> str:
    ok, origin_info = _run_cmd(
        f'git remote show {origin}',
    )
    if not ok:
        return ''
    match = re.search(r'HEAD branch: (.*)\n', origin_info)
    if not match or len(match.groups()) != 1:
        print(
            f'Failed to parse default branch from "{origin_info}"',
            file=sys.stderr,
        )
        return ''
    return match.groups()[0]


def main(argv: Sequence[str] = '.') -> int:
    global __REPO_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument('repo', nargs='*')
    args = parser.parse_args(argv)
    __REPO_PATH = ''.join(args.repo)

    current_branch = _get_current_branch_name()
    if not current_branch:
        return 1

    ok, origins = _get_origins()
    if not ok:
        return 1

    for origin in origins:
        default_branch = _get_default_branch_from_origin(origin)
        if not default_branch:
            return 1
        if current_branch == default_branch:
            print(
                f'Do not commit to default branch "{default_branch}" '
                f'from "{origin}".',
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
