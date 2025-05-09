#!/usr/bin/env python

import sys
from collections import Counter
from typing import NamedTuple


class ProgramYell(NamedTuple):
    weight: int
    children: set[str]


Tower = dict[str, ProgramYell]


def solve(input: str) -> int:
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

    def compute_weights(tower: Tower, base: str) -> dict[str, int]:
        def helper(base: str) -> int:
            total = (
                sum(helper(child) for child in tower[base].children)
                + tower[base].weight
            )
            res[base] = total
            return total

        res: dict[str, int] = {}
        helper(base)
        return res

    def fix_balance(tower: Tower) -> int:
        base = find_base(tower)
        weights = compute_weights(tower, base)

        balanced_weight = -1  # Will be updated to the correct value afterwards
        while True:
            children = tower[base].children
            subtowers = Counter(weights[child] for child in children)
            if len(subtowers) == 1:
                assert balanced_weight != -1  # Sanity check
                return balanced_weight - sum(weights[child] for child in children)
            assert len(subtowers) == 2  # Sanity check
            balanced_weight, unbalanced_weight = (v for v, _ in subtowers.most_common())
            base = next(
                child for child in children if weights[child] == unbalanced_weight
            )

    tower = parse(input)
    return fix_balance(tower)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
