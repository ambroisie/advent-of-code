#!/usr/bin/env python

import functools
import sys
from typing import NamedTuple


class Component(NamedTuple):
    left: int
    right: int

    @classmethod
    def from_str(cls, input: str) -> "Component":
        return cls(*map(int, input.split("/")))

    def remaining_port(self, connection: int) -> int:
        if connection == self.left:
            return self.right
        elif connection == self.right:
            return self.left
        assert False  # Sanity check


def solve(input: str) -> int:
    def parse(input: str) -> list[Component]:
        return [Component.from_str(line) for line in input.splitlines()]

    @functools.cache
    def strongest_bridge(start: int, components: frozenset[Component]) -> int:
        candidates = {c for c in components if start in c}
        if not candidates:
            return 0
        return max(
            sum(c) + strongest_bridge(c.remaining_port(start), components - {c})
            for c in candidates
        )

    components = parse(input)
    assert len(set(components)) == len(components)  # Sanity check
    return strongest_bridge(0, frozenset(components))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
