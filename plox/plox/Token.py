from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    # Single Char tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One OR Two Char tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENT = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    FALSE = auto()
    TRUE = auto()
    AND = auto()
    OR = auto()
    CLASS = auto()
    FUN = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    NIL = auto()
    RETURN = auto()
    PRINT = auto()
    SUPER = auto()
    THIS = auto()
    VAR = auto()
    EOF = auto()


@dataclass
class Token:
    type_: TokenType
    lexeme: str
    literal: object
    line: int


Keywords = {
    "add": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}
