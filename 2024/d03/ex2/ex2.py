#!/usr/bin/env python

import dataclasses
import re
import sys


@dataclasses.dataclass
class MulInstruction:
    lhs: int
    rhs: int

    def calc(self) -> int:
        return self.lhs * self.rhs


def solve(input: str) -> int:
    def parse(input: str) -> list[MulInstruction]:
        res: list[MulInstruction] = []

        MUL_REGEX = re.compile(r"do\(\)|don't\(\)|mul\((\d+),(\d+)\)")
        do = True
        for match in MUL_REGEX.finditer(input):
            if match.group(0) in ("do()", "don't()"):
                do = match.group(0) == "do()"
                continue
            if not do:
                continue
            res.append(MulInstruction(int(match.group(1)), int(match.group(2))))

        return res

    return sum(inst.calc() for inst in parse(input))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
