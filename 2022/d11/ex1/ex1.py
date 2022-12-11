#!/usr/bin/env python

import dataclasses
import sys
from collections import Counter, deque
from typing import Literal, Optional


@dataclasses.dataclass
class Operation:
    lhs: Optional[int]
    operator: Literal["+", "*"]
    rhs: Optional[int]

    def __call__(self, old: int) -> int:
        lhs = old if self.lhs is None else self.lhs
        rhs = old if self.rhs is None else self.rhs

        if self.operator == "*":
            return lhs * rhs
        if self.operator == "+":
            return lhs + rhs
        assert False

    @classmethod
    def from_input(cls, input: str) -> "Operation":
        assert input.startswith("  Operation: new = ")
        lhs, op, rhs = input.split()[-3:]

        assert op in ("+", "*")  # Sanity check

        return cls(
            None if lhs == "old" else int(lhs),
            op,  # type: ignore
            None if rhs == "old" else int(rhs),
        )


@dataclasses.dataclass
class Monkey:
    items: deque[int]
    operation: Operation
    test_divisor: int
    transfer: dict[bool, int]

    @classmethod
    def from_input(cls, input: list[str]) -> "Monkey":
        # Sanity checks
        assert input[0].startswith("Monkey ")
        assert "divisible by" in input[3]
        assert "true" in input[4]
        assert "false" in input[5]

        items = deque(
            int(n) for n in input[1].removeprefix("  Starting items: ").split(",")
        )
        operation = Operation.from_input(input[2])
        divisor = int(input[3].split()[-1])
        transfer = {
            True: int(input[4].split()[-1]),
            False: int(input[5].split()[-1]),
        }
        return Monkey(items, operation, divisor, transfer)


def solve(input: list[str]) -> int:
    def do_round(monkeys: list[Monkey], counts: dict[int, int]) -> None:
        for i, monkey in enumerate(monkeys):
            counts[i] += len(monkey.items)
            while monkey.items:
                item = monkey.items.popleft()
                item = monkey.operation(item)
                item //= 3
                target = monkey.transfer[(item % monkey.test_divisor) == 0]
                monkeys[target].items.append(item)

    monkeys = [Monkey.from_input(monkey_spec.splitlines()) for monkey_spec in input]
    counts: Counter[int] = Counter()

    for _ in range(20):
        do_round(monkeys, counts)

    ((_, a), (_, b)) = counts.most_common(2)
    return a * b


def main() -> None:
    input = sys.stdin.read().split("\n\n")
    print(solve(input))


if __name__ == "__main__":
    main()
