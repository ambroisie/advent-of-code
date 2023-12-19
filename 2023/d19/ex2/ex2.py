#!/usr/bin/env python

import math
import sys
from collections.abc import Iterator
from enum import StrEnum
from typing import NamedTuple, Optional


class Attribute(StrEnum):
    COOL = "x"
    MUSIC = "m"
    AERODYNAMIC = "a"
    SHINY = "s"


Extant = tuple[int, int]
Extants = dict[Attribute, Extant]


class Rule(NamedTuple):
    attr: Attribute
    cmp: str
    n: int
    success: str
    failure: str

    def apply(self, extants: Extants) -> Iterator[tuple[str, Extants]]:
        min, max = extants[self.attr]
        win: Optional[Extant] = None
        lose: Optional[Extant] = None
        match self.cmp:
            case "<":
                if min < self.n:
                    win = min, self.n - 1
                if self.n <= max:
                    lose = self.n, max
            case ">":
                if min <= self.n:
                    lose = min, self.n
                if self.n < max:
                    win = self.n + 1, max
        for attr, extant in (
            (self.success, win),
            (self.failure, lose),
        ):
            if extant is None:
                continue
            yield attr, extants | {self.attr: extant}


Workflow = dict[str, Rule]


def solve(input: str) -> int:
    def parse_rules(rules: list[str]) -> Workflow:
        def parse_line(line: str) -> Workflow:
            name, rules = line.split("{")
            rules = rules[:-1]  # Remove trailing '}'
            # I translate one rule into a succession of pass/fail transitions
            res: Workflow = {}
            raw = rules.split(",")

            for i, rule in enumerate(raw[:-1]):
                test, success = rule.split(":")
                attr = Attribute(test[0])
                cmp = test[1]
                n = int(test[2:])
                failure = raw[-1] if (i == len(raw) - 2) else f"{name}_{i + 1}"
                rule_name = name if i == 0 else f"{name}_{i}"
                res[rule_name] = Rule(attr, cmp, n, success, failure)

            return res

        return {
            name: rule for line in map(parse_line, rules) for name, rule in line.items()
        }

    def explore_workflow(rules: Workflow) -> int:
        def recurse(state: str, extants: Extants) -> int:
            if state == "R":
                return 0
            if state == "A":
                return math.prod((max - min + 1) for min, max in extants.values())
            return sum(
                recurse(new_state, new_extant)
                for new_state, new_extant in rules[state].apply(extants)
            )

        return recurse("in", {attr: (1, 4000) for attr in Attribute})

    paragraphs = input.split("\n\n")
    rules = parse_rules(paragraphs[0].splitlines())
    return explore_workflow(rules)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
