#!/usr/bin/env python

import sys
from dataclasses import dataclass
from typing import List, Tuple

Instruction = Tuple[str, int]
Position = Tuple[int, int]


@dataclass
class Ship:
    pos: Position
    rel_waypoint: Position


ORIENTATIONS = ["N", "W", "S", "E"]
MOVES = {
    "N": (1, 0),
    "W": (0, -1),
    "S": (-1, 0),
    "E": (0, 1),
}


def move_ship(pos: Ship, instr: Instruction) -> Ship:
    if instr[0] == "L":
        assert instr[1] % 90 == 0
        turns = instr[1] // 90
        x, y = pos.rel_waypoint
        for __ in range(turns):
            x, y = y, -x
        return Ship(pos.pos, (x, y))
    elif instr[0] == "R":
        assert instr[1] % 90 == 0
        turns = instr[1] // 90
        x, y = pos.rel_waypoint
        for __ in range(turns):
            x, y = -y, x
        return Ship(pos.pos, (x, y))
    elif instr[0] == "F":
        dx, dy = pos.rel_waypoint
        x, y = pos.pos
        x += dx * instr[1]
        y += dy * instr[1]
        return Ship((x, y), pos.rel_waypoint)
    else:
        dx, dy = MOVES[instr[0]]
        x, y = pos.rel_waypoint
        x += dx * instr[1]
        y += dy * instr[1]
        return Ship(pos.pos, (x, y))


def solve(raw: List[str]) -> int:
    instructions = [(i[0], int(i[1:])) for i in raw]
    ship = Ship((0, 0), (1, 10))
    for i in instructions:
        ship = move_ship(ship, i)
    return sum(abs(c) for c in ship.pos)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
