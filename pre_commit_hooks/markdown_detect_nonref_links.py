from __future__ import annotations

import argparse
import re
import sys
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    ret_val = 0

    for filename in args.filenames:
        print(f'Checking {filename}...')

        with open(filename, 'r') as f_handle:
            md = f_handle.readlines()

        line_no = 0
        for line in md:
            line_no += 1
            search = re.search(r'[\!]?\[.*\]\([^#mailto\:].*\)', line)
            if search:
                start_c, end_c = search.span()
                if end_c - start_c > 40:
                    end_c = start_c + 40
                print(
                    f'  - Non-ref link on line {line_no}: '
                    f'{line[start_c: end_c]}...',
                    file=sys.stderr
                )
                ret_val = 1

    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
