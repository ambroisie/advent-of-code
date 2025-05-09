#!/usr/bin/env python

import functools
import itertools
import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def parse(input: str) -> tuple[int, int]:
        a, b = input.splitlines()
        return int(a.split()[-1]), int(b.split()[-1])

    def generate(seed: int, factor: int) -> int:
        seed *= factor
        return seed % 2147483647

    def judge(a: int, b: int) -> bool:
        mask = (1 << 16) - 1
        return (a & mask) == (b & mask)

    def iter_judgements(seed_a: int, seed_b: int) -> Iterator[bool]:
        generate_a = functools.partial(generate, factor=16807)
        generate_b = functools.partial(generate, factor=48271)

        while True:
            seed_a, seed_b = generate_a(seed_a), generate_b(seed_b)
            yield judge(seed_a, seed_b)

    seed_a, seed_b = parse(input)
    return sum(itertools.islice(iter_judgements(seed_a, seed_b), 40000000))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
