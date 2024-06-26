import sys

from plox import errors
from plox.Scanner import Scanner
from plox.Parser import Parser
from plox.Ast import AstPrinter


def runRepl():
    while True:
        if line := input(">>> "):
            _run(line)


def runFile(file: str):
    with open(file) as f:
        src = f.read()
    _run(src)


def _run(src: str):
    tokens = Scanner(src).scanTokens()
    print(f"Tokens parsed: {tokens}")
    expressions = Parser(tokens).parse()

    if errors:
        return print(errors)
    if expressions is not None:
        return print(AstPrinter().display(expressions))
    print("Somehow, there were no errors, and no expressions were parsed.")


if __name__ == "__main__":
    match sys.argv[1:]:  # argv[0] is program name.
        case []:
            runRepl()
        case [f]:
            runFile(f)
        case _:
            print("Usage: `plox [script]`")
    for e in errors:
        print(e)
