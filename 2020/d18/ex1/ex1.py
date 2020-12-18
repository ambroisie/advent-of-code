#!/usr/bin/env python

import sys
from typing import Callable, Dict, List

"""
E : G [ (+|*) G ]*

G : '(' E ')' | CONSTANT
"""


def parse_g(expr: List[str]) -> int:
    top = expr.pop(0)
    if top == "(":
        ans = parse_e(expr)
        assert expr.pop(0) == ")"
        return ans
    return int(top)


def parse_e(expr: List[str]) -> int:
    ops: Dict[str, Callable[[int, int], int]] = {
        "*": lambda lhs, rhs: lhs * rhs,
        "+": lambda lhs, rhs: lhs + rhs,
    }
    lhs = parse_g(expr)
    while len(expr) and expr[0] in ["+", "*"]:
        op = expr.pop(0)
        rhs = parse_g(expr)
        lhs = ops[op](lhs, rhs)
    return lhs


def parse_infix(input: List[str]) -> int:
    """
    Parses the given string in infix notation.
    """
    ans = parse_e(input)
    assert len(input) == 0
    return ans


def tokenize(expr: str) -> List[str]:
    res = []

    def split_tok(tok: str) -> None:
        if "(" not in tok and ")" not in tok:
            res.append(tok)
        if "(" in tok:
            res.append("(")
            split_tok(tok[1:])
        if ")" in tok:
            split_tok(tok[:-1])
            res.append(")")

    for tok in expr.split():
        split_tok(tok)
    return res


def solve(raw: List[str]) -> int:
    return sum(parse_infix(tokenize(expr)) for expr in raw)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
