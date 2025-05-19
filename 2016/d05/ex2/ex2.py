#!/usr/bin/env python

import hashlib
import itertools
import sys


def solve(input: str) -> str:
    def crack_password(door_id: str) -> str:
        password = ["_"] * 8
        for i in itertools.count():
            hash = hashlib.md5((door_id + str(i)).encode()).hexdigest()
            if not hash.startswith("00000"):
                continue
            pos = hash[5]
            if pos not in ("0", "1", "2", "3", "4", "5", "6", "7"):
                continue
            if password[int(pos)] != "_":
                continue
            password[int(pos)] = hash[6]
            if all(c != "_" for c in password):
                break
        return "".join(password)

    return crack_password(input.strip())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
