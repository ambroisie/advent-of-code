#!/usr/bin/env python

import sys
from typing import List, Optional, cast


def solve(input: List[str]) -> int:
    def find_illegal_char(input: str) -> Optional[int]:
        chunks: List[str] = []
        ends_to_start = {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<",
        }

        for i, c in enumerate(input):
            # Is it a chunk beginning
            if c not in ends_to_start:
                chunks.append(c)
                continue
            # Is it matching the last element on the chunk stack
            current = chunks.pop()
            # If not, corruption has been found
            if ends_to_start[c] != current:
                return i

        return None

    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    return sum(
        score[line[cast(int, find_illegal_char(line))]]
        for line in input
        if find_illegal_char(line) is not None
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
