#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    digits = [int(n) for n in input.strip()]

    scores = [3, 7]
    elves = [0, 1]

    while scores[-len(digits) :] != digits and scores[-len(digits) - 1 : -1] != digits:
        sum = scores[elves[0]] + scores[elves[1]]
        scores.extend(map(int, str(sum)))
        elves = [(elf + 1 + scores[elf]) % len(scores) for elf in elves]

    left_of_digits = len(scores) - len(digits) - (scores[-len(digits) :] != digits)
    return left_of_digits


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
