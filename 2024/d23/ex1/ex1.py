#!/usr/bin/env python

import sys
from collections import defaultdict


def solve(input: str) -> int:
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

    def find_three_groups(graph: dict[str, set[str]]) -> set[tuple[str, str, str]]:
        res: set[tuple[str, str, str]] = set()
        for node in graph:
            for neighbour in graph[node]:
                for third in graph[node] & graph[neighbour]:
                    res.add(tuple(sorted((node, neighbour, third))))  # type: ignore
        return res

    topology = parse(input.splitlines())
    graph = links_to_graph(topology)
    groups = find_three_groups(graph)
    return sum(any(computer.startswith("t") for computer in group) for group in groups)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
