#!/usr/bin/env python

import itertools
import math
import sys
from typing import List, Tuple


def find_first_factor(earliest: int, timings: List[int]) -> Tuple[int, int]:
    timings = sorted(timings)
    for t in itertools.count(earliest):
        for n in timings:
            if t % n == 0:
                return t - earliest, n

    assert False  # Make Mypy happy


def solve(raw: List[str]) -> int:
    return math.prod(
        find_first_factor(int(raw[0]), [int(i) for i in raw[1].split(",") if i != "x"])
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
