#!/usr/bin/env python

import dataclasses
import enum
import sys


@dataclasses.dataclass
class Registers:
    reg_a: int
    reg_b: int
    reg_c: int


class Instruction(enum.IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclasses.dataclass
class Computer:
    registers: Registers
    program: list[int]
    ip: int = 0

    def _resolve_combo_operand(self, operand: int) -> int:
        assert operand != 7  # Sanity check
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.registers.reg_a
        if operand == 5:
            return self.registers.reg_b
        if operand == 6:
            return self.registers.reg_c
        assert False  # Sanity check

    # Returns False if the computer is halted
    # `output` is an out parameter
    def step(self, output: list[int]) -> bool:
        # NOTE: also accounting for operand in overflow check here
        if (self.ip + 1) >= len(self.program):
            return False

        instr, literal_operand = (
            Instruction(self.program[self.ip]),
            self.program[self.ip + 1],
        )
        combo_operand = self._resolve_combo_operand(literal_operand)

        ip_delta = 2
        match instr:
            case Instruction.ADV:
                self.registers.reg_a //= 2**combo_operand
            case Instruction.BXL:
                self.registers.reg_b ^= literal_operand
            case Instruction.BST:
                self.registers.reg_b = combo_operand % 8
            case Instruction.JNZ:
                if self.registers.reg_a != 0:
                    self.ip = literal_operand
                    ip_delta = 0
            case Instruction.BXC:
                self.registers.reg_b ^= self.registers.reg_c
            case Instruction.OUT:
                output.append(combo_operand % 8)
            case Instruction.BDV:
                self.registers.reg_b = self.registers.reg_a // 2**combo_operand
            case Instruction.CDV:
                self.registers.reg_c = self.registers.reg_a // 2**combo_operand
        self.ip += ip_delta

        return True


def solve(input: str) -> str:
    def parse_registers(input: list[str]) -> Registers:
        def parse_register(input: str) -> int:
            return int(input.split(": ")[1])

        return Registers(*map(parse_register, input))

    def parse(input: str) -> Computer:
        registers, program_str = input.split("\n\n")
        program = list(map(int, program_str.removeprefix("Program: ").split(",")))
        return Computer(parse_registers(registers.splitlines()), program)

    computer = parse(input)
    output: list[int] = []
    while computer.step(output):
        pass
    return ",".join(str(n) for n in output)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
