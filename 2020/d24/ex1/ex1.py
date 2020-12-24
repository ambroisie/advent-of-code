#!/usr/bin/env python

import sys
from collections import defaultdict
from typing import Dict, List, Tuple

Offset = Tuple[int, int]

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


def solve(raw: List[str]) -> int:
    blacks: Dict[Offset, bool] = defaultdict(bool)

    for offset in map(to_offset, raw):
        blacks[offset] = not blacks[offset]

    return sum(blacks.values())


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
