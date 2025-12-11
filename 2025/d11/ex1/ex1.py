#!/usr/bin/env python

import functools
import sys


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> dict[str, set[str]]:
        return {
            dev: set(outputs.split(" "))
            for dev, outputs in map(lambda s: s.split(": "), input)
        }

    def count_paths(graph: dict[str, set[str]], start: str, end: str) -> int:
        @functools.cache
        def rec(start: str, end: str) -> int:
            if start == end:
                return 1
            return sum(rec(n, end) for n in graph[start])

        # Input is assured to be a DAG, so a simple recursive count is enough
        return rec(start, end)

    graph = parse(input)
    return count_paths(graph, "you", "out")


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
