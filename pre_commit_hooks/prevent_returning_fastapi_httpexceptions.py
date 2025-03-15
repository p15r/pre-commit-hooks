from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import astroid
from astroid import nodes

if TYPE_CHECKING:
    from collections.abc import Sequence

EXCEPTION_NAMES = {'AFKException', 'HTTPException', 'WebSocketException'}


def walk_astroid_tree(node: nodes.NodeNG):
    """Recursively yield each node in the Astroid tree (similar to node.walk())."""
    yield node
    for child in node.get_children():
        yield from walk_astroid_tree(child)


def find_http_exception_returns(file_path: str) -> list[int]:
    """Parse `file_path` using astroid and return the line numbers of Return statements
    that return a Call to one of the EXCEPTION_NAMES.
    """
    code = Path(file_path).read_text(encoding='utf-8')
    module_node = astroid.parse(code, path=file_path)

    lines_with_exceptions = []
    for node in walk_astroid_tree(module_node):
        # Look for Return nodes
        if isinstance(node, nodes.Return) and node.value is not None:
            # We only care if the returned value is a Call
            if isinstance(node.value, nodes.Call):
                func = node.value.func
                # Could be a Name(...) or an Attribute(...), e.g. MyMod.HTTPException
                if isinstance(func, nodes.Name):
                    if func.name in EXCEPTION_NAMES:
                        lines_with_exceptions.append(node.lineno)
                elif isinstance(func, nodes.Attribute):
                    # If you need to handle something like some_module.HTTPException
                    # you can look at `func.attrname`:
                    if func.attrname in EXCEPTION_NAMES:
                        lines_with_exceptions.append(node.lineno)

    return lines_with_exceptions


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    ret_val = 0
    for target_file in args.filenames:
        exception_lines = find_http_exception_returns(target_file)
        for line_no in exception_lines:
            ret_val = 1
            print(
                f'{target_file}:{line_no} returns HTTP exception (`raise` instead)',
                file=sys.stderr,
            )
    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
