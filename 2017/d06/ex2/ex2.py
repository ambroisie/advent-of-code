#!/usr/bin/env python

import itertools
import sys

MemoryBlocks = tuple[int, ...]


def solve(input: str) -> int:
    def parse(input: str) -> MemoryBlocks:
        return tuple(int(n) for n in input.split())

    def redistribute(nums: MemoryBlocks) -> MemoryBlocks:
        res = list(nums)
        i = res.index(max(res))  # Quick and hasty `argmax`
        n, res[i] = res[i], 0
        common, remain = n // len(res), n % len(res)
        for j in range(i + 1, i + remain + 1):
            res[j % len(res)] += 1
        for j in range(len(res)):
            res[j] += common
        return tuple(res)

    blocks = parse(input)
    count: dict[MemoryBlocks, int] = {}
    for i in itertools.count():
        if blocks in count:
            return i - count[blocks]
        count[blocks] = i
        blocks = redistribute(blocks)
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
