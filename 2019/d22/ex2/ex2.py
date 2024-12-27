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

    def to_linear(instructions: list[Instruction]) -> tuple[int, int]:
        a, b = 1, 0
        for instr in instructions:
            new_a, new_b = instr.to_linear()
            a = a * new_a
            b = b * new_a + new_b
        return a, b

    def mod_pow(n: int, pow: int, mod: int) -> int:
        if pow == 0:
            return 1
        if pow == 1:
            return n % mod
        res = mod_pow(n, pow // 2, mod) ** 2
        if pow % 2 == 1:
            res *= n
        return res % mod

    def mod_inverse(n: int, mod: int) -> int:
        def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
            if b == 0:
                return a, 1, 0
            gcd, x, y = extended_gcd(b, a % b)
            # we want x * a + y * b == gcd
            return gcd, y, x - (a // b) * y

        gcd, _, y = extended_gcd(mod, n)
        assert gcd == 1  # Sanity check
        return y % mod

    def find_in_pos(
        card_pos: int, deck_size: int, repetitions: int, instructions: list[Instruction]
    ) -> int:
        a, b = to_linear(instructions)
        repeat_a = mod_pow(a, repetitions, deck_size)
        repeat_b = (b * (repeat_a - 1) * mod_inverse(a - 1, deck_size)) % deck_size

        return ((card_pos - repeat_b) * mod_inverse(repeat_a, deck_size)) % deck_size

    instructions = parse(input.splitlines())
    return find_in_pos(2020, 119315717514047, 101741582076661, instructions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
