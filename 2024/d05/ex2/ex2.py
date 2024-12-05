#!/usr/bin/env python

import collections
import copy
import functools
import sys

Graph = dict[int, set[int]]


def solve(input: str) -> int:
    def parse_ordering(input: str) -> Graph:
        graph: Graph = collections.defaultdict(set)
        for l in input.splitlines():
            lhs, rhs = map(int, l.split("|"))
            graph[lhs].add(rhs)
        return graph

    def parse_updates(input: str) -> list[list[int]]:
        return [[int(n) for n in line.split(",")] for line in input.splitlines()]

    def parse(input: str) -> tuple[Graph, list[list[int]]]:
        ordering, updates = input.split("\n\n")
        return parse_ordering(ordering), parse_updates(updates)

    def validate_update(ordering: Graph, update: list[int]) -> tuple[int, int] | None:
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                lhs, rhs = update[i], update[j]
                if lhs in ordering[rhs]:
                    return i, j
        return None

    def get_middle(update: list[int]) -> int:
        assert len(update) % 2 == 1  # Sanity check
        return update[len(update) // 2]

    def fix_update(ordering: Graph, update: list[int]) -> list[int]:
        # The graph has cycles, so using a topological sort is out
        # Instead just swap the wrong pages until we fixed the update
        update = copy.copy(update)
        while (indices := validate_update(ordering, update)) is not None:
            lhs, rhs = indices
            update[lhs], update[rhs] = update[rhs], update[lhs]
        return update

    ordering, updates = parse(input)
    invalid_updates = filter(functools.partial(validate_update, ordering), updates)
    fixed_updates = map(functools.partial(fix_update, ordering), invalid_updates)

    return sum(get_middle(update) for update in fixed_updates)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
