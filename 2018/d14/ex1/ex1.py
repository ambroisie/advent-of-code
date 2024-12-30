#!/usr/bin/env python

import functools
import sys


def solve(input: str) -> int:
    n_recipes = int(input)

    scores = [3, 7]
    elves = [0, 1]

    while (len(scores) - 10) < n_recipes:
        sum = scores[elves[0]] + scores[elves[1]]
        scores.extend(map(int, str(sum)))
        elves = [(elf + 1 + scores[elf]) % len(scores) for elf in elves]

    return functools.reduce(lambda lhs, rhs: lhs * 10 + rhs, scores[-10:])


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
