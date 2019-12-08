#!/usr/bin/env python

from dataclasses import dataclass
from enum import IntEnum
from typing import List, NamedTuple


class ParameterMode(IntEnum):
    POSITION = 0  # Acts on address
    IMMEDIATE = 1  # Acts on the immediate value


class Instruction(NamedTuple):
    address: int  # The address of the instruction, for convenience
    op: int  # The opcode
    p1_mode: ParameterMode  # Which mode is the first parameter in
    p2_mode: ParameterMode  # Which mode is the second parameter in
    p3_mode: ParameterMode  # Which mode is the third parameter in


def lookup_ops(index: int, memory: List[int]) -> Instruction:
    digits = list(map(int, str(memory[index])))
    a, b, c, d, e = [0] * (5 - len(digits)) + digits  # Pad with default values
    return Instruction(
        address=index,
        op=d * 10 + e,
        p1_mode=ParameterMode(c),
        p2_mode=ParameterMode(b),
        p3_mode=ParameterMode(a),
    )


@dataclass
class Computer:
    memory: List[int]  # Memory space
    rip: int = 0  # Instruction pointer

    def run(self):
        while True:
            instr = lookup_ops(self.rip, self.memory)
            if instr.op == 99:  # Halt
                return
            elif instr.op == 1:  # Sum
                self.do_addition(instr)
            elif instr.op == 2:  # Multiplication
                self.do_multiplication(instr)
            elif instr.op == 3:  # Load from input
                self.do_input(instr)
            elif instr.op == 4:  # Store to output
                self.do_output(instr)
            elif instr.op == 5:  # Jump if true
                self.do_jump_if_true(instr)
            elif instr.op == 6:  # Jump if false
                self.do_jump_if_false(instr)
            elif instr.op == 7:  # Less than
                self.do_less_than(instr)
            elif instr.op == 8:  # Equal to
                self.do_equal_to(instr)
            else:
                assert False  # Sanity check

    def do_addition(self, instr: Instruction) -> None:
        lhs, rhs, dest = self.memory[instr.address + 1 : instr.address + 4]

        if instr.p1_mode == ParameterMode.POSITION:
            lhs = self.memory[lhs]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            rhs = self.memory[rhs]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = lhs + rhs

        self.rip += 4  # Length of the instruction

    def do_multiplication(self, instr: Instruction) -> None:
        lhs, rhs, dest = self.memory[instr.address + 1 : instr.address + 4]

        if instr.p1_mode == ParameterMode.POSITION:
            lhs = self.memory[lhs]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            rhs = self.memory[rhs]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = lhs * rhs

        self.rip += 4  # Length of the instruction

    def do_input(self, instr: Instruction) -> None:
        value = int(input())
        param = self.memory[instr.address + 1]

        assert instr.p1_mode == ParameterMode.POSITION  # Sanity check
        self.memory[param] = value

        self.rip += 2  # Length of the instruction

    def do_output(self, instr: Instruction) -> None:
        value = self.memory[instr.address + 1]
        if instr.p1_mode == ParameterMode.POSITION:
            value = self.memory[value]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        print(value)

        self.rip += 2  # Length of the instruction

    def do_jump_if_true(self, instr: Instruction) -> None:
        cond, value = self.memory[instr.address + 1 : instr.address + 3]

        if instr.p1_mode == ParameterMode.POSITION:
            cond = self.memory[cond]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            value = self.memory[value]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        if cond != 0:
            self.rip = value
        else:
            self.rip += 3  # Length of the instruction

    def do_jump_if_false(self, instr: Instruction) -> None:
        cond, value = self.memory[instr.address + 1 : instr.address + 3]

        if instr.p1_mode == ParameterMode.POSITION:
            cond = self.memory[cond]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            value = self.memory[value]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        if cond == 0:
            self.rip = value
        else:
            self.rip += 3  # Length of the instruction

    def do_less_than(self, instr: Instruction) -> None:
        lhs, rhs, dest = self.memory[instr.address + 1 : instr.address + 4]

        if instr.p1_mode == ParameterMode.POSITION:
            lhs = self.memory[lhs]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            rhs = self.memory[rhs]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = 1 if lhs < rhs else 0

        self.rip += 4  # Length of the instruction

    def do_equal_to(self, instr: Instruction) -> None:
        lhs, rhs, dest = self.memory[instr.address + 1 : instr.address + 4]

        if instr.p1_mode == ParameterMode.POSITION:
            lhs = self.memory[lhs]
        else:
            assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

        if instr.p2_mode == ParameterMode.POSITION:
            rhs = self.memory[rhs]
        else:
            assert instr.p2_mode == ParameterMode.IMMEDIATE  # Sanity check

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = 1 if lhs == rhs else 0

        self.rip += 4  # Length of the instruction


def main() -> None:
    with open("input") as mem_f:
        memory = [int(n) for n in mem_f.read().split(",")]
        computer = Computer(memory)
        computer.run()


if __name__ == "__main__":
    main()
