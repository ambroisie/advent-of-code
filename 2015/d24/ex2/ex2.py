#!/usr/bin/env python

import itertools
import math
import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(n) for n in input.splitlines()]

    def package_groups(
        packages: list[int],
    ) -> Iterator[tuple[list[int], list[int], list[int], list[int]]]:
        assert sum(packages) % 4 == 0  # Sanity check
        target_weight = sum(packages) // 4

        # I'm lazy, a brute-force triple loop is good enough
        found = False
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
                        others_ = [p for i, p in enumerate(others) if i not in perm]
                        for third_len in range(1, len(others_) + 1):
                            for perm in itertools.combinations(
                                range(len(others_)), third_len
                            ):
                                third = [others_[p] for p in perm]
                                last = [
                                    others_[i]
                                    for i in range(len(others_))
                                    if i not in perm
                                ]
                                yield first, second, third, last
                                # We only care to enumerate all valid *first* packages
                                # Not *all* permutations
                                found = True
                                break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        break
                    # *Don't* break if `found`, we want to keep enumerating this length
            if found:
                break

    def quantum_entanglement(packages: list[int]) -> int:
        return math.prod(packages)

    packages = parse(input)
    return min(quantum_entanglement(split[0]) for split in package_groups(packages))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
