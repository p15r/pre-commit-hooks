from __future__ import annotations

import argparse
import re
import sys
from typing import Sequence


MAX_OUTPUT_CMD_LENGTH = 40


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    issue_detected = False

    ret_val = 0

    for filename in args.filenames:
        print(f'Checking {filename}...')

        with open(filename, 'r') as f_handle:
            md = f_handle.readlines()

        line_no = 0
        for line in md:
            line_no += 1
            line = line.strip().replace('\n', '')
            search = re.search(r'.*&& \\$', line)
            if search:
                issue_detected = True
                dots = ''
                start_c, end_c = search.span()
                if end_c - start_c > MAX_OUTPUT_CMD_LENGTH:
                    start_c = end_c - MAX_OUTPUT_CMD_LENGTH
                    dots = '...'

                print(
                    f'  - multi-line command on line {line_no}: '
                    f'{dots}'
                    f'{line[start_c:]}',
                    file=sys.stderr
                )
                ret_val = 1

    if issue_detected:
        remediation = '''\n  Change to format:
    RUN : \\
        && ls \\
        && ls -lha \\
        && :'''

        print(remediation)

    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
