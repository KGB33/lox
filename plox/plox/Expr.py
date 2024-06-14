from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override, Protocol
from dataclasses import dataclass

from plox.Token import Token


class Expr(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R:
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: object

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)


class Visitor[R](Protocol):
    def visit_binary_expr(self, expr: Binary) -> R: ...
    def visit_grouping_expr(self, expr: Grouping) -> R: ...
    def visit_literal_expr(self, expr: Literal) -> R: ...
    def visit_unary_expr(self, expr: Unary) -> R: ...
