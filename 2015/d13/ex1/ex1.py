#!/usr/bin/env python

import collections
import itertools
import sys


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[str, str, int]:
        split_input = input.removesuffix(".").split()
        p, other = split_input[0], split_input[-1]
        delta = int(split_input[3]) * (1 if split_input[2] == "gain" else -1)
        return p, other, delta

    def parse(input: str) -> dict[str, dict[str, int]]:
        res: dict[str, dict[str, int]] = collections.defaultdict(dict)
        for p, neighbour, delta in map(parse_line, input.splitlines()):
            res[p][neighbour] = delta
        return res

    def score_seating(deltas: dict[str, dict[str, int]], seating: list[str]) -> int:
        table = itertools.chain(seating, [seating[0]])
        return sum(
            deltas[p1][p2] + deltas[p2][p1] for p1, p2 in itertools.pairwise(table)
        )

    deltas = parse(input)
    return max(
        score_seating(deltas, list(perm))
        for perm in itertools.permutations(deltas.keys())
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
