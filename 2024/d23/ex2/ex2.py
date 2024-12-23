#!/usr/bin/env python

import sys
from collections import defaultdict
from collections.abc import Iterator


def solve(input: str) -> str:
    def parse_line(input: str) -> tuple[str, str]:
        lhs, rhs = input.split("-")
        return lhs, rhs

    def parse(input: list[str]) -> list[tuple[str, str]]:
        return [parse_line(line) for line in input]

    def links_to_graph(topology: list[tuple[str, str]]) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = defaultdict(set)
        for lhs, rhs in topology:
            graph[lhs].add(rhs)
            graph[rhs].add(lhs)
        return graph

    # Maximum clique solution thanks to [1]
    # [1]: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def bron_kerbosch(graph: dict[str, set[str]]) -> Iterator[set[str]]:
        def helper(
            clique: set[str],
            candidates: set[str],
            discarded: set[str],
        ) -> Iterator[set[str]]:
            if not candidates and not discarded:
                yield clique
            while candidates:
                v = candidates.pop()
                yield from helper(
                    clique | {v},
                    candidates & graph[v],
                    discarded & graph[v],
                )
                discarded.add(v)

        return helper(set(), set(graph.keys()), set())

    topology = parse(input.splitlines())
    graph = links_to_graph(topology)
    cliques = bron_kerbosch(graph)
    historian_group = max(cliques, key=len)  # MyPy doesn't like it inline in `sorted`
    return ",".join(sorted(historian_group))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
