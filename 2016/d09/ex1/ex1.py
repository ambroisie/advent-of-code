#!/usr/bin/env python

import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def decompress(input: str) -> str:
        def helper() -> Iterator[str]:
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
                    yield input[j + 1 : j + length + 1] * repeat
                    i = j + length + 1
                else:
                    yield input[i:j]
                    i = j
                is_marker = not is_marker

        return "".join(helper())

    decompressed = decompress(input.strip())
    return sum(not c.isspace() for c in decompressed)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
