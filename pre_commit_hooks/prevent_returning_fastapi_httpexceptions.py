from __future__ import annotations

# TODO(patrick): this detrects ast.Call of exception type,
# what if it's an already instantiated var?
import argparse
import ast
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


class HTTPExceptionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.http_exception_returns: list[int] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._process_function(node)

    def visit_AsyncFunctionDef(  # noqa: N802
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        self._process_function(node)

    def _process_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        for stmt in ast.walk(node):
            if (
                isinstance(stmt, ast.Return)
                and isinstance(
                    stmt.value,
                    ast.Call,
                )
                and getattr(stmt.value.func, 'id', None)
                in [
                    'AFKException',
                    'HTTPException',
                    'WebSocketException',
                ]
            ):
                self.http_exception_returns.append(stmt.lineno)


def find_http_exception_returns(file_path: str) -> list[int]:
    with Path(file_path).open(encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=file_path)
    visitor = HTTPExceptionVisitor()
    visitor.visit(tree)
    return visitor.http_exception_returns


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    ret_val = 0
    for target_file in args.filenames:
        http_exception_returns = find_http_exception_returns(target_file)
        for line_no in http_exception_returns:
            ret_val = 1
            print(
                f'{target_file}:{line_no} returns HTTP exception, '
                '(`raise` instead)',
                file=sys.stderr,
            )
    return ret_val


if __name__ == '__main__':
    raise SystemExit(main())
