from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    ret_val = 0

    for filename in args.filenames:
        print(f'Checking {filename}...')

        with Path.open(filename) as f_handle:
            rego = f_handle.readlines()

        for line_no, line in enumerate(rego, start=1):
            print(f'Processing line no {line_no}') 

    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
