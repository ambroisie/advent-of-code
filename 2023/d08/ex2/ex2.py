#!/usr/bin/env python

import itertools
import math
import sys

Graph = dict[str, list[str]]


def solve(input: list[str]) -> int:
    def parse_graph(input: list[str]) -> Graph:
        res: Graph = {}

        for line in input:
            start, dests = line.split(" = ")
            res[start] = dests[1:-1].split(", ")

        return res

    def parse(input: list[str]) -> tuple[str, Graph]:
        return input[0], parse_graph(input[2:])

    def navigate(directions: str, graph: Graph, start: str) -> int:
        pos = start
        i = 0
        for dir in itertools.cycle(directions):
            if pos[-1] == "Z":
                break
            pos = graph[pos][0 if dir == "L" else 1]
            i += 1
        return i

    directions, graph = parse(input)
    starts = set(node for node in graph if node[-1] == "A")
    steps = {navigate(directions, graph, n) for n in starts}
    return math.lcm(*steps)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
