#!/usr/bin/env python

import enum
import sys
from collections import defaultdict
from typing import NamedTuple


class Op(enum.StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def apply(self, lhs: bool, rhs: bool) -> bool:
        match self:
            case Op.AND:
                return lhs & rhs
            case Op.OR:
                return lhs | rhs
            case Op.XOR:
                return lhs ^ rhs


class Gate(NamedTuple):
    lhs: str
    op: Op
    rhs: str


def solve(input: str) -> str:
    def parse_values(input: list[str]) -> dict[str, bool]:
        return {
            name: bool(int(val)) for name, val in map(lambda s: s.split(": "), input)
        }

    def parse_operation(input: str) -> tuple[str, Gate]:
        lhs, op, rhs, _, name = input.split()
        return name, Gate(lhs, Op(op), rhs)

    def parse_circuit(input: list[str]) -> dict[str, Gate]:
        return {name: gate for name, gate in map(parse_operation, input)}

    def parse(input: str) -> tuple[dict[str, bool], dict[str, Gate]]:
        values, circuit = input.split("\n\n")
        return parse_values(values.splitlines()), parse_circuit(circuit.splitlines())

    def downstream_ops(circuit: dict[str, Gate]) -> dict[str, set[Op]]:
        res: dict[str, set[Op]] = defaultdict(set)
        for gate in circuit.values():
            res[gate.lhs].add(gate.op)
            res[gate.rhs].add(gate.op)
        return res

    def match_adders(circuit: dict[str, Gate]) -> set[str]:
        def validate_and(wire: str, wire_ops: dict[str, set[Op]]) -> bool:
            gate = circuit[wire]
            assert gate.op == Op.AND  # Sanity check

            # AND must lead into an OR carry, unless it reads the first bit
            return wire_ops[wire] == {Op.OR} or {gate.lhs, gate.rhs} == {"x00", "y00"}

        def validate_or(wire: str, wire_ops: dict[str, set[Op]]) -> bool:
            gate = circuit[wire]
            assert gate.op == Op.OR  # Sanity check

            # OR outputs the last bit as a direct carry, or into an AND and XOR
            return wire == "z45" or wire_ops[wire] == {Op.AND, Op.XOR}

        def validate_xor(wire: str, wire_ops: dict[str, set[Op]]) -> bool:
            gate = circuit[wire]
            assert gate.op == Op.XOR  # Sanity check

            inputs = {gate.lhs, gate.rhs}
            has_input = all(any(i.startswith(w) for i in inputs) for w in ("x", "y"))

            # If lowest bit, XOR has no carry and outputs directly
            if inputs == {"x00", "y00"} and wire == "z00":
                return True
            # Otherwise, if it read input bits, it outputs to a carry XOR
            if has_input and Op.XOR in wire_ops[wire]:
                return True
            # If it doesn't read input bits, it must output to Z
            if not has_input and wire.startswith("z"):
                return True
            return False

        def validate(wire: str, wire_ops: dict[str, set[Op]]) -> bool:
            return {
                Op.AND: validate_and,
                Op.OR: validate_or,
                Op.XOR: validate_xor,
            }[circuit[wire].op](wire, wire_ops)

        wire_ops = downstream_ops(circuit)
        return {wire for wire in circuit if not validate(wire, wire_ops)}

    _, circuit = parse(input)
    return ",".join(sorted(match_adders(circuit)))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
