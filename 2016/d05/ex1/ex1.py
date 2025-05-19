#!/usr/bin/env python

import hashlib
import itertools
import sys


def solve(input: str) -> str:
    def crack_password(door_id: str) -> str:
        password: list[str] = []
        for i in itertools.count():
            hash = hashlib.md5((door_id + str(i)).encode()).hexdigest()
            if not hash.startswith("00000"):
                continue
            password.append(hash[5])
            if len(password) == 8:
                break
        return "".join(password)

    return crack_password(input.strip())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
