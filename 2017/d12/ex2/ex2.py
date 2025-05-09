#!/usr/bin/env python

import collections
import sys


class UnionFind:
    _parent: list[int]
    _rank: list[int]

    def __init__(self, size: int):
        # Each node is in its own set, making it its own parent...
        self._parent = list(range(size))
        # ... And its rank 0
        self._rank = [0] * size

    def find(self, elem: int) -> int:
        while (parent := self._parent[elem]) != elem:
            # Replace each parent link by a link to the grand-parent
            elem, self._parent[elem] = parent, self._parent[parent]
        return elem

    def union(self, lhs: int, rhs: int) -> int:
        lhs = self.find(lhs)
        rhs = self.find(rhs)
        # Bail out early if they already belong to the same set
        if lhs == rhs:
            return lhs
        # Always keep `lhs` as the taller tree
        if self._rank[lhs] < self._rank[rhs]:
            lhs, rhs = rhs, lhs
        # Merge the smaller tree into the taller one
        self._parent[rhs] = lhs
        # Update the rank when merging trees of approximately the same size
        if self._rank[lhs] == self._rank[rhs]:
            self._rank[lhs] += 1
        return lhs

    def sets(self) -> dict[int, set[int]]:
        res: dict[int, set[int]] = collections.defaultdict(set)
        for elem in range(len(self._parent)):
            res[self.find(elem)].add(elem)
        return dict(res)


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[int, set[int]]:
        origin, others = input.split(" <-> ")
        return int(origin), {int(n) for n in others.split(", ")}

    def parse(input: str) -> dict[int, set[int]]:
        return {n: children for n, children in map(parse_line, input.splitlines())}

    def count_groups(graph: dict[int, set[int]]) -> int:
        uf = UnionFind(len(graph))
        for n, children in graph.items():
            for child in children:
                uf.union(n, child)
        return len(uf.sets())

    graph = parse(input)
    return count_groups(graph)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
