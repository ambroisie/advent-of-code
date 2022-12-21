#!/usr/bin/env python

import dataclasses
import enum
import operator
import sys
from typing import Optional, Union

Num = Union[int, "MathObserver"]


class Operator(str, enum.Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

    def __call__(self, lhs: Num, rhs: Num) -> Num:
        OPERATIONS = {
            self.ADD: operator.add,
            self.SUB: operator.sub,
            self.MUL: operator.mul,
            self.DIV: operator.floordiv,
        }
        return OPERATIONS[self](lhs, rhs)

    def reverse(self, lhs: Num, rhs: Num) -> Num:
        OPERATIONS = {
            self.ADD: Operator.SUB,
            self.SUB: Operator.ADD,
            self.MUL: Operator.DIV,
            self.DIV: Operator.MUL,
        }
        return OPERATIONS[self](lhs, rhs)


@dataclasses.dataclass
class MathObserver:
    _operations: list[tuple[Operator, int, bool]] = dataclasses.field(
        default_factory=list
    )
    _target: Optional[int] = dataclasses.field(default=None, init=False)

    def __add__(self, rhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.ADD, rhs, False)])

    def __radd__(self, lhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.ADD, lhs, False)])

    def __mul__(self, rhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.MUL, rhs, False)])

    def __rmul__(self, lhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.MUL, lhs, False)])

    def __sub__(self, rhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.SUB, rhs, False)])

    def __rsub__(self, lhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.SUB, lhs, True)])

    def __floordiv__(self, rhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.DIV, rhs, False)])

    def __rfloordiv__(self, lhs: int) -> "MathObserver":
        return MathObserver(self._operations + [(Operator.DIV, lhs, True)])

    def __eq__(self, rhs: object) -> bool:
        return self._record_eq(rhs)

    def __req__(self, lhs: object) -> bool:
        return self._record_eq(lhs)

    def _record_eq(self, value: object) -> bool:
        # Sanity checks
        assert isinstance(value, int)
        assert self._target is None
        self._target = value
        return True

    def resolve(self) -> int:
        assert self._target is not None  # Sanity check
        target: int = self._target

        for op, n, is_assymetric_rhs in reversed(self._operations):
            if is_assymetric_rhs:
                target = op(n, target)  # type: ignore
            else:
                target = op.reverse(target, n)  # type: ignore

        return target


class Monkey:
    def get_value(self, monkeys: dict[str, "Monkey"]) -> Num:
        raise NotImplemented


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
    _value: Optional[Num] = dataclasses.field(default=None, init=False)

    def get_value(self, monkeys: dict[str, "Monkey"]) -> Num:
        if self._value is None:
            self._value = self.op(
                monkeys[self.lhs].get_value(monkeys),
                monkeys[self.rhs].get_value(monkeys),
            )
        return self._value


class Human(Monkey):
    def get_value(self, monkeys: dict[str, "Monkey"]) -> MathObserver:
        return MathObserver()


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

    monkeys["humn"] = Human()

    root = monkeys["root"]
    assert isinstance(root, MathMonkey)  # Sanity check

    lhs, rhs = monkeys[root.lhs], monkeys[root.rhs]
    assert lhs.get_value(monkeys) == rhs.get_value(monkeys)

    for monkey in (lhs, rhs):
        value = monkey.get_value(monkeys)
        if not isinstance(value, MathObserver):
            continue
        return value.resolve()
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
