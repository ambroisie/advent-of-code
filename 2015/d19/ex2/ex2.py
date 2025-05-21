#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def parse(input: str) -> tuple[dict[str, list[str]], str]:
        raw_replacements, molecule = input.strip().split("\n\n")
        res: dict[str, list[str]] = collections.defaultdict(list)
        for start, end in (
            line.split(" => ") for line in raw_replacements.splitlines()
        ):
            res[start].append(end)
        return res, molecule

    def inverse(input: dict[str, list[str]]) -> dict[str, str]:
        res: dict[str, str] = {}
        for key, vals in input.items():
            for val in vals:
                res[val] = key
        assert len(res) == sum(map(len, input.values()))  # Sanity check
        return res

    def build(replacements: dict[str, list[str]], molecule: str) -> int:
        # We will be "building down" to the electron, so inverse the replacement mapping
        inversed_replacements = inverse(replacements)
        # Order the replacement needles to try the longest ones first
        needles = sorted(inversed_replacements.keys(), key=len, reverse=True)
        res = 0
        while molecule != "e":
            for needle in needles:
                if needle not in molecule:
                    continue
                res += 1
                molecule = molecule.replace(needle, inversed_replacements[needle], 1)
        return res

    replacements, molecule = parse(input)
    return build(replacements, molecule)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
