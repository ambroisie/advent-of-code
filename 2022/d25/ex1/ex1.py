#!/usr/bin/env python

import sys


def solve(input: list[str]) -> str:
    def from_snafu(input: str) -> int:
        res = 0
        for c in input:
            if c == "=":
                n = -2
            elif c == "-":
                n = -1
            else:
                n = int(c)
            res = res * 5 + n
        return res

    def to_snafu(input: int) -> str:
        # Base case
        if not input:
            return "0"

        DIGITS = {
            2: "2",
            1: "1",
            0: "0",
            -1: "-",
            -2: "=",
        }

        digits: list[int] = []
        while input:
            input, d = divmod(input, 5)
            if d not in DIGITS:
                d -= 5
                input += 1
            digits.append(d)
        return "".join(DIGITS[c] for c in reversed(digits))

    return to_snafu(sum(map(from_snafu, input)))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
