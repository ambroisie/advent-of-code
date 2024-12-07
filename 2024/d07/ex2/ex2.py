#!/usr/bin/env python

import operator
import sys


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[tuple[int, list[int]]]:
        return [
            (int(value), [int(n) for n in numbers.split()])
            for value, numbers in map(lambda l: l.split(": "), input)
        ]

    def solvable(target: int, numbers: list[int]) -> bool:
        def concat(lhs: int, rhs: int) -> int:
            return int(str(lhs) + str(rhs))

        def helper(current_value: int, current_index: int) -> bool:
            next_index = current_index + 1
            if len(numbers) == next_index:
                return target == current_value
            if current_value > target:
                return False
            for op in (operator.add, operator.mul, concat):
                if helper(op(current_value, numbers[next_index]), next_index):
                    return True
            return False

        return helper(numbers[0], 0)

    equations = parse(input.splitlines())
    return sum(value for value, numbers in equations if solvable(value, numbers))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
