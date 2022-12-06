#!/usr/bin/env python

import collections
import itertools
import sys
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def sliding_window(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def solve(input: str) -> int:
    SIZE = 14
    for i, tup in enumerate(sliding_window(input, SIZE), start=SIZE):
        if len(set(tup)) == SIZE:
            return i
    assert False


def main() -> None:
    input = sys.stdin.read().replace("\n", "")
    print(solve(input))


if __name__ == "__main__":
    main()
