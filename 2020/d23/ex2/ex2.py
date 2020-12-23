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
        return next * links[next]

    current = circle[0]
    circle += [i + 1 for i in range(max(circle), 1000000)]
    links = to_links(circle)

    for __ in range(10000000):
        current = step(links, current)

    return to_answer(links)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    assert len(input) == 1
    print(solve([int(c) for c in input[0]]))


if __name__ == "__main__":
    main()
