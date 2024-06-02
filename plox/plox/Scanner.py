from typing import Any
from plox.Token import Token, TokenType, Keywords


class Scanner:
    def __init__(self, src: str):
        self.src = src
        self.start: int = 0
        self.current: int = 0
        self.line: int = 0
        self.tokens: list[Token] = []

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd:
            self._scanToken()
            self.start = self.current
        self.add_token(TokenType.EOF)
        return self.tokens

    def _scanToken(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                self.add_token(TokenType.SLASH)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            # Whitespace/Comments
            case "#":
                while self.peek() != "\n" and not self.isAtEnd:
                    self.advance()
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.parse_str()
            case digit if digit.isdigit():
                self.parse_number()
            case ident if ident.isalpha() or ident == "_":
                self.parse_ident()

            case _:
                raise ValueError(f"Could not match {c} to a Token!")

    def add_token(self, type_: TokenType, literal: Any = None):
        self.tokens.append(
            Token(type_, self.src[self.start : self.current], literal, self.line)
        )

    @property
    def isAtEnd(self):
        return self.current >= len(self.src)

    def match(self, c: str) -> bool:
        if self.isAtEnd:
            return False
        if self.src[self.current] != c:
            return False
        self.current = +1
        return True

    def peek(self) -> str:
        if self.isAtEnd:
            return "\0"
        return self.src[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.src):
            return "\0"
        return self.src[self.current + 1]

    def advance(self) -> str:
        idx = self.current
        self.current = idx + 1
        return self.src[idx]

    def parse_str(self):
        while self.peek() != '"' and not self.isAtEnd:
            if self.advance() == "\n":
                self.line += 1
        if self.isAtEnd:
            ValueError(f"{self.line}:: Unterminated String.")

        self.advance()  # Grab closing quote
        string = self.src[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, string)

    def parse_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.src[self.start : self.current]))

    def parse_ident(self):
        while self.peek().isalnum():
            self.advance()
        ident = self.src[self.start : self.current]
        type = Keywords.get(ident, TokenType.IDENT)
        self.add_token(type)
