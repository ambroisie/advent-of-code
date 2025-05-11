#!/usr/bin/env python

import collections
import enum
import sys
from typing import NamedTuple


class Direction(enum.StrEnum):
    LEFT = "left"
    RIGHT = "right"

    def apply(self, pos: int) -> int:
        return pos + 1 if self == Direction.RIGHT else pos - 1


class Rules(NamedTuple):
    zero_write: bool
    zero_dir: Direction
    zero_transition: str

    one_write: bool
    one_dir: Direction
    one_transition: str

    @classmethod
    def from_str(cls, input: str) -> "Rules":
        lines = input.splitlines()
        return cls(
            zero_write=bool(int(lines[1][-2])),
            zero_dir=Direction(lines[2][:-1].split()[-1]),
            zero_transition=lines[3][-2],
            one_write=bool(int(lines[5][-2])),
            one_dir=Direction(lines[6][:-1].split()[-1]),
            one_transition=lines[7][-2],
        )

    def apply(self, tape: dict[int, bool], pos: int) -> tuple[str, int]:
        if tape[pos]:
            tape[pos] = self.one_write
            return self.one_transition, self.one_dir.apply(pos)
        else:
            tape[pos] = self.zero_write
            return self.zero_transition, self.zero_dir.apply(pos)


def solve(input: str) -> int:
    def parse_rules(input: str) -> tuple[str, Rules]:
        assert input.startswith("In state ")  # Sanity check
        state, lines = input.split("\n", 1)
        return state[-2], Rules.from_str(lines)

    def parse(input: str) -> tuple[str, int, dict[str, Rules]]:
        first, *rest = input.split("\n\n")
        raw_state, raw_checksum = first.splitlines()
        rules = {state: rules for state, rules in map(parse_rules, rest)}
        return raw_state[-2], int(raw_checksum.split()[-2]), rules

    state, iterations, rules = parse(input)
    pos = 0
    tape: dict[int, bool] = collections.defaultdict(bool)
    for _ in range(iterations):
        state, pos = rules[state].apply(tape, pos)
    return sum(tape.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
