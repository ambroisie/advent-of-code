#!/usr/bin/env python

import sys
from typing import NamedTuple


class ProgramYell(NamedTuple):
    weight: int
    children: set[str]


Tower = dict[str, ProgramYell]


def solve(input: str) -> str:
    def parse_line(line: str) -> tuple[str, ProgramYell]:
        name, rest = line.split(" ", 1)
        weight, rest = rest.split(")")
        children = set(rest.removeprefix(" -> ").split(", ")) if rest else set()
        return name, ProgramYell(int(weight[1:]), children)

    def parse(input: str) -> Tower:
        return {name: yell for name, yell in map(parse_line, input.splitlines())}

    def find_base(tower: Tower) -> str:
        candidates = set(tower.keys())
        for yell in tower.values():
            candidates -= yell.children
        assert len(candidates) == 1
        return candidates.pop()

    tower = parse(input)
    return find_base(tower)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
