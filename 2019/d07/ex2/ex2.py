#!/usr/bin/env python

import itertools
import sys
from copy import deepcopy
from dataclasses import dataclass, field
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

    def run(self) -> None:
        while not self.is_halted:
            self.run_single()

    def run_single(self):  # Returns True when halted
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
        else:
            assert False  # Sanity check

    def _get_value(self, mode: ParameterMode, val: int) -> int:
        if mode == ParameterMode.POSITION:
            return self.memory[val]
        assert mode == ParameterMode.IMMEDIATE  # Sanity check
        return val

    def _do_addition(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = lhs + rhs

        self.rip += 4  # Length of the instruction

    def _do_multiplication(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = lhs * rhs

        self.rip += 4  # Length of the instruction

    def _do_input(self, instr: Instruction) -> None:
        if len(self.input_list) == 0:
            raise InputInterrupt  # No input, halt until an input is provided

        value = int(self.input_list.pop(0))
        param = self.memory[instr.address + 1]

        assert instr.p1_mode == ParameterMode.POSITION  # Sanity check
        self.memory[param] = value

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

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = 1 if lhs < rhs else 0

        self.rip += 4  # Length of the instruction

    def _do_equal_to(self, instr: Instruction) -> None:
        lhs = self._get_value(instr.p1_mode, self.memory[instr.address + 1])
        rhs = self._get_value(instr.p2_mode, self.memory[instr.address + 2])
        dest = self.memory[instr.address + 3]

        assert instr.p3_mode == ParameterMode.POSITION  # Sanity check
        self.memory[dest] = 1 if lhs == rhs else 0

        self.rip += 4  # Length of the instruction


def main() -> None:
    memory = [int(n) for n in sys.stdin.read().split(",")]
    max = 0
    ans = tuple(-1 for __ in range(5))
    for perm in itertools.permutations(range(5, 10)):
        amps = [Computer(deepcopy(memory), input_list=[phase]) for phase in perm]

        amp1 = amps[0]  # Keep track of this guy for the output solution
        amp1.input_list.append(0)  # Initial input

        while not all(amp.is_halted for amp in amps):
            # Put a non halted comuter to the front
            while amps[0].is_halted:
                amps.append(amps.pop(0))
            # Run it until exhaustion or input/output interrupt
            try:
                amps[0].run()
            except InputInterrupt:
                amps.append(amps.pop(0))
            except OutputInterrupt:
                amps[1].input_list.append(amps[0].output_list.pop())

        res = amp1.input_list.pop(0)  # Amplifier 5 output to amplifier 1 at the end
        if res > max:
            max = res
            ans = perm
            print(f"Max: {max}, res: {ans}")

    print(f"Final one: {max}, with {ans}")


if __name__ == "__main__":
    main()
