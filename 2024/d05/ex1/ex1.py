#!/usr/bin/env python

import collections
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

    def validate_update(ordering: Graph, update: list[int]) -> bool:
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                lhs, rhs = update[i], update[j]
                if lhs in ordering[rhs]:
                    return False
        return True

    def get_middle(update: list[int]) -> int:
        assert len(update) % 2 == 1  # Sanity check
        return update[len(update) // 2]

    ordering, updates = parse(input)
    return sum(
        get_middle(update) for update in updates if validate_update(ordering, update)
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
