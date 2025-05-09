#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[list[str]]:
        return [line.split() for line in input.splitlines()]

    def validate_passphrase(passphrase: list[str]) -> bool:
        return len(set("".join(sorted(w)) for w in passphrase)) == len(passphrase)

    passphrases = parse(input)
    return sum(map(validate_passphrase, passphrases))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
