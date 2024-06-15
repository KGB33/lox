import pytest

from plox.Expr import Binary, Literal, Unary
from plox.Parser import Parser
from plox.Scanner import Scanner
from plox.Token import Token, TokenType


def test_math_expression():
    src = "10 + 15 == 25"
    expected = Binary(
        operator=Token(TokenType.EQUAL_EQUAL, "==", None, 0),
        right=Literal(value=25),
        left=Binary(
            operator=Token(TokenType.PLUS, "+", None, 0),
            right=Literal(value=15),
            left=Literal(value=10),
        ),
    )
    tokens = Scanner(src).scanTokens()
    actual = Parser(tokens).parse()
    assert actual == expected


@pytest.mark.xfail
def test_variable_assignment():
    src = "var foo = 10 + 15"
    expected = Binary(
        operator=Token(TokenType.EQUAL, "=", None, 0),
        right=Binary(
            operator=Token(TokenType.PLUS, "+", None, 0),
            right=Literal(15),
            left=Literal(10),
        ),
        left=Unary(
            operator=Token(TokenType.VAR, "var", None, 0), right=Literal(value="foo")
        ),
    )
    tokens = Scanner(src).scanTokens()
    actual = Parser(tokens).parse()
    assert actual == expected
