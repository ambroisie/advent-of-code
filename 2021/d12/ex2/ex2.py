#!/usr/bin/env python

import itertools
import sys
from collections import defaultdict
from typing import Dict, List, Set

Map = Dict[str, Set[str]]


def solve(input: List[str]) -> int:
    def parse() -> Map:
        res: Map = defaultdict(set)

        for start, to in map(lambda s: s.split("-"), input):
            res[start].add(to)
            res[to].add(start)

        return res

    caves = parse()

    def dfs(start: str, seen: Set[str] = set(), has_doubled_back: bool = False) -> int:
        if start == "end":
            return 1

        seen = seen | {start}
        res = 0

        for dest in caves[start]:
            doubles_back = False
            if dest in seen and dest.islower():
                if has_doubled_back or dest == "start":
                    continue
                doubles_back = True
            res += dfs(dest, seen, has_doubled_back or doubles_back)

        return res

    return dfs("start")


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
