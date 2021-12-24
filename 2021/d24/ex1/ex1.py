#!/usr/bin/env python

import enum
import functools
import sys
from typing import List, Literal, NamedTuple, Optional, Union, cast

import z3

Register = Literal["w", "x", "y", "z"]


class InstructionType(enum.Enum):
    INPUT = "inp"
    ADD = "add"
    MULTIPLY = "mul"
    DIVIDE = "div"
    MODULO = "mod"
    EQUAL = "eql"


class Instruction(NamedTuple):
    type: InstructionType
    destination: Register
    source: Optional[Union[Register, int]]


def solve(input: List[str]) -> int:
    def parse() -> List[Instruction]:
        def parse_instruction(line: str) -> Instruction:
            type, *registers = line.split()

            assert registers[0] in ("w", "x", "y", "z")  # Sanity check
            destination = cast(Register, registers[0])

            source: Optional[Union[Register, int]] = None
            if type != "inp":
                if registers[1] in ("w", "x", "y", "z"):
                    source = cast(Register, registers[1])
                else:
                    source = int(registers[1])

            return Instruction(InstructionType(type), destination, source)

        return [parse_instruction(line) for line in input]

    def run_z3(instructions: List[Instruction]) -> int:
        solver = z3.Optimize()

        BITS = 64

        digits = [z3.BitVec(f"input_{i}", BITS) for i in range(14)]
        next_input = iter(digits).__next__

        for d in digits:
            solver.add(z3.And(1 <= d, d <= 9))

        zero, one = z3.BitVecVal(0, BITS), z3.BitVecVal(1, BITS)

        registers = {r: zero for r in ("w", "x", "y", "z")}

        for i, instr in enumerate(instructions):
            if instr.type == InstructionType.INPUT:
                registers[instr.destination] = next_input()
                continue

            assert instr.source is not None  # Sanity check

            value = registers[instr.destination]
            if isinstance(instr.source, int):
                source = z3.BitVecVal(instr.source, BITS)
            else:
                source = registers[instr.source]

            res = z3.BitVec(f"result_{i}", BITS)
            if instr.type == InstructionType.ADD:
                solver.add(res == (value + source))
            elif instr.type == InstructionType.MULTIPLY:
                solver.add(res == (value * source))
            elif instr.type == InstructionType.DIVIDE:
                solver.add(source > zero)  # Sanity check
                solver.add(res == (value / source))
            elif instr.type == InstructionType.MODULO:
                solver.add(value >= zero)  # Sanity check
                solver.add(source > zero)  # Sanity check
                solver.add(res == (value % source))
            elif instr.type == InstructionType.EQUAL:
                solver.add(res == z3.If(value == source, one, zero))
            else:
                assert False  # Sanity check
            registers[instr.destination] = res

        solver.add(registers["z"] == zero)

        model_number = functools.reduce(lambda a, b: a * 10 + b, digits)

        solver.maximize(model_number)
        assert solver.check() == z3.sat  # Sanity check

        return solver.model().eval(model_number)

    return run_z3(parse())


def main() -> None:
    input = [line.rstrip("\n") for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
