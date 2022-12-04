#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def is_overlapping(line: str) -> bool:
        def assignment_to_set(elf: str) -> set[int]:
            start, end = elf.split("-")
            return set(range(int(start), int(end) + 1))

        elf1, elf2 = map(assignment_to_set, line.split(","))
        return bool(elf1 & elf2)

    return sum(map(is_overlapping, input))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
