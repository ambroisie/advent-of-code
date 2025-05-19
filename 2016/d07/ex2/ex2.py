#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def iter_aba(input: str) -> Iterator[tuple[str, str]]:
        for i in range(3, len(input) + 1):
            a, b, c = (input[i - j] for j in range(3, 0, -1))
            if a == b:
                continue
            if a != c:
                continue
            yield a, b

    def split_address(address) -> tuple[list[str], list[str]]:
        nets: tuple[list[str], list[str]] = [], []
        i = 0
        is_hypernet = False
        while i < len(address):
            if is_hypernet:
                j = address.find("]", i)
            else:
                j = address.find("[", i)
            if j == -1:
                j = len(address)
            nets[is_hypernet].append(address[i:j])
            i = j
            is_hypernet = not is_hypernet
        return nets

    def supports_ssl(address: str) -> bool:
        supernets, hypernets = split_address(address)
        aba_candidates = itertools.chain.from_iterable(map(iter_aba, supernets))
        for a, b in aba_candidates:
            bab = b + a + b
            if any(bab in net for net in hypernets):
                return True
        return False

    return sum(map(supports_ssl, input.splitlines()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
