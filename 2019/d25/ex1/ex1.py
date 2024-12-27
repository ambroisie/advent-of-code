#!/usr/bin/env python

import itertools
import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
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

    def run_until_input_interrupt(self) -> None:
        while not self.is_halted:
            try:
                self.run_no_output_interrupt()
            except InputInterrupt:
                return

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


class Move(StrEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def opposite(self) -> "Move":
        if self == Move.NORTH:
            return Move.SOUTH
        if self == Move.SOUTH:
            return Move.NORTH
        if self == Move.EAST:
            return Move.WEST
        if self == Move.WEST:
            return Move.EAST
        assert False  # Sanity check


@dataclass
class Graph:
    nodes: dict[str, dict[Move, str]] = field(default_factory=dict)
    explored: set[str] = field(default_factory=set)

    def add_room(self, room: str) -> None:
        self.nodes.setdefault(room, {})

    def add_door(self, room: str, move: Move) -> None:
        if move in self.nodes[room]:
            return

        other_room = f"{move} of {room}"
        self.nodes[room][move] = other_room
        self.add_room(other_room)
        self.nodes[other_room].setdefault(move.opposite(), room)

    def set_visited(self, room: str) -> None:
        self.explored.add(room)

    # FIXME: repetition
    def goto(self, start: str, end: str) -> list[Move]:
        queue: deque[tuple[str, list[Move]]] = deque([(start, [])])
        visited: set[str] = {start}

        while queue:
            room, path = queue.popleft()
            visited.add(room)
            if room == end:
                return path
            for dir, neighbour in self.nodes[room].items():
                if neighbour in visited:
                    continue
                queue.append((neighbour, path + [dir]))

        assert False  # Sanity check

    def visit_unexplored(self, start: str) -> tuple[str, list[Move]] | None:
        queue: deque[tuple[str, list[Move]]] = deque([(start, [])])
        visited: set[str] = {start}

        while queue:
            room, path = queue.popleft()
            visited.add(room)
            if room not in self.explored:
                return room, path
            for dir, neighbour in self.nodes[room].items():
                if neighbour in visited:
                    continue
                queue.append((neighbour, path + [dir]))

        return None

    def rename(self, old: str, new: str) -> None:
        if old == new or old not in self.nodes:
            return

        self.nodes[new] = self.nodes.pop(old)
        for neighbours in self.nodes.values():
            for move in Move:
                if move not in neighbours:
                    continue
                neighbours[move] = new if neighbours[move] == old else neighbours[move]

        if old in self.explored:
            self.explored.remove(old)
            self.explored.add(new)


def get_room_name(output: list[str]) -> str:
    for line in output:
        if not line.startswith("== "):
            continue
        return line.replace("==", "").strip()
    assert False  # Sanity check


def add_doors(
    output: list[str],
    room: str,
    graph: Graph,
) -> None:
    DOORS_LEAD = "Doors here lead:"

    if DOORS_LEAD not in output:
        return

    doors_lead_index = output.index(DOORS_LEAD)
    doors_lead_end = output.index("", doors_lead_index)
    directions = [
        Move(line.removeprefix("- "))
        for line in output[doors_lead_index:doors_lead_end]
        if line.startswith("- ")
    ]

    for dir in directions:
        graph.add_door(room, dir)


def gather_items_in_room(
    output: list[str],
) -> list[str]:
    ITEMS_HERE = "Items here:"
    # XXX: hard-coded list of items
    CURSED_ITEMS = {
        "escape pod",
        "giant electromagnet",
        "infinite loop",
        "molten lava",
        "photons",
    }

    if ITEMS_HERE not in output:
        return []

    items_here_index = output.index(ITEMS_HERE)
    items_here_end = output.index("", items_here_index)
    items = [
        line.removeprefix("- ")
        for line in output[items_here_index:items_here_end]
        if line.startswith("- ")
    ]
    return [f"take {item}" for item in items if item not in CURSED_ITEMS]


def explore_rooms(
    output: list[str],
    room: str,
    graph: Graph,
) -> tuple[str, list[str], bool]:
    SECURITY = "Security Checkpoint"

    # Commands we want to execute
    commands: list[str] = []

    # Get the actual room name, and fix the graph to refer to it
    actual_room = get_room_name(output)
    graph.rename(room, actual_room)
    room = actual_room

    # Mark this room as visited
    graph.set_visited(room)

    # Add new doors to graph, except security checkpoint which won't let us through
    if room != SECURITY:
        add_doors(output, room, graph)

    # Gather items in room
    commands += gather_items_in_room(output)

    # Go to an unexplored room if possible
    if (res := graph.visit_unexplored(room)) is not None:
        room, path = res
        commands += path
    else:
        # Go to security room otherwise, with all our items
        return SECURITY, list(map(str, graph.goto(room, SECURITY))), False

    return room, commands, True


def get_last_output(droid: Computer) -> list[str]:
    output = "".join(map(chr, droid.output_list))
    droid.output_list.clear()
    res: list[str] = []
    for line in output.splitlines()[::-1]:
        res.append(line)
        if line.startswith("== "):
            break
    return res[::-1]


def gather_items(droid: Computer) -> Computer:
    # Avoid changing the input droid
    droid = deepcopy(droid)

    room = "Starting room"
    graph = Graph()
    graph.add_room(room)

    needs_items = True
    while needs_items:
        droid.run_until_input_interrupt()
        output = get_last_output(droid)
        room, commands, needs_items = explore_rooms(output, room, graph)
        commands.append("")  # Account for final new-line
        droid.input_list.extend(map(ord, "\n".join(commands)))

    # Finish going back to security
    droid.run_until_input_interrupt()
    # And drain last output
    get_last_output(droid)

    return droid


def get_current_items(droid: Computer) -> set[str]:
    # Avoid changing the input droid
    droid = deepcopy(droid)

    assert not droid.input_list  # Sanity check
    assert not droid.output_list  # Sanity check

    droid.input_list = list(map(ord, "inv\n"))
    droid.run_until_input_interrupt()
    return {
        line.removeprefix("- ")
        for line in "".join(map(chr, droid.output_list)).splitlines()
        if line.startswith("- ")
    }


def go_through_security(droid: Computer) -> Computer:
    items = get_current_items(droid)

    for r in range(0, len(items)):
        for keep in itertools.combinations(items, r):
            drop = items - set(keep)

            # Try on a temporary droid, use `droid` as a save point
            tmp_droid = deepcopy(droid)
            tmp_droid.input_list.extend(
                map(ord, "".join(f"drop {item}\n" for item in drop))
            )
            # XXX: hard-coded direction of final room
            tmp_droid.input_list.extend(map(ord, "west\n"))

            try:
                tmp_droid.run_no_output_interrupt()
            except InputInterrupt:
                # This set of items failed, try again
                continue
            # We halted, return the droid
            return tmp_droid

    assert False


def solve(input_str: str) -> int:
    memory = [int(n) for n in input_str.split(",")]
    droid = Computer(memory)

    # Explore the ship and gather all items
    droid = gather_items(droid)

    # Go through checkpoint weight plate
    droid = go_through_security(droid)

    final_output = "".join(map(chr, droid.output_list))
    # Most terrible parsing of the year
    return int(final_output.splitlines()[-1].split("typing ")[1].split()[0])


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
