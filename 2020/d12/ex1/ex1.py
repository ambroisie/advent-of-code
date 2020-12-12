#!/usr/bin/env python

import sys
from typing import List, Tuple

Positiom = Tuple[str, int, int]
Instruction = Tuple[str, int]

ORIENTATIONS = ["N", "W", "S", "E"]
MOVES = {
    "N": (1, 0),
    "W": (0, -1),
    "S": (-1, 0),
    "E": (0, 1),
}


def move_ship(pos: Positiom, instr: Instruction) -> Positiom:
    if instr[0] == "L":
        assert instr[1] % 90 == 0  # Sanity check
        delt = instr[1] // 90
        orientation = ORIENTATIONS[
            (ORIENTATIONS.index(pos[0]) + delt) % len(ORIENTATIONS)
        ]
        return (orientation, *pos[1:])
    elif instr[0] == "R":
        assert instr[1] % 90 == 0  # Sanity check
        delt = instr[1] // 90
        orientation = ORIENTATIONS[ORIENTATIONS.index(pos[0]) - delt]
        return (orientation, *pos[1:])
    else:
        dx, dy = MOVES[pos[0] if instr[0] == "F" else instr[0]]
        x, y = pos[1], pos[2]
        x += dx * instr[1]
        y += dy * instr[1]
        return (pos[0], x, y)


def solve(raw: List[str]) -> int:
    instructions = [(i[0], int(i[1:])) for i in raw]
    ship = ("E", 0, 0)
    for i in instructions:
        ship = move_ship(ship, i)
    return abs(ship[1]) + abs(ship[2])


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
