import sys
from enum import IntEnum

from plox.Scanner import Scanner


class ReturnValue(IntEnum):
    Ok = 0
    UsageError = 1
    ParsingError = 10
    RuntimeError = 20


errors: list[str] = []


def runRepl():
    while True:
        if line := input(">>> "):
            _run(line)


def runFile(file: str):
    with open(file) as f:
        src = f.read()
    _run(src)


def _run(src: str):
    for t in Scanner(src).scanTokens():
        print(t)


def addError(line: int, msg: str):
    errors.append(f"[l: {line}] Error: {msg}")


if __name__ == "__main__":
    match sys.argv[1:]:  # argv[0] is program name.
        case []:
            runRepl()
        case [f]:
            runFile(f)
        case _:
            print("Usage: `plox [script]`")
