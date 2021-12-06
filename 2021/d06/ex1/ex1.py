#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Iterator, List, TypeVar

T = TypeVar("T")


def nth(iterable: Iterator[T], n: int) -> T:
    return next(itertools.islice(iterable, n, None))


def solve(input: List[str]) -> int:
    fish = [0] * 9
    for n, count in Counter(map(int, input[0].split(","))).items():
        fish[n] = count

    def step(fish: List[int]) -> List[int]:
        # Count how many clones happen
        new_fish = fish[0]

        # Do the next cycle
        fish[0:-1] = fish[1:]
        fish[6] += new_fish
        fish[8] = new_fish  # Override number of new fish

        return fish

    def iter(fish: List[int]) -> Iterator[List[int]]:
        while True:
            yield (fish := step(fish))

    return sum(nth(iter(fish), 80 - 1))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
