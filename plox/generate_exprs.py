import sys
from pathlib import Path
import subprocess

from textwrap import dedent


def main(out_dir: Path, base_name: str, types: list[tuple[str, list[str]]]):
    file_name = out_dir / f"{base_name}.py"
    code = dedent(f"""\
        from __future__ import annotations
        from abc import ABC, abstractmethod
        from typing import override, Protocol
        from dataclasses import dataclass

        from plox.Token import Token

        class {base_name}(ABC):
            @abstractmethod
            def accept[R](self, visitor: Visitor[R]) -> R:
                pass
        """)
    for class_name, fields in types:
        code = code + generate_type(base_name, class_name, fields)

    code = code + generate_visitor(base_name, [n for n, _ in types])
    with open(file_name, "w") as f:
        _ = f.write(code)


def generate_type(base_name: str, class_name: str, fields: list[str]) -> str:
    code = "\n"
    code = (
        code
        + dedent(f"""\
        @dataclass
        class {class_name}({base_name}):
    """)
        + "    "
        + f"\n{' '*4}".join(f for f in fields)
        + "\n    @override"
        + "\n    def accept[R](self, visitor: Visitor[R]) -> R:\n"
        + f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)"
    )
    return code


def generate_visitor(base_name: str, types: list[str]) -> str:
    code = dedent("""
        class Visitor[R](Protocol):
        """)
    for t in types:
        code = (
            code
            + f"    def visit_{t.lower()}_{base_name.lower()}(self, {base_name.lower()}: {t}) -> R: ... \n"
        )
    return code


def check_git():
    cmd = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, check=True
    )
    assert (
        len(cmd.stdout) == 0
    ), "Please stash changes before running this potentally destructive command."


if __name__ == "__main__":
    match sys.argv:
        case [_, dir]:
            # check_git()
            main(
                Path(dir),
                "Expr",
                [
                    ("Binary", ["left: Expr", "operator: Token", "right: Expr"]),
                    ("Grouping", ["expression: Expr "]),
                    ("Literal", ["value: object"]),
                    ("Unary", ["operator: Token", "right: Expr"]),
                ],
            )
        case _:
            print("Usage: generate_ast.py <output_dir>")
            sys.exit(1)

    _ = subprocess.run(["ruff", "format"], check=True)
