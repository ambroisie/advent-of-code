#!/usr/bin/env python

import itertools
import sys
from typing import List, Tuple


def solve(circle: List[int]) -> int:
    def to_links(circle: List[int]) -> List[int]:
        links = [-1 for __ in range(len(circle) + 1)]
        cyclic = itertools.cycle(circle)
        next(cyclic)  # Advance it by one
        for prev, cur in zip(circle, cyclic):
            links[prev] = cur
        return links

    def step(links: List[int], current: int) -> int:
        cup0 = links[current]
        cup1 = links[cup0]
        cup2 = links[cup1]

        links[current] = links[cup2]  # Remove 3-tuple from the linked-list

        # Find destination
        dest = (current - 1) if current > 1 else (len(links) - 1)
        while dest in (cup0, cup1, cup2):
            dest = (dest - 1) if dest > 1 else (len(links) - 1)

        # Update our links
        links[cup2], links[dest] = links[dest], cup0

        return links[current]  # What's the next value in the cycle ?

    def to_answer(links: List[int]) -> int:
        next = links[1]
        res = 0
        while next != 1:
            res = res * 10 + next
            next = links[next]
        return res

    current = circle[0]
    links = to_links(circle)

    for __ in range(100):
        current = step(links, current)

    return to_answer(links)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    assert len(input) == 1
    print(solve([int(c) for c in input[0]]))


if __name__ == "__main__":
    main()
