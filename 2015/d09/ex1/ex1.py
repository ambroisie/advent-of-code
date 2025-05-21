#!/usr/bin/env python

import collections
import itertools
import sys


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[str, str, int]:
        p1, _, p2, _, dist = input.split()
        return p1, p2, int(dist)

    def parse(input: str) -> dict[str, dict[str, int]]:
        res: dict[str, dict[str, int]] = collections.defaultdict(dict)
        for p1, p2, dist in map(parse_line, input.splitlines()):
            res[p1][p2] = dist
            res[p2][p1] = dist
        return res

    # Boring Traveling Salesman solution
    distances = parse(input)
    return min(
        sum(distances[s][e] for s, e in itertools.pairwise(travel_plan))
        for travel_plan in itertools.permutations(distances.keys())
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
