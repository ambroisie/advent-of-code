#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Tree(NamedTuple):
    children: list["Tree"]
    metadata: list[int]

    @classmethod
    def from_raw(cls, raw: list[int]) -> "Tree":
        def helper(offset: int) -> tuple[Tree, int]:
            n_children, n_metadata = raw[offset], raw[offset + 1]
            offset += 2

            children: list[Tree] = []
            for _ in range(n_children):
                tree, offset = helper(offset)
                children.append(tree)
            metadata = raw[offset : offset + n_metadata]
            offset += n_metadata

            return cls(children, metadata), offset

        tree, offset = helper(0)
        assert offset == len(raw)
        return tree

    def preorder(self) -> Iterator["Tree"]:
        yield self
        for child in self.children:
            yield from child.preorder()


def solve(input: str) -> int:
    def parse(input: str) -> Tree:
        raw = [int(n) for n in input.split()]
        return Tree.from_raw(raw)

    tree = parse(input)
    return sum(itertools.chain.from_iterable(node.metadata for node in tree.preorder()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
