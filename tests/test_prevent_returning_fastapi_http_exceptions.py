from pre_commit_hooks.prevent_returning_fastapi_httpexceptions import main


def test_returning_http_exceptions(capsys):
    expected = (
        'tests/harness/return_httpexception.py:2 returns HTTP exception '
        '(`raise` instead)\n'
        'tests/harness/return_httpexception.py:8 returns HTTP exception '
        '(`raise` instead)\n'
        'tests/harness/return_httpexception.py:12 returns HTTP exception '
        '(`raise` instead)\n'
    )

    ret = main(['tests/harness/return_httpexception.py'])
    captured = capsys.readouterr()
    assert ret == 1
    assert captured.err == expected


def test_raise_http_exceptions():
    ret = main(['tests/harness/raise_httpexception.py'])
    assert ret == 0
