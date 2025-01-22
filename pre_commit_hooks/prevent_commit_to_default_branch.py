from __future__ import annotations

import argparse
import re
import shlex
import subprocess  # nosec: B404
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

# TODO(patrick): update `.python-requires` (and other places) that require
#   minimum Python version with this syntax ("|" in type hints,
#   or "tuple" in type hints)
# TODO(patrick): update pre-commit config of this repo, then remove the
#   `# nosec` comments


def _run_cmd(cmd: str, suppress_error: str = '') -> tuple[bool, str]:
    proc = subprocess.Popen(  # noqa: S603 # nosec: B603
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_b, stderr_b = proc.communicate()
    stdout = stdout_b.decode().strip()
    stderr = stderr_b.decode().strip()
    if proc.returncode != 0:
        if suppress_error not in stderr:
            print(
                f'Failed to get current branch. Command: "{cmd}". '
                f'Return code {proc.returncode}. '
                f'Stderr: "{stderr}".',
            )
        return False, stderr
    return True, stdout


def _get_origins() -> tuple[bool, list[str]]:
    ok, origins = _run_cmd('git remote')
    if not ok:
        return False, []
    return True, [o.strip() for o in origins.split('\n')]


def _get_branch_name(default_branch_raw: str, origin: str, repo: str) -> str:
    match = re.search(rf'{origin}[/]?(.*){repo}', default_branch_raw)
    if not match or len(match.groups()) != 1:
        print(
            f'Failed to parse default branch from "{default_branch_raw}"',
            file=sys.stderr,
        )
        return ''
    return match.groups()[0]


def main(argv: Sequence[str] = '.') -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('repo')
    args = parser.parse_args(argv)

    ok, current_branch_raw = _run_cmd(
        f'git rev-parse --abbrev-ref HEAD {args.repo}',
    )
    if not ok:
        return 1
    current_branch = _get_branch_name(
        current_branch_raw.replace('\n', ''),
        '',
        args.repo,
    )

    ok, origins = _get_origins()
    if not ok:
        return 1

    for origin in origins:
        suppress_error = 'unknown revision or path not in the working tree'
        ok, default_branch_raw = _run_cmd(
            f'git rev-parse --abbrev-ref {origin}/HEAD {args.repo}',
            suppress_error,
        )
        if not ok and suppress_error in default_branch_raw:
            # refs not local available for this origin, can be safely ignored
            pass
        elif not ok:
            return 1
        default_branch = _get_branch_name(
            default_branch_raw.replace('\n', ''),
            origin,
            args.repo,
        )
        if current_branch == default_branch:
            print(
                f'Do not commit to default branch "{default_branch}" '
                f'on origin "{origin}".',
            )
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
