#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> str:
    def curve_step(input: str) -> str:
        b = input.translate(str.maketrans("01", "10"))[::-1]
        return input + "0" + b

    def checksum(state: str) -> str:
        while len(state) % 2 == 0:
            state = "".join(str(int(a == b)) for a, b in itertools.batched(state, 2))
        return state

    state = input.strip()
    disk_size = 35651584
    while len(state) < disk_size:
        state = curve_step(state)
    return checksum(state[:disk_size])


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
