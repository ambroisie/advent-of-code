#!/usr/bin/env python

import collections
import itertools
import sys
from collections.abc import Iterable
from typing import Generic, Hashable, NamedTuple, TypeVar


class Point(NamedTuple):
    x: int
    y: int
    z: int
    t: int


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


# PEP 695 still not supported by MyPy...
T = TypeVar("T", bound=Hashable)


class DisjointSet(Generic[T]):
    _values: list[T]
    _to_index: dict[T, int]
    _sets: UnionFind

    def __init__(self, values: Iterable[T]) -> None:
        self._values = list(values)
        self._to_index = {v: i for i, v in enumerate(self._values)}
        self._sets = UnionFind(len(self._values))

    def find(self, elem: T) -> T:
        return self._values[self._sets.find(self._to_index[elem])]

    def union(self, lhs: T, rhs: T) -> T:
        return self._values[self._sets.union(self._to_index[lhs], self._to_index[rhs])]

    def sets(self) -> dict[T, set[T]]:
        sets = self._sets.sets()
        return {
            self._values[r]: {self._values[i] for i in values}
            for r, values in sets.items()
        }


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(","))) for line in input]

    def dist(lhs: Point, rhs: Point) -> int:
        return sum(abs(l - r) for l, r in zip(lhs, rhs))

    def count_constellations(points: list[Point]) -> int:
        sets = DisjointSet(points)

        for a, b in itertools.combinations(points, 2):
            if dist(a, b) > 3:
                continue
            sets.union(a, b)

        return len(sets.sets())

    points = parse(input.splitlines())
    return count_constellations(points)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
