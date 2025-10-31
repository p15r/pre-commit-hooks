from pre_commit_hooks.dockerfile_multiline_cmds import main


def test_failing_file():
    ret = main(['tests/harness/Dockerfile_bad'])
    assert ret == 1


def test_passing_file():
    ret = main(['tests/harness/Dockerfile_good'])
    assert ret == 0
