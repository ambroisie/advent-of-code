#!/usr/bin/env python

import enum
import math
import sys
from collections import defaultdict, deque
from typing import NamedTuple


class ModuleType(enum.StrEnum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCAST = "broadcaster"


class Pulse(enum.IntEnum):
    LOW = 0
    HIGH = 1


class Rule(NamedTuple):
    module_type: ModuleType
    destinations: list[str]


Modules = dict[str, Rule]


def solve(input: list[str]) -> int:
    def parse_rule(line: str) -> tuple[str, Rule]:
        module, outputs = line.split(" -> ")

        name: str
        module_type: ModuleType

        if module != "broadcaster":
            name = module[1:]
            module_type = ModuleType(module[0])
        else:
            name = module
            module_type = ModuleType(module)

        return name, Rule(module_type, outputs.split(", "))

    def parse(input: list[str]) -> Modules:
        return dict(map(parse_rule, input))

    def compute_inputs(modules: Modules) -> dict[str, list[str]]:
        inputs: dict[str, list[str]] = defaultdict(list)

        for src, rule in modules.items():
            for dst in rule.destinations:
                inputs[dst].append(src)

        return inputs

    def count_pulses(modules: Modules, button_pushes: int) -> tuple[int, int]:
        inputs = compute_inputs(modules)
        total_pulses = {pulse: 0 for pulse in Pulse}
        last_pulse: dict[str, Pulse] = defaultdict(lambda: Pulse.LOW)

        for _ in range(button_pushes):
            queue: deque[tuple[Pulse, str]] = deque([(Pulse.LOW, "broadcaster")])

            while queue:
                pulse, name = queue.popleft()
                total_pulses[pulse] += 1
                mod = modules.get(name)

                # This is for unknown outputs
                if mod is None:
                    continue

                new_pulse: Pulse
                match mod.module_type:
                    case ModuleType.FLIP_FLOP:
                        if pulse == Pulse.HIGH:
                            continue
                        new_pulse = Pulse(1 - last_pulse[name])
                    case ModuleType.CONJUNCTION:
                        high_inputs = all(
                            last_pulse[input] == Pulse.HIGH for input in inputs[name]
                        )
                        new_pulse = Pulse.LOW if high_inputs else Pulse.HIGH
                    case ModuleType.BROADCAST:
                        new_pulse = pulse

                last_pulse[name] = new_pulse
                for dst in mod.destinations:
                    queue.append((new_pulse, dst))

        return total_pulses[Pulse.LOW], total_pulses[Pulse.HIGH]

    modules = parse(input)
    return math.prod(count_pulses(modules, 1000))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
