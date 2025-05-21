#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def quote_len(raw: str) -> int:
        characters = collections.Counter(raw)
        # The `+ 2` is for the surrounding quotes
        return characters.total() + characters['"'] + characters["\\"] + 2

    strings = input.splitlines()
    return sum(quote_len(raw) - len(raw) for raw in strings)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
