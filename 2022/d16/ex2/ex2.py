#!/usr/bin/env python

import dataclasses
import functools
import sys
from collections import defaultdict


@dataclasses.dataclass
class Valve:
    flow: int
    neighbours: set[str]


Graph = dict[str, Valve]
DistanceMatrix = dict[str, dict[str, int]]

START_ROOM = "AA"


def solve(input: list[str]) -> int:
    def to_graph(input: list[str]) -> Graph:
        res = {}

        for line in input:
            assert line.startswith("Valve ")  # Sanity check

            name = line.split()[1]
            flow = line.split("=")[1].split(";")[0]
            neighbours = line.split(";")[1].replace(", ", " ").split()[4:]

            res[name] = Valve(int(flow), set(neighbours))

        return res

    def useful_valves(g: Graph) -> set[str]:
        return {k for k, v in g.items() if v.flow > 0}

    def floyd_warshall(g: Graph) -> DistanceMatrix:
        points = list(g.keys())

        res: DistanceMatrix = defaultdict(dict)

        for p in points:
            for n in g[p].neighbours:
                res[p][n] = 1

        for p in points:
            for i in points:
                for j in points:
                    if (ip := res[i].get(p)) is None:
                        continue
                    if (pj := res[p].get(j)) is None:
                        continue
                    dist = ip + pj
                    if (ij := res[i].get(j)) is not None:
                        dist = min(dist, ij)
                    res[i][j] = dist

        return res

    def prune_distances(dist: DistanceMatrix, of_interest: set[str]) -> DistanceMatrix:
        # Only keep non-zero valves for our visits
        pruned = {
            i: {j: dist for j, dist in line.items() if j in of_interest}
            for i, line in dist.items()
            if i in of_interest
        }
        # Explicitly add the starting room, in case it was pruned
        pruned[START_ROOM] = {
            n: dist for n, dist in dist[START_ROOM].items() if n in of_interest
        }
        return pruned

    def max_flow(g: Graph, dist: DistanceMatrix) -> int:
        def pressure_per_minute(opened_valves: frozenset[str]) -> int:
            return sum(g[valve].flow for valve in opened_valves)

        @functools.cache
        def helper(
            start: str, time: int, opened_valves: frozenset[str]
        ) -> tuple[int, frozenset[str]]:
            assert time >= 0  # Sanity check
            if time == 0:
                return 0, opened_valves

            pressure = pressure_per_minute(opened_valves)

            # Base-case, don't do anything
            best = pressure * time, opened_valves

            # Try to open the current valve if not done already
            if start not in opened_valves:
                score, valves = helper(start, time - 1, opened_valves | {start})
                score += pressure
                best = max(best, (score, valves))

            # Try to go to each neighbour
            for n, d in dist[start].items():
                if d >= time:
                    continue
                score, valves = helper(n, time - d, opened_valves)
                score += pressure * d
                best = max(best, (score, valves))

            return best

        opened_valves = set()
        # If starting room has no flow, consider it open to reduce search space
        if g[START_ROOM].flow == 0:
            opened_valves.add(START_ROOM)
        score, valves = helper(START_ROOM, 26, frozenset(opened_valves))
        elephant_score, _ = helper(START_ROOM, 26, valves)
        elephant_score -= pressure_per_minute(valves) * 26  # Don't double count
        return score + elephant_score

    graph = to_graph(input)
    dist = prune_distances(floyd_warshall(graph), useful_valves(graph))
    return max_flow(graph, dist)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
