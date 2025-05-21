#!/usr/bin/env python

import enum
import operator
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    AND = "AND_"
    OR = "OR_"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    NOT = "NOT"
    IDENTITY = ""  # For the output to `a`, which has no operator

    def apply(self, lhs: int, rhs: int | None) -> int:
        if self == Op.IDENTITY:
            assert rhs is None
            return lhs
        if self == Op.NOT:
            assert rhs is None
            return ~lhs
        assert rhs is not None
        return getattr(operator, self.lower())(lhs, rhs)


class Instruction(NamedTuple):
    op: Op
    lhs: str
    rhs: str | None = None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        split_input = input.split()
        if len(split_input) == 1:
            op = ""
            lhs = split_input[0]
            rest = []
        elif split_input[0] == "NOT":
            op, lhs, *rest = split_input
        else:
            lhs, op, *rest = split_input
        # Hacky way to match with the function in the `operator` module...
        if op in ("AND", "OR"):
            op = op + "_"
        return cls(Op(op), lhs, *rest)


Circuit = dict[str, Instruction | int]


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[str, Instruction | int]:
        raw_instr, wire = input.split(" -> ")
        if raw_instr.isdigit():
            return wire, int(raw_instr)
        return wire, Instruction.from_str(raw_instr)

    def parse(input: str) -> Circuit:
        return {wire: val for wire, val in map(parse_line, input.splitlines())}

    def dependencies(circuit: Circuit) -> dict[str, set[str]]:
        res: dict[str, set[str]] = {wire: set() for wire in circuit.keys()}
        for wire, val in circuit.items():
            if isinstance(val, int):
                continue
            for dep in (val.lhs, val.rhs):
                if dep is None:
                    continue
                if dep.isdigit():
                    continue
                res[wire].add(dep)
        return res

    def topo_sort(dep_graph: dict[str, set[str]]) -> list[str]:
        res: list[str] = []

        queue = {n for n, deps in dep_graph.items() if not deps}
        seen: set[str] = set()

        while queue:
            node = queue.pop()

            res.append(node)
            seen.add(node)
            # Iterate over all nodes as we don't have information on children
            for child, deps in dep_graph.items():
                if child in seen:
                    continue
                if deps - seen:
                    continue
                queue.add(child)

        return res

    def run(circuit: Circuit) -> dict[str, int]:
        res: dict[str, int] = {}
        for wire in topo_sort(dependencies(circuit)):
            match circuit[wire]:
                case int(n):
                    res[wire] = n
                case Instruction(op, lhs, rhs):
                    resolve = lambda v: int(v) if v.isdigit() else res[v]
                    lhs_n = resolve(lhs)
                    rhs_n = None if rhs is None else resolve(rhs)
                    res[wire] = op.apply(lhs_n, rhs_n)
        return res

    circuit = parse(input)
    wires = run(circuit)
    return wires["a"]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
