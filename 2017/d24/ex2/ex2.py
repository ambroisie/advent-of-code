#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
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


class Bridge(NamedTuple):
    components: tuple[Component, ...]
    head: int

    @property
    def length(self):
        return len(self.components)

    @property
    def strength(self):
        return sum(itertools.chain.from_iterable(self.components))

    def add(self, c: Component) -> "Bridge":
        assert self.head in c  # Sanity check
        return Bridge(self.components + (c,), c.remaining_port(self.head))


def solve(input: str) -> int:
    def parse(input: str) -> list[Component]:
        return [Component.from_str(line) for line in input.splitlines()]

    def longest_bridge(components: set[Component]) -> Bridge:
        def build_bridges(
            bridge: Bridge, components: set[Component]
        ) -> Iterator[Bridge]:
            candidates = {c for c in components if bridge.head in c}
            if not candidates:
                yield bridge
                return
            for c in candidates:
                yield from build_bridges(bridge.add(c), components - {c})

        return max(
            build_bridges(Bridge((), 0), components),
            key=lambda b: (b.length, b.strength),
        )

    components = parse(input)
    assert len(set(components)) == len(components)  # Sanity check
    bridge = longest_bridge(set(components))
    return bridge.strength


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
