#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from typing import Dict, Iterator, List, Tuple, TypeVar

Rules = Dict[str, str]

T = TypeVar("T")


def nth(iterable: Iterator[T], n: int) -> T:
    return next(itertools.islice(iterable, n, None))


def solve(input: List[str]) -> int:
    def parse() -> Tuple[str, Rules]:
        template = input[0]
        rules = {
            pair: insertion
            for pair, insertion in map(lambda s: s.split(" -> "), input[2:])
        }
        return template, rules

    def step(template: str, rules: Rules) -> str:
        res: List[str] = []

        # Look at all pairs
        for a, b in zip(template, template[1:]):
            res.append(a)
            if (a + b) in rules:
                res.append(rules[a + b])

        # Add the last element
        res.append(template[-1])
        return "".join(res)

    def polymerize(template: str, rules: Rules) -> Iterator[str]:
        while True:
            yield (template := step(template, rules))

    def score(template: str) -> int:
        counts = [n for __, n in Counter(template).most_common()]
        return counts[0] - counts[-1]

    template, rules = parse()
    return score(nth(polymerize(template, rules), 10 - 1))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
