#!/usr/bin/env bash

set -euxo pipefail

TOX_SETUP="-r -vv --notest"
TOX_RUN="-r --skip-pkg-install"

PY_VER=$(
    python -c \
    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    )
PY_VER_MAJOR=${PY_VER: 0:1}
PY_VER_MINOR=${PY_VER: 2}

if [[ $PY_VER_MAJOR != 3 ]]; then
    echo "Python $PY_VER is not supported..."
    exit 1
fi

if [[ $PY_VER_MINOR == 6 ]]; then
    TOX_BIN=$(which tox4)

    $TOX_BIN $TOX_SETUP
    $TOX_BIN $TOX_RUN -- "${@}"
    exit $?
fi

TOX_BIN=$(which tox)
$TOX_BIN $TOX_SETUP
$TOX_BIN $TOX_RUN -- "${@}"
exit $?
