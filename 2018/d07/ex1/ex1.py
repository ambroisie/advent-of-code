#!/usr/bin/env python

import sys
from collections import defaultdict
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> str:
    def parse(input: list[str]) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = defaultdict(set)
        for line in input:
            split = line.split()
            prev, after = split[1], split[7]
            graph[after].add(prev)
            graph[prev]  # Ensure that all nodes are in the dictionary
        return graph

    def topo_sort(graph: dict[str, set[str]]) -> list[str]:
        res: list[str] = []

        queue = {n for n, deps in graph.items() if not deps}
        seen: set[str] = set()

        while queue:
            # We must pop in alphabetical order
            node = min(queue)
            queue.remove(node)

            res.append(node)
            seen.add(node)

            # Iterate over all nodes as we don't have information on children
            for child, deps in graph.items():
                if child in seen:
                    continue
                if deps - seen:
                    continue
                queue.add(child)

        return res

    graph = parse(input.splitlines())
    return "".join(topo_sort(graph))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
