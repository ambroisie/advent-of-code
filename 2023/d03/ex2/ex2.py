#!/usr/bin/env python

import sys
from collections import defaultdict
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class SchematicNumber(NamedTuple):
    value: int
    start: Point

    def neighbours(self) -> Iterator["Point"]:
        # How long is the number
        length = len(str(self.value))

        # Every point to the left
        for dx in range(-1, 1 + 1):
            yield Point(self.start.x + dx, self.start.y - 1)

        # Every point below/above
        for dy in range(length):
            for dx in (-1, 1):
                yield Point(self.start.x + dx, self.start.y + dy)

        # Every point to the right
        for dx in range(-1, 1 + 1):
            yield Point(self.start.x + dx, self.start.y + length)


SymbolsMap = dict[Point, str]


def parse_line(x: int, line: str) -> tuple[set[SchematicNumber], SymbolsMap]:
    numbers: set[SchematicNumber] = set()
    symbols: SymbolsMap = {}

    y = 0
    while y != len(line):
        char = line[y]
        pos = Point(x, y)
        if char.isdigit():
            dy = 0
            while (y + dy) < len(line) and (line[y + dy]).isdigit():
                dy += 1
            numbers.add(SchematicNumber(value=int(line[y : y + dy]), start=pos))
            y += dy
            continue
        elif char == ".":
            pass
        else:
            symbols[pos] = char
        y += 1

    return numbers, symbols


def parse(input: list[str]) -> tuple[set[SchematicNumber], SymbolsMap]:
    numbers: set[SchematicNumber] = set()
    symbols: SymbolsMap = {}

    for x, line in enumerate(input):
        new_numbers, new_symbols = parse_line(x, line)
        numbers |= new_numbers
        symbols |= new_symbols

    return numbers, symbols


def solve(input: list[str]) -> int:
    numbers, symbols = parse(input)
    gear_adjacency: dict[Point, list[SchematicNumber]] = defaultdict(list)

    for n in numbers:
        for p in n.neighbours():
            if not symbols.get(p) == "*":
                continue
            gear_adjacency[p].append(n)

    gear_power = [
        nums[0].value * nums[1].value
        for nums in gear_adjacency.values()
        if len(nums) == 2
    ]

    return sum(gear_power)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
