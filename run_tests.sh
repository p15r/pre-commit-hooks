#!/usr/bin/env bash

set -euxo pipefail

function die () {
	echo "Error: ${1}"
	exit 1
}

function is_tox_installed () {
	error_msg="Please install tox-uv (https://github.com/tox-dev/tox-uv?tab=readme-ov-file#how-to-use)"

	if ! [ -x "$(command -v tox)" ]; then
		die "${error_msg}"
	fi

	tox_version=$(tox --version)
	if ! [[ "${tox_version}" == *"tox-uv"* ]]; then
		die "${error_msg}"
	fi
}

function main() {
	is_tox_installed
	tox -r -- ${@:-}    # `tox -r -posarg` sends `-posarg` to uv
}

main ${@:-}
