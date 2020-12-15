#!/usr/bin/env python
import itertools
import sys
from collections import defaultdict
from typing import Dict, Iterator, List


def nth(iterable: Iterator[int], n: int) -> int:
    return next(itertools.islice(iterable, n, None))


def spoken(spoken: List[int]) -> Iterator[int]:
    turn = 0
    turns: Dict[int, List[int]] = defaultdict(list)
    for last in spoken:
        turn += 1
        turns[last].append(turn)
        yield last
    while True:
        if len(last_turn := turns[last]) < 2:
            last = 0
        else:
            last = last_turn[-1] - last_turn[-2]
        turn += 1
        turns[last].append(turn)
        yield last


def solve(nums: List[int]) -> int:
    return nth(spoken(nums), 2020 - 1)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    assert len(input) == 1
    print(solve([int(i) for i in input[0].split(",")]))


if __name__ == "__main__":
    main()
