#!/usr/bin/env python

import functools
import itertools
import operator
import sys


def solve(input: str) -> str:
    def parse(input: str) -> list[int]:
        return [ord(c) for c in input.strip()]

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

    lengths = parse(input)
    lengths += [17, 31, 73, 47, 23]  # Additional lengths
    sparse_hash = compute_sparse_hash(lengths)
    dense_hash = compute_dense_hash(sparse_hash)
    return "".join(f"{n:02x}" for n in dense_hash)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
