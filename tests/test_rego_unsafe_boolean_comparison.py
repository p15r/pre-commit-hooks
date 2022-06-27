from pre_commit_hooks.rego_unsafe_boolean_comparison import main


def test_failing_file(capsys):
    expected = (
        '  - Unsafe boolean comparison 22: ...e_enabled != true...\n'
        '  - Unsafe boolean comparison 40: ...input == true...\n'
        '  - Unsafe boolean comparison 43: ...input==true...\n'
        '  - Unsafe boolean comparison 46: ...input != true...\n'
        '  - Unsafe boolean comparison 49: ...input == false...\n'
        '  - Unsafe boolean comparison 52: ...input != false...\n'
    )

    ret = main(['tests/harness/unsafe_boolean_comparison.rego'])
    captured = capsys.readouterr()
    assert ret == 1
    assert captured.err == expected


def test_passing_file():
    ret = main(['tests/harness/safe_boolean_comparison.rego'])
    assert ret == 0
