#!/usr/bin/env python

import sys
from typing import Callable, Dict, List

"""
E : T [ * T ]*

T : G [ + G ]*

G : '(' E ')' | CONSTANT
"""


def parse_g(expr: List[str]) -> int:
    top = expr.pop(0)
    if top == "(":
        ans = parse_e(expr)
        assert expr.pop(0) == ")"
        return ans
    return int(top)


def parse_t(expr: List[str]) -> int:
    lhs = parse_g(expr)
    while len(expr) and expr[0] == "+":
        expr.pop(0)
        rhs = parse_g(expr)
        lhs += rhs
    return lhs


def parse_e(expr: List[str]) -> int:
    lhs = parse_t(expr)
    while len(expr) and expr[0] == "*":
        expr.pop(0)
        rhs = parse_t(expr)
        lhs *= rhs
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
