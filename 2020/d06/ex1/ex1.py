#!/usr/bin/env python

import sys
from collections import defaultdict
from typing import DefaultDict, List, Set


def solve(raw: List[str]) -> int:
    answers: DefaultDict[int, Set[str]] = defaultdict(set)
    group = 0
    for line in raw:
        if line == "":
            group += 1
            continue
        answers[group] |= {char for char in line}
    return sum(len(answer) for answer in answers.values())


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
