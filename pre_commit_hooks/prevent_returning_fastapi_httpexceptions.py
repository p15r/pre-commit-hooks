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
    """Recursively yield each node in the astroid tree (similar to node.walk() in newer versions)."""
    yield node
    for child in node.get_children():
        yield from walk_astroid_tree(child)


def is_call_to_known_exception(call_node: nodes.Call) -> bool:
    """Check if `call_node` is a Call to any name/attribute in EXCEPTION_NAMES."""
    func = call_node.func
    if isinstance(func, nodes.Name):
        return func.name in EXCEPTION_NAMES
    if isinstance(func, nodes.Attribute):
        return func.attrname in EXCEPTION_NAMES
    return False


def is_variable_instance_of_known_exception(
    name_node: nodes.Name,
    current_scope: nodes.Scope,
) -> bool:
    """Use `lookup` on the current scope to see if `name_node` refers to a variable
    that is an instance of a known exception class.
    """
    # `lookup` returns a tuple: (assign_nodes, inferred_values)
    # - `assign_nodes` are where the name is defined
    # - `inferred_values` are what astroid thinks the name might be
    assignments, inferred_values = current_scope.lookup(name_node.name)
    # print(f'lookup for {name_node.name=}: {assignments=}, {inferred_values=}')

    # If we have no inferred results, bail out
    if not inferred_values:
        return False

    for inferred in inferred_values:
        # Sometimes you'll see astroid.Uninferable
        if inferred is astroid.Uninferable:
            continue
        # If it's directly a class definition named in EXCEPTION_NAMES
        if (
            isinstance(inferred, nodes.ClassDef)
            and inferred.name in EXCEPTION_NAMES
        ):
            return True

        # If it's an instance, check if the proxied class name is known
        if isinstance(inferred, astroid.Instance):
            class_def = inferred._proxied
            if class_def and class_def.name in EXCEPTION_NAMES:
                return True

        if isinstance(inferred, astroid.AssignName):
            print(f'DEBUG: {vars(inferred)=}')

    return False


def find_http_exception_returns(file_path: str) -> list[int]:
    """Parse `file_path` using astroid and return line numbers of Return statements
    that:
      - directly call a known exception (AFKException, HTTPException, etc.), or
      - return a variable that is inferred (via lookup) to be an instance of one.
    """
    code = Path(file_path).read_text(encoding='utf-8')
    module_node = astroid.parse(code, path=file_path)

    lines_with_exceptions = []
    for node in walk_astroid_tree(module_node):
        # Only consider Return nodes
        if isinstance(node, nodes.Return) and node.value is not None:
            ret_expr = node.value

            # --- CASE A: Direct call in the return statement ---
            if isinstance(ret_expr, nodes.Call) and is_call_to_known_exception(
                ret_expr
            ):
                lines_with_exceptions.append(node.lineno)
                continue

            # --- CASE B: Return a variable that might hold an exception ---
            # If it's a Name, we do a scope lookup
            if isinstance(ret_expr, nodes.Name):
                # `node.scope()` finds the nearest astroid scope (function, class, or module)
                scope_node = node.scope()
                if scope_node and is_variable_instance_of_known_exception(
                    ret_expr, scope_node
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
                f'{target_file}:{line_no} returns HTTP exception (`raise` instead)',
                file=sys.stderr,
            )
    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
