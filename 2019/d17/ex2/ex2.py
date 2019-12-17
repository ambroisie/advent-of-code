#!/usr/bin/env python


import sys
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import List, NamedTuple


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


class Position(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


DIRECTIONS = [d for d in Direction]
ARROW_DIRECTION = {
    "^": Direction.NORTH,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
    ">": Direction.EAST,
}
DIRECTION_OFFSET = {
    Direction.NORTH: (-1, 0),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
    Direction.EAST: (0, 1),
}


def turn(d: Direction, turn: str) -> Direction:
    def turn_left() -> Direction:
        return DIRECTIONS[(DIRECTIONS.index(d) + 1) % len(DIRECTIONS)]

    def turn_right() -> Direction:
        return DIRECTIONS[DIRECTIONS.index(d) - 1]

    if turn == "L":
        return turn_left()
    elif turn == "R":
        return turn_right()
    assert False  # Sanity check


def find_arrow(mapped_view: List[List[str]]) -> Position:
    for x in range(len(mapped_view)):
        for y in range(len(mapped_view[0])):
            if mapped_view[x][y] in ARROW_DIRECTION:
                return Position(x, y)

    assert False  # Sanity check


def get_path(mapped_view: List[List[str]]) -> List[str]:
    pos = find_arrow(mapped_view)

    def pos_is_valid(p: Position) -> bool:
        return 0 <= p.x < len(mapped_view) and 0 <= p.y < len(mapped_view[0])

    def pos_is_scaffold(p: Position) -> bool:
        return pos_is_valid(p) and mapped_view[p.x][p.y] != "."

    direction = ARROW_DIRECTION[mapped_view[pos.x][pos.y]]
    ans: List[str] = []

    def advance_until_stopped(turn_string: str) -> bool:
        nonlocal pos
        nonlocal direction
        d = turn(direction, turn_string)
        offset = DIRECTION_OFFSET[d]
        neighbor = Position(*(a + b for a, b in zip(pos, offset)))
        tot = 0
        while pos_is_scaffold(neighbor):
            tot += 1
            mapped_view[pos.x][pos.y] = "@"
            pos = neighbor
            neighbor = Position(*(a + b for a, b in zip(pos, offset)))

        if tot == 0:
            return False
        direction = d
        ans.append(turn_string)
        ans.append(str(tot))
        return True

    has_no_neighbors = False
    while not has_no_neighbors:
        for turn_string in ("L", "R"):
            if advance_until_stopped(turn_string):
                break
        else:
            has_no_neighbors = True
    return ans


def sequitur_algorithm(path: str) -> None:
    # FIXME: seems like a good candidate for compression
    pass


def main() -> None:
    memory = [int(n) for n in sys.stdin.read().split(",")]
    camera = Computer(deepcopy(memory))

    camera.run_no_output_interrupt()

    view = "".join(chr(c) for c in camera.output_list)
    mapped_view = [[c for c in line] for line in view.split("\n") if line != ""]

    path = get_path(mapped_view)
    print(path)

    # I didn't want to write the compression algorithm when I could just use Vim
    # The answere is A,B,B,A,C,A,A,C,B,C
    # A: R,8,L,12,R,8
    # B: R,12,L,8,R,10
    # C: R,8,L,8,L,8,R,8,R,10

    ans = "A,B,B,A,C,A,A,C,B,C"
    A = "R,8,L,12,R,8"
    B = "R,12,L,8,R,10"
    C = "R,8,L,8,L,8,R,8,R,10"

    assert len(ans) <= 20  # Sanity check
    assert len(A) <= 20  # Sanity check
    assert len(B) <= 20  # Sanity check
    assert len(C) <= 20  # Sanity check

    memory[0] = 2  # Wake up the robot
    robot = Computer(memory)

    for c in ans:
        robot.input_list.append(ord(c))
    robot.input_list.append(ord("\n"))
    for c in A:
        robot.input_list.append(ord(c))
    robot.input_list.append(ord("\n"))
    for c in B:
        robot.input_list.append(ord(c))
    robot.input_list.append(ord("\n"))
    for c in C:
        robot.input_list.append(ord(c))
    robot.input_list.append(ord("\n"))

    for c in "n\n":  # Do not output the video feed
        robot.input_list.append(ord(c))

    robot.run_no_output_interrupt()
    print(robot.output_list.pop())


if __name__ == "__main__":
    main()
