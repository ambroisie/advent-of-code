#!/usr/bin/env python

import collections
import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def parse(input: str) -> tuple[dict[str, list[str]], str]:
        raw_replacements, molecule = input.strip().split("\n\n")
        res: dict[str, list[str]] = collections.defaultdict(list)
        for start, end in (
            line.split(" => ") for line in raw_replacements.splitlines()
        ):
            res[start].append(end)
        return res, molecule

    def replace_needle(input: str, needle: str, to: str) -> Iterator[str]:
        assert needle in input  # Sanity check
        i = input.find(needle)
        while i != -1:
            yield input[:i] + to + input[i + len(needle) :]
            i = input.find(needle, i + 1)

    def do_replacements(
        replacements: dict[str, list[str]], molecule: str
    ) -> Iterator[str]:
        for needle, vals in replacements.items():
            if needle not in molecule:
                continue
            for to in vals:
                yield from replace_needle(molecule, needle, to)

    replacements, molecule = parse(input)
    new_molecules = set(do_replacements(replacements, molecule))
    return len(new_molecules)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
