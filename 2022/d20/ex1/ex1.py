#!/usr/bin/env python

import sys
from collections import deque


def solve(input: list[int]) -> int:
    def mix(file: list[int]) -> list[int]:
        shuffled = deque(enumerate(file))

        for i, n in enumerate(file):
            item = shuffled.index((i, n))
            shuffled.remove((i, n))
            # Moving the item to the left means moving the collection to the left
            shuffled.rotate(-n)
            shuffled.insert(item, (i, n))

        return [n for _, n in shuffled]

    def coordinates(file: list[int]) -> tuple[int, int, int]:
        zero_index = file.index(0)
        indices = map(lambda n: n + zero_index, [1000, 2000, 3000])
        return tuple(map(lambda n: file[n % len(file)], indices))  # type: ignore

    return sum(coordinates(mix(input)))


def main() -> None:
    input = [int(n) for n in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
