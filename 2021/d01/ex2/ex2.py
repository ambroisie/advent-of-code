#!/usr/bin/env python

import collections
import itertools
import sys
from typing import List


def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def solve(input: List[int]) -> int:
    windowed = [sum(window) for window in sliding_window(input, 3)]
    return sum(prev < cur for (prev, cur) in zip(windowed, windowed[1:]))


def main() -> None:
    input = [int(line) for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
