#!/usr/bin/env python

import ast
import sys


def solve(input: str) -> int:
    strings = input.splitlines()
    # It's too easy to use the built-in parser not to do it...
    return sum(len(raw) - len(ast.literal_eval(raw)) for raw in strings)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
