#!/usr/bin/env python
import sys


def calc_fuel(mass: int) -> int:
    fuel = mass // 3 - 2
    return fuel + calc_fuel(fuel) if fuel > 0 else 0


def main() -> None:
    print(sum(calc_fuel(int(l)) for l in sys.stdin))


if __name__ == "__main__":
    main()
