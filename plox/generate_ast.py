import sys
from pathlib import Path
import subprocess

from textwrap import dedent


def main(out_dir: Path, base_name: str, types: list[tuple[str, list[str]]]):
    file_name = out_dir / f"{base_name}.py"
    code = dedent(f"""\
        from abc import ABC
        from dataclasses import dataclass

        from plox.Token import Token

        class {base_name}(ABC):
            pass
        """)
    for name, fields in types:
        code = code + dedent(f"""
            @dataclass
            class {name}({base_name}):
                {f"\n{' '*16}".join(f for f in fields)}
        """)
    with open(file_name, "w") as f:
        _ = f.write(code)


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
            check_git()
            main(
                Path(dir),
                "Expr",
                [
                    ("Binary", ["left: Expr", "operator: Token", "right: Expr"]),
                    ("Grouping", ["expression: Expr "]),
                    ("Literal", ["value: Any"]),
                    ("Unary", ["operator: Token", "right: Expr"]),
                ],
            )
        case _:
            print("Usage: generate_ast.py <output_dir>")
            sys.exit(1)

    _ = subprocess.run(["ruff", "format"], check=True)
