import pytest

from plox.Interpreter import Interpreter
from plox.Scanner import Scanner
from plox.Parser import Parser


@pytest.mark.parametrize(
    "stmt,expected",
    [
        ("!True", False),
        ("!False", True),
        ("!!True", True),
        ("!!!False", True),
        ("-10", -10),
    ],
)
def test_basic_unary_expressions(stmt, expected):
    tokens = Scanner(stmt).scanTokens()
    print(f"{tokens=}")
    expressions = Parser(tokens).parse()
    print(f"{expressions=}")
    assert expressions is not None
    result = Interpreter()._evaluate(expressions)

    assert result == expected
