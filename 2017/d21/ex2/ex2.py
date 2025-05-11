#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator

# 2x2 *and* 3x3 grid
Grid = tuple[tuple[bool, ...], ...]
START = ".#./..#/###"


def solve(input: str) -> int:
    def parse_pattern(input: str) -> Grid:
        return tuple(tuple(c == "#" for c in line) for line in input.split("/"))

    def parse(input: str) -> dict[Grid, Grid]:
        return {
            start: end
            for start, end in (
                map(parse_pattern, line.split(" => ")) for line in input.splitlines()
            )
        }

    def permutations(grid: Grid) -> set[Grid]:
        def iter_rotated(grid: Grid) -> Iterator[Grid]:
            for _ in range(4):
                yield grid
                grid = tuple(
                    tuple(grid[len(grid) - y - 1][x] for y in range(len(grid[0])))
                    for x in range(len(grid))
                )

        def iter_flipped(grid: Grid) -> Iterator[Grid]:
            yield grid
            yield grid[::-1]
            yield tuple(line[::-1] for line in grid)

        return {
            flip for rotated in iter_rotated(grid) for flip in iter_flipped(rotated)
        }

    def normalize_rules(raw_rules: dict[Grid, Grid]) -> dict[Grid, Grid]:
        res: dict[Grid, Grid] = {}
        for pattern, grid in raw_rules.items():
            for perm in permutations(pattern):
                res[perm] = grid
        return res

    def enhance(rules: dict[Grid, Grid], rounds: int) -> list[list[bool]]:
        def step(grid: list[list[bool]]) -> list[list[bool]]:
            is_even = len(grid) % 2 == 0
            step_size = 2 if is_even else 3
            next_size = len(grid) * (step_size + 1) // step_size
            res = [[False for _ in range(next_size)] for _ in range(next_size)]

            for x, y in itertools.product(range(len(grid) // step_size), repeat=2):
                elem = tuple(
                    tuple(
                        grid[x * step_size + dx][y * step_size + dy]
                        for dy in range(step_size)
                    )
                    for dx in range(step_size)
                )
                new_grid = rules[elem]
                for dx, line in enumerate(new_grid):
                    for dy, p in enumerate(line):
                        res[x * len(new_grid) + dx][y * len(line) + dy] = p

            return res

        grid = [[p for p in line] for line in parse_pattern(START)]
        for _ in range(rounds):
            grid = step(grid)
        return grid

    raw_rules = parse(input)
    norm_rules = normalize_rules(raw_rules)
    art = enhance(norm_rules, 18)
    return sum(itertools.chain.from_iterable(art))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
