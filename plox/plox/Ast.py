from plox.Expr import Expr, Grouping, Unary, Binary, Literal


class AstPrinter:
    def display(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *args: Expr) -> str:
        return f"({name} {' '.join(e.accept(self) for e in args)})"

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
