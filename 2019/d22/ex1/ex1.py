#!/usr/bin/env python

import dataclasses
import enum
import sys


class Technique(enum.Enum):
    DEAL_NEW = enum.auto()
    CUT = enum.auto()
    DEAL_INCR = enum.auto()


@dataclasses.dataclass
class Instruction:
    tech: Technique
    n: int

    def to_linear(self) -> tuple[int, int]:
        if self.tech == Technique.DEAL_NEW:
            return (-1, -1)
        if self.tech == Technique.CUT:
            return (1, -self.n)
        if self.tech == Technique.DEAL_INCR:
            return (self.n, 0)
        assert False  # Sanity check

    def apply(self, card_pos: int, deck_size: int) -> int:
        a, b = self.to_linear()
        return (card_pos * a + b) % deck_size


def solve(input: str) -> int:
    def parse_instruction(input: str) -> Instruction:
        if input == "deal into new stack":
            return Instruction(Technique.DEAL_NEW, 0)
        n = int(input.split()[-1])
        if input.startswith("cut"):
            return Instruction(Technique.CUT, n)
        if input.startswith("deal with increment"):
            return Instruction(Technique.DEAL_INCR, n)
        assert False  # Sanity check

    def parse(input: list[str]) -> list[Instruction]:
        return [parse_instruction(line) for line in input]

    def find_final_pos(
        card_pos: int, deck_size: int, instructions: list[Instruction]
    ) -> int:
        for instr in instructions:
            card_pos = instr.apply(card_pos, deck_size)
        return card_pos

    instructions = parse(input.splitlines())
    return find_final_pos(2019, 10007, instructions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
