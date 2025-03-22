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


def walk_astroid_tree(node: nodes.NodeNG) -> nodes.NodeNG:
    """Recursively yield each node in the astroid tree.

    (similar to node.walk() in newer versions)
    """
    yield node
    for child in node.get_children():
        yield from walk_astroid_tree(child)


def is_call_to_known_exception(call_node: nodes.Call) -> bool:
    """Check if Call is to any name/attribute in EXCEPTION_NAMES."""
    func = call_node.func
    if isinstance(func, nodes.Name):
        return func.name in EXCEPTION_NAMES
    if isinstance(func, nodes.Attribute):
        return func.attrname in EXCEPTION_NAMES
    return False


def chase_assignments_for_exception(
    name_node: nodes.Name,
    scope_node: nodes.Scope,
) -> bool:
    """Manually chase all assignments for `name_node`.

    For each place `name_node` is assigned, look at the right-hand side (RHS).
    If that RHS is:
      - A direct call to a known exception, return True.
      - Another name, recursively chase that name as well.
    """
    assignments, inferred_values = scope_node.lookup(name_node.name)
    for inferred in inferred_values:
        if not isinstance(inferred, astroid.AssignName):
            continue

        parent = inferred.parent
        # Typically astroid.Assign, but could be AnnAssign etc.
        if isinstance(parent, astroid.Assign):
            rhs = parent.value
            if rhs is None:
                continue
            # Direct call to known exception
            if isinstance(rhs, nodes.Call) and is_call_to_known_exception(rhs):
                return True

            # Right-hand side is another Name; chase it recursively
            if isinstance(rhs, nodes.Name):  # noqa: SIM102
                if chase_assignments_for_exception(rhs, scope_node):
                    return True

    return False


def find_http_exception_returns(file_path: str) -> list[int]:
    """Parse `file_path` and return line numbers of Return statements.

    This is true if:
    - directly call a known exception, or
    - return a variable that is traced (via manual chasing) to be an instance
      of one.
    """
    code = Path(file_path).read_text(encoding='utf-8')
    module_node = astroid.parse(code, path=file_path)

    lines_with_exceptions = []
    for node in walk_astroid_tree(module_node):
        # Only consider Return nodes
        if isinstance(node, nodes.Return) and node.value is not None:
            ret_expr = node.value

            # Direct call in the return statement
            if isinstance(ret_expr, nodes.Call) and is_call_to_known_exception(
                ret_expr,
            ):
                lines_with_exceptions.append(node.lineno)
                continue

            # Return a variable that might hold an exception
            if isinstance(ret_expr, nodes.Name):
                scope_node = node.scope()
                if scope_node and chase_assignments_for_exception(
                    ret_expr,
                    scope_node,
                ):
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
                f'{target_file}:{line_no} returns HTTP exception '
                '(`raise` instead)',
                file=sys.stderr,
            )
    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
