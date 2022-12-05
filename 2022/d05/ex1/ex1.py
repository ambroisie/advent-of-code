#!/usr/bin/env python

import dataclasses
import sys

Stack = list[str]


@dataclasses.dataclass
class Instruction:
    n: int
    start: int
    end: int

    @classmethod
    def from_input(cls, input: str) -> "Instruction":
        words = input.split()
        return Instruction(int(words[1]), int(words[3]) - 1, int(words[5]) - 1)


def parse(input: list[str]) -> tuple[list[Stack], list[Instruction]]:
    def parse_stacks(input: list[str]) -> list[Stack]:
        stacks: list[Stack] = [[] for _ in range(1, len(input[-1]), 4)]
        for line in reversed(input[:-1]):
            for stack, i in enumerate(range(1, len(line), 4)):
                c = line[i]
                if c == " ":
                    continue
                stacks[stack].append(c)
        return stacks

    def parse_instructions(input: list[str]) -> list[Instruction]:
        return list(map(Instruction.from_input, input))

    empty_line = input.index("")

    return parse_stacks(input[:empty_line]), parse_instructions(input[empty_line + 1 :])


def solve(input: list[str]) -> str:
    stacks, instructions = parse(input)
    for instr in instructions:
        start, end = stacks[instr.start], stacks[instr.end]
        items = (start.pop() for _ in range(instr.n))
        end.extend(items)
    return "".join(stack[-1] for stack in stacks if stack)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
