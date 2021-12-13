#!/usr/bin/env python

# Mypy has issues with assigning Callable to fields of objects
# See https://github.com/python/mypy/issues/708
# type: ignore

import itertools
import sys
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum
from typing import Callable, List, NamedTuple


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
    read_input: Callable[[], str] = input
    print_output: Callable[[int], None] = print

    def run(self) -> None:
        is_halted = self.run_single()
        while not is_halted:
            is_halted = self.run_single()

    def run_single(self) -> bool:  # Returns True when halted
        instr = lookup_ops(self.rip, self.memory)
        if instr.op == 99:  # Halt
            return True  # Halted
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
        return False  # Not halted

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
        value = int(self.read_input())
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

        self.print_output(value)

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
    def get_input_fun(phase: int, last_output: List[int]) -> Callable[[], str]:
        has_been_called = False

        def _input() -> str:
            nonlocal has_been_called
            if has_been_called:
                return str(last_output.pop(0))
            has_been_called = True
            return str(phase)

        return _input

    memory = [int(n) for n in sys.stdin.read().split(",")]
    max = 0
    ans = tuple(-1 for __ in range(5))
    for a, b, c, d, e in itertools.permutations(range(5)):
        amp1 = Computer(deepcopy(memory))
        amp1_output: List[int] = []
        amp1.read_input = get_input_fun(a, [0])
        amp1.print_output = lambda x: amp1_output.append(int(x))

        amp2 = Computer(deepcopy(memory))
        amp2_output: List[int] = []
        amp2.read_input = get_input_fun(b, amp1_output)
        amp2.print_output = lambda x: amp2_output.append(int(x))

        amp3 = Computer(deepcopy(memory))
        amp3_output: List[int] = []
        amp3.read_input = get_input_fun(c, amp2_output)
        amp3.print_output = lambda x: amp3_output.append(int(x))

        amp4 = Computer(deepcopy(memory))
        amp4_output: List[int] = []
        amp4.read_input = get_input_fun(d, amp3_output)
        amp4.print_output = lambda x: amp4_output.append(int(x))

        amp5 = Computer(deepcopy(memory))
        amp5_output: List[int] = []
        amp5.read_input = get_input_fun(e, amp4_output)
        amp5.print_output = lambda x: amp5_output.append(int(x))

        amp1.run()
        amp2.run()
        amp3.run()
        amp4.run()
        amp5.run()

        res = amp5_output.pop(0)
        if res > max:
            max = res
            ans = (a, b, c, d, e)
            print(f"Max: {max}, res: {ans}")

    print(f"Final one: {max}, with {ans}")


if __name__ == "__main__":
    main()
