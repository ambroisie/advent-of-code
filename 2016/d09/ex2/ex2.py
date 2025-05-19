#!/usr/bin/env python

import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def decompress(input: str) -> int:
        def helper() -> Iterator[int]:
            i = 0
            is_marker = False
            while i < len(input):
                if is_marker:
                    j = input.find(")", i)
                else:
                    j = input.find("(", i)
                if j == -1:
                    j = len(input)
                if is_marker:
                    length, repeat = map(int, input[i + 1 : j].split("x"))
                    yield decompress(input[j + 1 : j + length + 1]) * repeat
                    i = j + length + 1
                else:
                    yield j - i
                    i = j
                is_marker = not is_marker

        return sum(helper())

    return decompress(input.strip())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
