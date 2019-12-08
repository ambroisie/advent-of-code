#!/usr/bin/env python

import sys
from copy import deepcopy
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


def do_addition(instr: Instruction, memory: List[int]) -> int:
    lhs, rhs, dest = memory[instr.address + 1 : instr.address + 4]
    if instr.p1_mode == ParameterMode.POSITION:
        lhs = memory[lhs]
    if instr.p2_mode == ParameterMode.POSITION:
        rhs = memory[rhs]
    assert instr.p3_mode != ParameterMode.IMMEDIATE  # Sanity check
    memory[dest] = lhs + rhs

    return 4  # Length of the instruction


def do_multiplication(instr: Instruction, memory: List[int]) -> int:
    lhs, rhs, dest = memory[instr.address + 1 : instr.address + 4]
    if instr.p1_mode == ParameterMode.POSITION:
        lhs = memory[lhs]
    if instr.p2_mode == ParameterMode.POSITION:
        rhs = memory[rhs]
    assert instr.p3_mode != ParameterMode.IMMEDIATE  # Sanity check
    memory[dest] = lhs * rhs

    return 4  # Length of the instruction


def do_input(instr: Instruction, memory: List[int]) -> int:
    value = int(input())
    param = memory[instr.address + 1]

    assert instr.p1_mode == ParameterMode.POSITION  # Sanity check
    memory[param] = value

    return 2  # Length of the instruction


def do_output(instr: Instruction, memory: List[int]) -> int:
    value = memory[instr.address + 1]
    if instr.p1_mode == ParameterMode.POSITION:
        value = memory[value]
    else:
        assert instr.p1_mode == ParameterMode.IMMEDIATE  # Sanity check

    print(value)

    return 2  # Length of the instruction


def run_op(memory: List[int]) -> None:
    index = 0
    while True:
        instr = lookup_ops(index, memory)
        if instr.op == 99:  # Halt
            return
        elif instr.op == 1:  # Sum
            index += do_addition(instr, memory)
        elif instr.op == 2:  # Multiplication
            index += do_multiplication(instr, memory)
        elif instr.op == 3:  # Load from input
            index += do_input(instr, memory)
        elif instr.op == 4:  # Store to output
            index += do_output(instr, memory)


def main() -> None:
    with open("input") as mem_f:
        memory = [int(n) for n in mem_f.read().split(",")]
        run_op(memory)


if __name__ == "__main__":
    main()
