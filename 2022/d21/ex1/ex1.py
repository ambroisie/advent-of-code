#!/usr/bin/env python

import dataclasses
import enum
import operator
import sys
from typing import Optional


class Operator(str, enum.Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

    def __call__(self, lhs: int, rhs: int) -> int:
        OPERATIONS = {
            self.ADD: operator.add,
            self.SUB: operator.sub,
            self.MUL: operator.mul,
            self.DIV: operator.floordiv,
        }
        return OPERATIONS[self](lhs, rhs)


class Monkey:
    def get_value(self, monkeys: dict[str, "Monkey"]) -> int:
        raise NotImplementedError


@dataclasses.dataclass
class YellerMonkey(Monkey):
    value: int

    def get_value(self, monkeys: dict[str, "Monkey"]) -> int:
        return self.value


@dataclasses.dataclass
class MathMonkey(Monkey):
    lhs: str
    op: Operator
    rhs: str
    _value: Optional[int] = dataclasses.field(default=None, init=False)

    def get_value(self, monkeys: dict[str, "Monkey"]) -> int:
        if self._value is None:
            self._value = self.op(
                monkeys[self.lhs].get_value(monkeys),
                monkeys[self.rhs].get_value(monkeys),
            )
        return self._value


def solve(input: list[str]) -> int:
    def parse_monkey(input: str) -> tuple[str, Monkey]:
        name, value = input.split(": ")

        monkey: Monkey
        match value.split():
            case [lhs, op, rhs]:
                monkey = MathMonkey(lhs, Operator(op), rhs)
            case [n]:
                monkey = YellerMonkey(int(n))
            case _:
                assert False  # Sanity check

        return name, monkey

    monkeys = dict(map(parse_monkey, input))
    return monkeys["root"].get_value(monkeys)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
