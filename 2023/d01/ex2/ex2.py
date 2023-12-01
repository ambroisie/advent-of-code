#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def extract_digits(line: str) -> list[int]:
        # Just do a search and replace to simplify our  lives
        digits = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        # The solution expects "sevenine" to translate to 79, so keep first/last character
        # as a work-around.
        for word, value in digits.items():
            line = line.replace(word, word[0] + str(value) + word[-1])
        return [int(c) for c in line if c.isdigit()]

    def value(line: str) -> int:
        digits = extract_digits(line)
        return digits[0] * 10 + digits[-1]

    return sum(value(line) for line in input)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
