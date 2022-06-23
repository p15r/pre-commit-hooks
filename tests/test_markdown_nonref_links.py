from pre_commit_hooks.markdown_detect_nonref_links import main


def test_failing_file():
    ret = main(['tests/harness/nonrefs.md', 'tests/harness/refs.md'])
    assert ret == 1


def test_passing_file():
    ret = main(['tests/harness/refs.md'])
    assert ret == 0
