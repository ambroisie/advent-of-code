#!/usr/bin/env python

from typing import Iterator


def is_valid_password(p: int) -> bool:
    digits = str(p)

    def has_unique_adjacent_digit():
        counts = {d: 0 for d in range(10)}
        for a, b in zip(digits, digits[1:]):
            if a == b:
                counts[int(a)] += 1
        return any(count == 1 for count in counts.values())

    def digits_never_decrease():
        return all(a == b for a, b in zip(sorted(digits), digits))

    return has_unique_adjacent_digit() and digits_never_decrease()


def compute_pass(begin: int, end: int) -> Iterator[int]:
    for p in range(begin, end + 1):
        if is_valid_password(p):
            yield p


def main() -> None:
    begin = 264793
    end = 803935
    print(sum(1 for p in compute_pass(begin, end)))


if __name__ == "__main__":
    main()
