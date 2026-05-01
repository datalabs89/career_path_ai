"""Simple calculator with a safe expression evaluator and REPL.

Usage:
  python calculator.py            # starts interactive REPL
  python calculator.py "2+2*3"   # evaluates expression and prints result

This evaluator only permits basic arithmetic and selected math functions.
"""

from __future__ import annotations
import ast
import operator as op
import math
import sys
from typing import Any

# Supported binary operators
_BINARY_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Whitelisted math functions
_ALLOWED_NAMES = {name: getattr(math, name) for name in (
    "sqrt",
    "sin",
    "cos",
    "tan",
    "log",
    "log10",
    "pow",
    "floor",
    "ceil",
    "fabs",
    "factorial",
    "degrees",
    "radians",
    "exp",
)}
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
})


class EvalVisitor(ast.NodeVisitor):
    def visit(self, node: ast.AST) -> Any:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in _BINARY_OPERATORS:
            try:
                return _BINARY_OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ValueError("Division by zero")
        raise ValueError(f"Unsupported binary operator: {op_type}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    def visit_Call(self, node: ast.Call) -> Any:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = _ALLOWED_NAMES[func_name]
        args = [self.visit(a) for a in node.args]
        return func(*args)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    # For Python <3.8 compatibility
    def visit_Num(self, node: ast.Num) -> Any:  # type: ignore[override]
        return node.n


def evaluate(expr: str) -> float:
    """Safely evaluate a mathematical expression and return a number."""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid expression") from e
    visitor = EvalVisitor()
    return visitor.visit(tree)


def repl() -> None:
    print("Calculator REPL — type 'exit' or 'quit' to leave. 'help' for tips.")
    while True:
        try:
            text = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text.lower() in ("exit", "quit"):
            break
        if text.lower() == "help":
            print("Enter any arithmetic expression, e.g. 2+3*4, or use math functions like sqrt(2).")
            continue
        try:
            result = evaluate(text)
            print(result)
        except Exception as e:
            print("Error:", e)


def main() -> None:
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(evaluate(expr))
        except Exception as e:
            print("Error:", e)
            sys.exit(1)
    else:
        repl()


if __name__ == "__main__":
    main()