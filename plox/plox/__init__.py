from enum import IntEnum

from plox.Token import Token, TokenType


class ReturnValue(IntEnum):
    Ok = 0
    UsageError = 1
    ParsingError = 10
    RuntimeError = 20


errors: list[str] = []


def add_error_from_token(t: Token, msg: str):
    if t.type_ == TokenType.EOF:
        add_error(t.line, f"at EOF {msg}")
    add_error(t.line, f"at '{t.lexeme}' {msg}")


def add_error(line: int, msg: str):
    errors.append(f"[l: {line}] Error: {msg}")
