#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def has_abba(input: str) -> bool:
        for i in range(4, len(input) + 1):
            a, b, c, d = (input[i - j] for j in range(4, 0, -1))
            if a == b:
                continue
            if a != d:
                continue
            if b != c:
                continue
            return True
        return False

    def supports_tls(address: str) -> bool:
        abba_found = False
        is_hypernet = False
        i = 0
        while i < len(address):
            if is_hypernet:
                j = address.find("]", i)
            else:
                j = address.find("[", i)
            if j == -1:
                j = len(address)
            if has_abba(address[i:j]):
                if is_hypernet:
                    return False
                abba_found = True
            i = j
            is_hypernet = not is_hypernet
        return abba_found

    return sum(map(supports_tls, input.splitlines()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
