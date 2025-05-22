#!/usr/bin/env python

import itertools
import math
import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(n) for n in input.splitlines()]

    def package_groups(packages: list[int]) -> tuple[list[int], list[int], list[int]]:
        assert sum(packages) % 3 == 0  # Sanity check
        target_weight = sum(packages) // 3

        # I'm lazy, a brute-force double loop is good enough
        for first_len in range(1, len(packages) + 1):
            for perm in itertools.combinations(range(len(packages)), first_len):
                first = [packages[p] for p in perm]
                if sum(first) != target_weight:
                    continue
                others = [p for i, p in enumerate(packages) if i not in perm]
                for sec_len in range(1, len(others) + 1):
                    for perm in itertools.combinations(range(len(others)), sec_len):
                        second = [others[p] for p in perm]
                        if sum(second) != target_weight:
                            continue
                        last = [p for i, p in enumerate(others) if i not in perm]
                        return first, second, last
        assert False  # Sanity check

    def quantum_entanglement(packages: list[int]) -> int:
        return math.prod(packages)

    packages = parse(input)
    best_split = package_groups(packages)
    return quantum_entanglement(best_split[0])


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
