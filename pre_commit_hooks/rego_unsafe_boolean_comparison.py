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
            search = re.search(r'(\!\=|\=\=)[\s]?(true|false)', line)
            if search:
                start_c, end_c = search.span()
                if start_c < 10:
                    start_c = 0
                else:
                    start_c -= 10
                if end_c - start_c > 30:
                    end_c = start_c + 30
                print(
                    f'  - Unsafe boolean comparison {line_no}: '
                    f'...{line[start_c:end_c].strip()}...',
                    file=sys.stderr,
                )
                ret_val = 1

    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
