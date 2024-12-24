#!/usr/bin/env python

import copy
import enum
import sys
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


def solve(input: str) -> int:
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

    def run_circuit(
        values: dict[str, bool], circuit: dict[str, Gate]
    ) -> dict[str, bool]:
        def helper(values: dict[str, bool], wire: str) -> bool:
            if (res := values.get(wire)) is not None:
                return res
            gate = circuit[wire]
            val = gate.op.apply(helper(values, gate.lhs), helper(values, gate.rhs))
            values[wire] = val
            return val

        res = copy.copy(values)
        for key in circuit:
            helper(res, key)
        return res

    def read_zs(values: dict[str, bool]) -> int:
        zs = sorted(
            (wire for wire in values.keys() if wire.startswith("z")), reverse=True
        )
        res = 0
        for z in zs:
            res = res << 1 | values[z]
        return res

    values, circuit = parse(input)
    values = run_circuit(values, circuit)
    return read_zs(values)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
