from plox.Token import Token


class PloxRuntimeError(RuntimeError):
    operator: Token
    operand: object
    dunder: str

    def __str__(self):
        return f"{self.operator=} called with {self.operand=} which does not support {self.dunder=}"
