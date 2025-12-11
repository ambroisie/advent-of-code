#!/usr/bin/env python

import functools
import itertools
import math
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
            return sum(rec(n, end) for n in graph.get(start, []))

        # Input is assured to be a DAG, so a simple recursive count is enough
        return rec(start, end)

    graph = parse(input)
    return sum(
        math.prod(count_paths(graph, a, b) for a, b in itertools.pairwise(path))
        for path in (
            ["svr", "dac", "fft", "out"],
            ["svr", "fft", "dac", "out"],
        )
    )


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
