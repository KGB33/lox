import plox
from plox.Token import Token, TokenType
from plox.Expr import Binary, Expr, Grouping, Unary, Literal


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current: int = 0
        self.tokens = tokens

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except ParseError as e:
            print(e)
            return None

    def expression(self) -> Expr:
        """
        expression  → equality ;
        """
        return self.equality()

    def equality(self) -> Expr:
        """
        equality    → comparison ( ( "!=" | "==" ) comparison )* ;
        """
        expr = self.comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        """
        comparison  → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        """
        expr = self.term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        """
        term        → factor ( ( "-" | "+" ) factor )* ;
        """
        expr = self.factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        """
        factor      → unary ( ( "/" | "*" ) unary )* ;
        """
        expr = self.unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        """
        unary       → ( "!" | "-" ) unary | primary ;
        """
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        """
        primary     → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
        """
        t = self._advance()
        match t.type_:
            case TokenType.FALSE:
                return Literal(False)
            case TokenType.TRUE:
                return Literal(True)
            case TokenType.NIL:
                return Literal(None)
            case TokenType.NUMBER | TokenType.STRING:
                return Literal(self._previous().literal)
            case TokenType.LEFT_PAREN:
                expr = self.expression()
                _ = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(expr)
            case _:
                raise self._error(t, f"Unable to match {t} into a primary expression.")

    def synchronize(self):
        """
        When a ParseError is thrown, discard tokens untill a statement boundry is found.
        """
        _ = self._advance()
        while not self.isAtEnd:
            if self._previous().type_ == TokenType.SEMICOLON:
                return
            match self._peek().type_:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
                case _:
                    _ = self._advance()

    def _match(self, *args: TokenType) -> bool:
        for t in args:
            if self._check(t):
                _ = self._advance()
                return True
        return False

    def _check(self, t: TokenType) -> bool:
        if self.isAtEnd:
            return False
        return self._peek().type_ == t

    def _advance(self) -> Token:
        if not self.isAtEnd:
            self.current += 1
        return self._previous()

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _consume(self, to_token: TokenType, error_msg: str):
        if self._check(to_token):
            return self._advance()

        raise self._error(self._peek(), error_msg)

    def _error(self, t: Token, msg: str):
        plox.add_error_from_token(t, msg)
        return ParseError(msg)

    @property
    def isAtEnd(self) -> bool:
        return self.current >= len(self.tokens)
