#!/usr/bin/env python

import collections
import itertools
import sys
from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def sliding_window(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def solve(input: str) -> int:
    def is_nice(input: str) -> bool:
        if not any(
            ab in rest
            for ab, rest in (
                (input[i : i + 2], input[i + 2 :]) for i in range(len(input) - 1)
            )
        ):
            return False
        if not any(a == c for a, _, c in sliding_window(input, 3)):
            return False
        return True

    return sum(map(is_nice, input.splitlines()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
