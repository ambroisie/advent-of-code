#!/usr/bin/env python
import functools
import itertools
import operator
import sys


def main() -> None:
    values = [int(n) for n in sys.stdin.readlines()]
    for tup in itertools.combinations(values, 2):
        if sum(tup) == 2020:
            print(functools.reduce(operator.mul, tup))
            break


if __name__ == "__main__":
    main()
