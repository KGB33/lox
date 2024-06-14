from plox import Expr
from plox.Ast import AstPrinter
from plox.Token import Token, TokenType


def test_ast_printer():
    expr = Expr.Binary(
        Expr.Unary(Token(TokenType.MINUS, "-", None, 1), Expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(Expr.Literal(45.67)),
    )
    expected = "(* (- 123) (group 45.67))"
    assert AstPrinter().display(expr) == expected
