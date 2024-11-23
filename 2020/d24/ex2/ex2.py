#!/usr/bin/env python

import itertools
import sys
from collections import defaultdict
from typing import Dict, Iterator, List, Tuple

Offset = Tuple[int, int]
Grid = Dict[Offset, bool]

DELTAS = {
    "nw": (0, -1),
    "ne": (1, -1),
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
}


def to_offset(path: str) -> Offset:
    offset = 0, 0
    i = 0
    while i < len(path):
        direction = path[i]
        i += 1
        if direction in ["s", "n"]:
            direction += path[i]
            i += 1
        x, y = offset
        dx, dy = DELTAS[direction]
        offset = x + dx, y + dy
    return offset


def neighbours(tile: Offset) -> Iterator[Offset]:
    x, y = tile
    for dx, dy in DELTAS.values():
        yield x + dx, y + dy


def step(blacks: Grid) -> Grid:
    to_visit = set(itertools.chain.from_iterable(neighbours(tile) for tile in blacks))
    to_visit |= {tile for tile in blacks}
    res: Grid = defaultdict(bool)

    for tile in to_visit:
        num_neighbours = sum(blacks[n] for n in neighbours(tile))
        if blacks[tile]:
            res[tile] = num_neighbours in (1, 2)
        else:
            res[tile] = num_neighbours == 2

    return res


def solve(raw: List[str]) -> int:
    blacks: Grid = defaultdict(bool)

    for offset in map(to_offset, raw):
        blacks[offset] = not blacks[offset]

    for __ in range(100):
        blacks = step(blacks)

    return sum(blacks.values())


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
