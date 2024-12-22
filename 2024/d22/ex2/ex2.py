#!/usr/bin/env python

import functools
import itertools
import operator
import sys
from collections import Counter, deque
from collections.abc import Iterator

Sequence = tuple[int, int, int, int]


def solve(input: str) -> int:
    def monkey_hash(seed: int) -> int:
        MASK = (1 << 24) - 1
        seed ^= seed << 6
        seed &= MASK

        seed ^= seed >> 5
        seed &= MASK

        seed ^= seed << 11
        seed &= MASK

        return seed

    def list_prices(seed: int) -> list[int]:
        prices: list[int] = [seed % 10]
        for _ in range(2000):
            seed = monkey_hash(seed)
            prices.append(seed % 10)
        return prices

    def find_sequences(prices: list[int]) -> Counter[Sequence]:
        # Adapted from an `itertools` recipe
        def sliding_window() -> Iterator[tuple[int, ...]]:
            iterator = iter(prices)
            window = deque(itertools.islice(iterator, 5 - 1), maxlen=5)
            for x in iterator:
                window.append(x)
                yield tuple(window)

        assert len(prices) == 2001  # Sanity check
        sequences: Counter[Sequence] = Counter()
        for i, (a, b, c, d, e) in enumerate(sliding_window(), start=4):
            sequences.setdefault((b - a, c - b, d - c, e - d), prices[i])
        return sequences

    seeds = [int(n) for n in input.splitlines()]
    prices = [list_prices(seed) for seed in seeds]
    sequences = functools.reduce(operator.add, map(find_sequences, prices))
    return max(sequences.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
