#!/usr/bin/env python

import sys
from collections import defaultdict
from typing import Dict, List


def make_chain(adapters: List[int]) -> int:
    adapters = sorted(adapters)
    output = 0
    device = adapters[-1] + 3
    jolts: Dict[int, int] = defaultdict(int)
    for adapter in adapters:
        delt = adapter - output
        jolts[delt] += 1
        output = adapter
    jolts[device - output] += 1

    return jolts[1] * jolts[3]


def solve(raw: List[str]) -> int:
    return make_chain([int(line) for line in raw])


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
