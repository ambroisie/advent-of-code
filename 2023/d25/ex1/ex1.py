#!/usr/bin/env python

import copy
import random
import sys
from collections import Counter, defaultdict
from typing import cast

Graph = dict[str, Counter[str]]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> Graph:
        res: Graph = defaultdict(Counter)

        for line in input:
            node, destinations = line.split(": ")
            for dest in destinations.split():
                res[node][dest] = 1
                res[dest][node] = 1

        return res

    def contract_edge(graph: Graph, s: str, t: str) -> None:
        assert s != t  # Sanity check
        assert s in graph  # Sanity check
        assert t in graph  # Sanity check

        # Merge the edges
        graph[s] += graph[t]
        # Don't count the potential t-s edge
        del graph[s][s]
        # Remove t from the graph
        for other in graph[t].keys():
            del graph[other][t]
        del graph[t]
        # Update the neighbours values
        for other, v in graph[s].items():
            graph[other][s] = v

    # Stoer-Wagner algorithm
    def min_cut_exact(graph: Graph) -> tuple[set[str], set[str]]:
        def phase(graph: Graph) -> tuple[str, str, int]:
            assert len(graph) >= 2  # Sanity check

            candidates = set(graph.keys())
            start = candidates.pop()
            found = [start]
            cut_weight: list[int] = []

            while candidates:
                (weight, node) = max(
                    (sum(graph[node][other] for other in found), node)
                    for node in candidates
                )
                candidates.discard(node)
                found.append(node)
                cut_weight.append(weight)

            return found[-2], found[-1], cut_weight[-1]

        partition: set[str] = set()
        g = copy.deepcopy(graph)

        # Initialize our best weight/parition
        best_weight = cast(int, float("inf"))
        best_partition = set(partition)

        while len(g) > 1:
            s, t, w = phase(g)
            partition.add(t)
            contract_edge(g, s, t)
            if w < best_weight:
                best_weight = w
                best_partition = set(partition)

        return best_partition, graph.keys() - best_partition

    def min_cut_karger(graph: Graph, target: int) -> tuple[set[str], set[str]]:
        assert len(graph) >= 2  # Sanity check

        original_edges = [
            (source, dest)
            for source, destinations in graph.items()
            for dest in destinations
            if source < dest
        ]

        while True:
            g = copy.deepcopy(graph)
            contracted = {v: v for v in graph}
            while len(g) > 2:
                s, t = (contracted[v] for v in random.choice(original_edges))
                if s == t:
                    continue
                contract_edge(g, s, t)
                # Hacky union-find-ish algorithm, for laziness
                for k, v in contracted.items():
                    if v != t:
                        continue
                    contracted[k] = s
            # Pick a partition at random here
            node = next(iter(g))
            # Check that we met our target
            if g[node].total() > target:
                continue
            partition = {n for n, parent in contracted.items() if parent == node}
            return partition, graph.keys() - partition

    graph = parse(input)
    # The exact algorithm is very slow on big graphs, at which point Karger's algorithm is better
    if len(graph) < 100:
        left, right = min_cut_exact(graph)
    else:
        left, right = min_cut_karger(graph, 3)
    return len(left) * len(right)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
