#!/usr/bin/env python

import collections
import dataclasses
import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    SND = "snd"
    SET = "set"
    ADD = "add"
    MUL = "mul"
    MOD = "mod"
    RCV = "rcv"
    JGZ = "jgz"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str | None = None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        op, *rest = input.split()
        return cls(Op(op), *rest)


@dataclasses.dataclass
class Program:
    instructions: list[Instruction]
    id: dataclasses.InitVar[int]
    registers: dict[str, int] = dataclasses.field(init=False)
    ip: int = dataclasses.field(init=False, default=0)

    receive_queue: collections.deque[int] = dataclasses.field(
        init=False, default_factory=collections.deque
    )
    send_queue: collections.deque[int] = dataclasses.field(
        init=False, default_factory=collections.deque
    )
    values_sent: int = dataclasses.field(init=False, default=0)

    def __post_init__(self, id: int) -> None:
        self.registers = collections.defaultdict(int)
        self.registers["p"] = id

    def _resolve(self, y: str | None) -> int:
        assert y is not None  # Sanity check
        try:
            return int(y)
        except ValueError:
            return self.registers[y]

    def execute(self) -> None:
        while True:
            assert 0 <= self.ip < len(self.instructions)  # Sanity check
            instr = self.instructions[self.ip]
            match instr.op:
                case Op.SND:
                    self.send_queue.append(self._resolve(instr.x))
                    self.values_sent += 1
                case Op.SET:
                    self.registers[instr.x] = self._resolve(instr.y)
                case Op.ADD:
                    self.registers[instr.x] += self._resolve(instr.y)
                case Op.MUL:
                    self.registers[instr.x] *= self._resolve(instr.y)
                case Op.MOD:
                    self.registers[instr.x] %= self._resolve(instr.y)
                case Op.RCV:
                    if not self.receive_queue:
                        return  # Block and wait for a value to be sent
                    self.registers[instr.x] = self.receive_queue.popleft()
                case Op.JGZ:
                    if self._resolve(instr.x) > 0:
                        self.ip += self._resolve(instr.y) - 1  # Account auto-increment
            self.ip += 1

    @property
    def is_terminated(self) -> bool:
        # Has the program jumped outside the instructions
        return self.ip < 0 or self.ip >= len(self.instructions)

    @property
    def is_blocked(self) -> bool:
        if self.is_terminated:
            return True
        # Is it blocked on a `RCV`
        return self.instructions[self.ip].op == Op.RCV and not self.receive_queue


def solve(input: str) -> int:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    instructions = parse(input)
    p0, p1 = Program(instructions, id=0), Program(instructions, id=1)

    while True:
        if p0.is_blocked and p1.is_blocked:
            return p1.values_sent

        p0.execute()
        p1.execute()

        p0.receive_queue.extend(p1.send_queue)
        p1.send_queue.clear()
        p1.receive_queue.extend(p0.send_queue)
        p0.send_queue.clear()


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
