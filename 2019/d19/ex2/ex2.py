#!/usr/bin/env python

import sys
from copy import deepcopy
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterator, List, NamedTuple, Tuple


class ParameterMode(IntEnum):
    POSITION = 0  # Acts on address
    IMMEDIATE = 1  # Acts on the immediate value
    RELATIVE = 2  # Acts on offset to relative base


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


class InputInterrupt(Exception):
    pass


class OutputInterrupt(Exception):
    pass


@dataclass
class Computer:
    memory: List[int]  # Memory space
    rip: int = 0  # Instruction pointer
    input_list: List[int] = field(default_factory=list)
    output_list: List[int] = field(default_factory=list)
    is_halted: bool = field(default=False, init=False)
    relative_base: int = field(default=0, init=False)

    def run(self) -> None:
        while not self.is_halted:
            self.run_single()

    def run_no_output_interrupt(self) -> None:
        while not self.is_halted:
            try:
                self.run_single()
            except OutputInterrupt:
                continue

    def run_single(self) -> None:  # Returns True when halted
        instr = lookup_ops(self.rip, self.memory)
        if instr.op == 99:  # Halt
            self.is_halted = True
        elif instr.op == 1:  # Sum
            self._do_addition(instr)
        elif instr.op == 2:  # Multiplication
            self._do_multiplication(instr)
        elif instr.op == 3:  # Load from input
            self._do_input(instr)
        elif instr.op == 4:  # Store to output
            self._do_output(instr)
        elif instr.op == 5:  # Jump if true
            self._do_jump_if_true(instr)
        elif instr.op == 6:  # Jump if false
            self._do_jump_if_false(instr)
        elif instr.op == 7:  # Less than
            self._do_less_than(instr)
        elif instr.op == 8:  # Equal to
            self._do_equal_to(instr)
        elif instr.op == 9:  # Change relative base
            self._do_change_relative_base(instr)
        else:
            assert False  # Sanity check

    def _fill_to_addres(self, address: int) -> None:
        values = address - len(self.memory) + 1
        if values <= 0:
            return
        for __ in range(values):
            self.memory.append(0)

    def _get_value(self, mode: ParameterMode, val: int) -> int:
        if mode == ParameterMode.POSITION:
            assert 0 <= val  # Sanity check
            self._fill_to_addres(val)
            return self.memory[val]
        elif mode == ParameterMode.RELATIVE:
            val += self.relative_base
            assert 0 <= val  # Sanity check
            self._fill_to_addres(val)
            return self.memory[val]
        assert mode == ParameterMode.IMMEDIATE  # Sanity check
        return val

    def _set_value(self, mode: ParameterMode, address: int, value: int) -> None:
        if mode == ParameterMode.RELATIVE:
            address += self.relative_base
        else:
            assert mode == ParameterMode.POSITION  # Sanity check

        assert address >= 0  # Sanity check
        self._fill_to_addres(address)

        self.memory[address] = value

    def _do_addition(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        self._set_value(instr.p3_mode, dest, lhs + rhs)

        self.rip += 4  # Length of the instruction

    def _do_multiplication(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        self._set_value(instr.p3_mode, dest, lhs * rhs)

        self.rip += 4  # Length of the instruction

    def _do_input(self, instr: Instruction) -> None:
        if len(self.input_list) == 0:
            raise InputInterrupt  # No input, halt until an input is provided

        value = int(self.input_list.pop(0))
        param = self.memory[instr.address + 1]

        self._set_value(instr.p1_mode, param, value)

        self.rip += 2  # Length of the instruction

    def _do_output(self, instr: Instruction) -> None:
        value = self._get_value(instr.p1_mode, self.memory[instr.address + 1])

        self.output_list.append(value)

        self.rip += 2  # Length of the instruction
        raise OutputInterrupt  # Alert that we got an output to give

    def _do_jump_if_true(self, instr: Instruction) -> None:
        cond = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        value = self._get_value(instr.p2_mode, self.memory[instr.address + 2])

        if cond != 0:
            self.rip = value
        else:
            self.rip += 3  # Length of the instruction

    def _do_jump_if_false(self, instr: Instruction) -> None:
        cond = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        value = self._get_value(instr.p2_mode, self.memory[instr.address + 2])

        if cond == 0:
            self.rip = value
        else:
            self.rip += 3  # Length of the instruction

    def _do_less_than(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        self._set_value(instr.p3_mode, dest, 1 if lhs < rhs else 0)

        self.rip += 4  # Length of the instruction

    def _do_equal_to(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        self._set_value(instr.p3_mode, dest, 1 if lhs == rhs else 0)

        self.rip += 4  # Length of the instruction

    def _do_change_relative_base(self, instr: Instruction) -> None:
        value = self._get_value(instr.p1_mode, self.memory[instr.address + 1])

        self.relative_base += value
        self.rip += 2  # Length of the instruction


def true_at(memory: List[int], x: int, y: int) -> bool:
    drone = Computer(deepcopy(memory), input_list=[x, y])
    drone.run_no_output_interrupt()
    assert len(drone.output_list) == 1
    return drone.output_list.pop() == 1


def main() -> None:
    memory = [int(n) for n in sys.stdin.read().split(",")]

    x = 0
    y = 0
    size = 100
    while not true_at(memory, x + size - 1, y):
        y += 1
        while not true_at(memory, x, y + size - 1):
            x += 1
    print((x * 10000 + y))


if __name__ == "__main__":
    main()
