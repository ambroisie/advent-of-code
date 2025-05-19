#!/usr/bin/env python

import collections
import dataclasses
import functools
import itertools
import operator
import sys


@dataclasses.dataclass(frozen=True)
class Input:
    n: int


@dataclasses.dataclass(frozen=True)
class Bot:
    n: int


@dataclasses.dataclass(frozen=True)
class Output:
    n: int


# Each node points to its children, to each of whom it outputs a chip
GraphKey = Input | Bot
GraphVal = Bot | Output
# By convention, a bot should list its outputs in [`low`, `high`] order
Graph = dict[GraphKey, list[GraphVal]]
# Reverse the graph representation for an easier topo_sort (only of the keys)
ReverseGraph = dict[GraphKey, set[GraphKey]]


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[GraphKey, list[GraphVal]]:
        split_input = input.split()
        if split_input[0] == "bot":
            low_n = int(split_input[6])
            low_type: type[GraphVal] = Bot if split_input[5] == "bot" else Output
            high_n = int(split_input[11])
            high_type: type[GraphVal] = Bot if split_input[10] == "bot" else Output
            return Bot(int(split_input[1])), [low_type(low_n), high_type(high_n)]
        return Input(int(split_input[1])), [Bot(int(split_input[-1]))]

    def parse(input: str) -> Graph:
        return {key: val for key, val in map(parse_line, input.splitlines())}

    def run(graph: Graph) -> dict[GraphVal, list[int]]:
        def reverse_graph(graph: Graph) -> ReverseGraph:
            res: ReverseGraph = {n: set() for n in graph}
            for node, children in graph.items():
                for child in children:
                    # We don't care about `Output`s here
                    if isinstance(child, Output):
                        continue
                    res[child].add(node)
            return res

        def topo_sort(graph: ReverseGraph) -> list[GraphKey]:
            res: list[GraphKey] = []

            queue = {n for n, deps in graph.items() if not deps}
            assert all(isinstance(n, Input) for n in queue)  # Sanity check
            seen: set[GraphKey] = set()

            while queue:
                node = queue.pop()

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

        reversed_graph = reverse_graph(graph)
        assert len(reversed_graph) == len(graph)  # Sanity check
        run_order = topo_sort(reversed_graph)
        assert len(run_order) == len(graph)  # Sanity check
        bots_bins: dict[GraphVal, list[int]] = collections.defaultdict(list)
        for node in run_order:
            match node:
                case Input(n):
                    assert len(graph[node]) == 1  # Sanity check
                    bots_bins[graph[node][0]].append(n)
                case Bot(n):
                    assert len(graph[node]) == 2  # Sanity check
                    assert len(bots_bins[node]) == 2  # Sanity check
                    # Have we found the bot we were looking for?
                    for out, val in zip(graph[node], sorted(bots_bins[node])):
                        bots_bins[out].append(val)
        return bots_bins

    graph = parse(input)
    outputs = run(graph)
    return functools.reduce(
        operator.mul,
        itertools.chain.from_iterable(outputs[Output(i)] for i in range(3)),
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
