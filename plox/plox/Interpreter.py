import sys
from plox.Exceptions import PloxRuntimeError
from plox.Expr import Binary, Expr, Grouping, Literal, Unary
from plox.Token import Token, TokenType


class Interpreter:
    def interpret(self, expr: Expr):
        try:
            print(self._evaluate(expr))
        except* PloxRuntimeError as excs:
            for e in excs.exceptions:
                print(e, file=sys.stderr)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)
        operator = expr.operator
        match operator.type_:
            case TokenType.MINUS:
                self._check_operands(operator, "__neg__", right)
                return -(right)  # type: ignore
            case TokenType.BANG:
                return not bool(right)
            case _:
                print(
                    f"{sys._getframe(  ).f_code.co_name} called with {expr.operator.type_=} but cannot handle that type. {expr=}",
                    file=sys.stderr,
                )

    def visit_binary_expr(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        operator = expr.operator
        match operator.type_:
            case TokenType.PLUS:
                self._check_operands(operator, "__add__", right, left)
                return left + right  # type: ignore
            case TokenType.MINUS:
                self._check_operands(operator, "__sub__", right, left)
                return left - right  # type: ignore
            case TokenType.SLASH:
                self._check_operands(operator, "__add__", right, left)
                return left / right  # type: ignore
            case TokenType.STAR:
                self._check_operands(operator, "__mul__", right, left)
                return left * right  # type: ignore
            case TokenType.GREATER:
                self._check_operands(operator, "__gt__", right, left)
                return left > right  # type: ignore
            case TokenType.GREATER_EQUAL:
                self._check_operands(operator, "__ge__", right, left)
                return left >= right  # type: ignore
            case TokenType.LESS:
                self._check_operands(operator, "__lt__", right, left)
                return left < right  # type: ignore
            case TokenType.LESS_EQUAL:
                self._check_operands(operator, "__le__", right, left)
                return left <= right  # type: ignore
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            case _:
                print(
                    f"{sys._getframe(  ).f_code.co_name} called with {expr.operator.type_=} but cannot handle that type. {expr=}",
                    file=sys.stderr,
                )

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def _check_operands(
        self,
        operator: Token,
        dunder: str,
        *operands: object,
    ):
        excs = []
        for operand in operands:
            if hasattr(operand, dunder):
                return
            excs.append(PloxRuntimeError(operator, operand, dunder))
        raise ExceptionGroup(f"Bad operand(s) for {operator}", excs)
