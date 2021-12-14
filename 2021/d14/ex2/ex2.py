#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from copy import deepcopy
from typing import Dict, Iterator, List, NamedTuple, Tuple, TypeVar


class Template(NamedTuple):
    bigrams: Counter[str]
    counts: Counter[str]


Rules = Dict[str, str]

T = TypeVar("T")


def nth(iterable: Iterator[T], n: int) -> T:
    return next(itertools.islice(iterable, n, None))


def solve(input: List[str]) -> int:
    def parse() -> Tuple[Template, Rules]:
        bigrams = Counter(a + b for a, b in zip(input[0], input[0][1:]))
        counts = Counter(input[0])
        rules = {
            pair: insertion
            for pair, insertion in map(lambda s: s.split(" -> "), input[2:])
        }
        return Template(bigrams, counts), rules

    def step(template: Template, rules: Rules) -> Template:
        bigrams: Counter[str] = Counter()
        counts = deepcopy(template.counts)
        for p, n in template.bigrams.items():
            if p in rules:
                insertion = rules[p]
                bigrams[p[0] + insertion] += n
                bigrams[insertion + p[1]] += n
                counts[insertion] += n
            else:
                # Counts are not changed in this case
                bigrams[p] = n
        return Template(bigrams, counts)

    def polymerize(template: Template, rules: Rules) -> Iterator[Template]:
        while True:
            yield (template := step(template, rules))

    def score(template: Template) -> int:
        nums = [n for __, n in template.counts.most_common()]
        return nums[0] - nums[-1]

    template, rules = parse()
    return score(nth(polymerize(template, rules), 40 - 1))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
