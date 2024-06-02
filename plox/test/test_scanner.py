from plox.Token import Token, TokenType
from plox.Scanner import Scanner


def test_scanner_parses_variable_ident():
    src = "var foo = 10.0"
    expected = [
        Token(TokenType.VAR, "var", None, 0),
        Token(TokenType.IDENT, "foo", None, 0),
        Token(TokenType.EQUAL, "=", None, 0),
        Token(TokenType.NUMBER, "10.0", 10.0, 0),
        Token(TokenType.EOF, "", None, 0),
    ]
    actual = Scanner(src).scanTokens()
    assert expected == actual


def test_scanner_parses_strings():
    src = """ "Some single-line String"\n"And\nnow\na Multiline\nString" """
    expected = [
        Token(
            TokenType.STRING, '"Some single-line String"', "Some single-line String", 0
        ),
        Token(
            TokenType.STRING,
            '"And\nnow\na Multiline\nString"',
            "And\nnow\na Multiline\nString",
            4,
        ),
        Token(TokenType.EOF, "", None, 4),
    ]
    actual = Scanner(src).scanTokens()
    assert expected == actual
