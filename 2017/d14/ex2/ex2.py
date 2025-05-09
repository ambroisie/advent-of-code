#!/usr/bin/env python

import collections
import functools
import itertools
import operator
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
    def knot_hash(byte_string: str) -> str:
        def compute_sparse_hash(lengths: list[int]) -> list[int]:
            circle = list(range(256))
            cur_pos, skip_size = 0, 0
            for _ in range(64):
                for n in lengths:
                    # Invalid length
                    assert n < len(circle)  # Sanity check
                    # Reverse
                    for i, j in zip(
                        range(cur_pos, cur_pos + n // 2),
                        # Avoid off-by-one by going further than necessary
                        range(cur_pos + n - 1, cur_pos, -1),
                    ):
                        i %= len(circle)
                        j %= len(circle)
                        circle[i], circle[j] = circle[j], circle[i]
                    # Move
                    cur_pos += n + skip_size
                    # Increase
                    skip_size += 1
            return circle

        def compute_dense_hash(sparse_hash: list[int]) -> list[int]:
            assert len(sparse_hash) == 256  # Sanity check
            return [
                functools.reduce(operator.xor, chunk)
                for chunk in itertools.batched(sparse_hash, 16)
            ]

        lengths = [ord(c) for c in byte_string]
        lengths += [17, 31, 73, 47, 23]  # Additional lengths
        sparse_hash = compute_sparse_hash(lengths)
        dense_hash = compute_dense_hash(sparse_hash)
        return "".join(f"{n:02x}" for n in dense_hash)

    def count_regions(hashes: list[int]) -> int:
        def occupied(row: int, bit: int) -> bool:
            return (hashes[row] & 1 << bit) != 0

        def key(row: int, bit: int) -> int:
            return row * 128 + bit

        def unkey(key: int) -> tuple[int, int]:
            return key // 128, key % 128

        uf = UnionFind(128 * 128)
        for i in range(128):
            for bit in range(128):
                if not occupied(i, bit):
                    continue
                for ni, nbit in (
                    (i - 1, bit),
                    (i, bit - 1),
                    (i + 1, bit),
                    (i, bit + 1),
                ):
                    if ni < 0 or ni >= 128:
                        continue
                    if nbit < 0 or nbit >= 128:
                        continue
                    if not occupied(ni, nbit):
                        continue
                    uf.union(key(i, bit), key(ni, nbit))
        # We created a UnionFind over *all* squares, only count *occupied* squares
        return sum(occupied(*unkey(root)) for root in uf.sets())

    input = input.strip()
    hashes = [int(knot_hash(f"{input}-{i}"), 16) for i in range(128)]
    return count_regions(hashes)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
