import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Generator

import pytest  # type: ignore[import-not-found]

from pre_commit_hooks.prevent_push_to_default_branch import main


@pytest.fixture
def repo_dir() -> str:
    if sys.version_info < (3, 12):
        repo_dir = tempfile.TemporaryDirectory(
            prefix='pre-commit-hook-prevent-push',
        )
    else:
        repo_dir = tempfile.TemporaryDirectory(
            prefix='pre-commit-hook-prevent-push',
            delete=False,
        )
    return repo_dir.name


@pytest.fixture(autouse=True)
def setup_teardown(repo_dir: str) -> Generator:
    repo_url = 'https://github.com/octocat/Hello-World'
    args = shlex.split(f'git clone {repo_url} {repo_dir}')
    proc = subprocess.run(args, capture_output=True)  # noqa: S603
    print(
        f'Repo cloning: {proc.stderr.decode()} '
        f'(returncode: {proc.returncode})',
    )
    yield
    shutil.rmtree(repo_dir)


def test_commit_to_default_branch(repo_dir: str) -> None:
    retcode = main(repo_dir)
    assert retcode == 1


def test_commit_to_non_default_branch(repo_dir: str) -> None:
    args = shlex.split('git switch test')
    proc = subprocess.run(  # noqa: S603
        args,
        cwd=repo_dir,
        capture_output=True,
    )
    print(
        f'Changing branch: {proc.stderr.decode()} '
        f'(returncode: {proc.returncode})',
    )
    retcode = main(repo_dir)
    assert retcode == 0
