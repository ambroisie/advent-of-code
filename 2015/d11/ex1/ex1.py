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


def solve(input: str) -> str:
    def parse(input: str) -> int:
        res = 0
        for c in input.strip():
            res = res * 26 + ord(c) - ord("a")
        return res

    def unparse(n: int) -> str:
        # Passwords *must* have 8 characters
        assert 0 <= n < 26**8  # Sanity check
        return "".join(chr(ord("a") + (n // 26**i) % 26) for i in range(8))[::-1]

    def has_straight(password: str) -> bool:
        for a, b, c in sliding_window(password, 3):
            if ord(a) + 1 == ord(b) and ord(b) + 1 == ord(c):
                return True
        return False

    def no_iol(password: str) -> bool:
        return not any(c in password for c in "iol")

    def has_couples(password: str) -> bool:
        for i, (a, b) in enumerate(itertools.pairwise(password)):
            if a != b:
                continue
            for c, d in itertools.pairwise(password[i + 2 :]):
                if c == d:
                    return True
            return False
        return False

    n = parse(input)
    while True:
        n = (n + 1) % 26**8  # Restrict password to 8 characters
        password = unparse(n)
        if not has_straight(password):
            continue
        if not no_iol(password):
            continue
        if not has_couples(password):
            continue
        return password


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
