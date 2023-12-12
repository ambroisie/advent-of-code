#!/usr/bin/env python

import functools
import itertools
import sys

Line = tuple[str, tuple[int, ...]]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Line]:
        return [
            (record, tuple(map(int, groups.split(","))))
            for record, groups in map(str.split, input)
        ]

    def unfold(lines: list[Line]) -> list[Line]:
        return [
            ("?".join(itertools.repeat(record, 5)), groups * 5)
            for record, groups in lines
        ]

    @functools.cache
    def solve_line(record: str, groups: tuple[int, ...]) -> int:
        # Empty string must have no groups left, or it's not a solve
        if len(record) == 0:
            return 1 if len(groups) == 0 else 0
        # Empty groups must not contain any broken spring, or it's not a solve
        if len(groups) == 0:
            return 1 if all(c in (".", "?") for c in record) else 0
        # Skip working springs
        if record[0] == ".":
            return solve_line(record[1:], groups)
        # Try with a '.' (and discard it directly), or a '#' for the unknown springs
        if record[0] == "?":
            return solve_line(record[1:], groups) + solve_line("#" + record[1:], groups)
        # We start with a '#', check that the group is long enough
        if len(record) < groups[0] or any(c == "." for c in record[: groups[0]]):
            return 0
        # And check that we _can_ separate the group from the next one
        if len(record) > groups[0] and record[groups[0]] == "#":
            return 0
        # Now recurse
        return solve_line(record[groups[0] + 1 :], groups[1:])

    lines = parse(input)
    lines = unfold(lines)
    return sum(solve_line(record, groups) for record, groups in lines)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
