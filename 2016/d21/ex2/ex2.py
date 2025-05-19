#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    SWAP_POSITION = "swap position"
    SWAP_LETTER = "swap letter"
    ROTATE_LEFT = "rotate left"
    ROTATE_RIGHT = "rotate right"
    ROTATE_BASED = "rotate based"
    REVERSE_POSITION = "reverse positions"
    MOVE_POSITION = "move position"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str | None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        split_input = input.split()
        op = Op(" ".join(split_input[:2]))
        x: str
        y: str | None
        match op:
            case Op.ROTATE_LEFT | Op.ROTATE_RIGHT:
                x, y = split_input[2], None
            case Op.ROTATE_BASED:
                x, y = split_input[-1], None
            case _:
                x, y = split_input[2], split_input[-1]
        return cls(op, x, y)

    def undo(self, password: str) -> str:
        letters = list(password)
        match self.op:
            case Op.SWAP_POSITION:
                assert self.y is not None  # Sanity check
                x, y = int(self.x), int(self.y)
                letters[x], letters[y] = letters[y], letters[x]
            case Op.SWAP_LETTER:
                assert self.y is not None  # Sanity check
                x, y = letters.index(self.x), letters.index(self.y)
                letters[x], letters[y] = letters[y], letters[x]
            case Op.ROTATE_LEFT:
                x = int(self.x)
                x %= len(letters)
                letters = letters[-x:] + letters[:-x]
            case Op.ROTATE_RIGHT:
                x = int(self.x)
                x %= len(letters)
                letters = letters[x:] + letters[:x]
            case Op.ROTATE_BASED:
                # original: 0 1 2 3 4 5 6 7
                #   result: 1 3 5 7 2 4 6 0
                # rotation: 1 2 3 4 6 7 0 1
                x = {
                    1: 1,
                    3: 2,
                    5: 3,
                    7: 4,
                    2: 6,
                    4: 7,
                    6: 0,
                    0: 1,
                }[letters.index(self.x)]
                letters = letters[x:] + letters[:x]
            case Op.REVERSE_POSITION:
                assert self.y is not None  # Sanity check
                x, y = int(self.x), int(self.y)
                letters[x : y + 1] = letters[x : y + 1][::-1]
            case Op.MOVE_POSITION:
                assert self.y is not None  # Sanity check
                x, y = int(self.x), int(self.y)
                letter = letters.pop(y)
                letters.insert(x, letter)
        return "".join(letters)


def solve(input: str) -> str:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    instructions = parse(input)
    password = "fbgdceah"
    for instruction in instructions[::-1]:
        password = instruction.undo(password)
    return password


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
