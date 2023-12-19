#!/usr/bin/env python

import sys
from enum import StrEnum
from typing import NamedTuple


class Attribute(StrEnum):
    COOL = "x"
    MUSIC = "m"
    AERODYNAMIC = "a"
    SHINY = "s"


Part = dict[Attribute, int]


class Rule(NamedTuple):
    attr: Attribute
    cmp: str
    n: int
    success: str
    failure: str

    def apply(self, part: Part) -> str:
        COMP = {
            "<": lambda x: x < self.n,
            ">": lambda x: x > self.n,
        }
        if COMP[self.cmp](part[self.attr]):
            return self.success
        return self.failure


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

    def parse_parts(parts: list[str]) -> list[Part]:
        def parse_part(line: str) -> Part:
            line = line[1:-1]  # Remove braces
            values = {
                Attribute(name): int(n)
                for name, n in map(lambda x: x.split("="), line.split(","))
            }
            return values

        return [parse_part(line) for line in parts]

    def apply_workflow(part: Part, rules: Workflow) -> bool:
        state = "in"
        while state not in ("R", "A"):
            state = rules[state].apply(part)
        return state == "A"

    paragraphs = input.split("\n\n")
    rules = parse_rules(paragraphs[0].splitlines())
    parts = parse_parts(paragraphs[1].splitlines())
    return sum(sum(part.values()) for part in parts if apply_workflow(part, rules))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
