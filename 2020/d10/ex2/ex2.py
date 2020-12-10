#!/usr/bin/env python

import sys
from typing import Dict, List


def make_chain(adapters: List[int]) -> int:
    adapters += [0, max(adapters) + 3]
    adapters = sorted(adapters)
    jolts: Dict[int, int] = {}
    N = len(adapters)

    def rec(index: int) -> int:
        if (res := jolts.get(index)) is not None:
            return res
        if index == N - 1:
            return 1
        total = sum(
            rec(i)
            for i in range(index + 1, min(N, index + 4))
            if (adapters[i] - adapters[index]) <= 3
        )
        jolts[index] = total
        return total

    return rec(0)


def solve(raw: List[str]) -> int:
    return make_chain([int(line) for line in raw])


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
