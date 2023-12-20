#!/usr/bin/env python

import enum
import itertools
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

    def count_buttons(modules: Modules) -> int:
        def count_buttons_for(
            wanted_src: str,
            wanted_dst: str,
            pulse_wanted: Pulse,
        ) -> int:
            inputs = compute_inputs(modules)
            last_pulse: dict[str, Pulse] = defaultdict(lambda: Pulse.LOW)

            for i in itertools.count(start=1):
                queue: deque[tuple[Pulse, str]] = deque([(Pulse.LOW, "broadcaster")])

                while queue:
                    pulse, name = queue.popleft()

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
                                last_pulse[input] == Pulse.HIGH
                                for input in inputs[name]
                            )
                            new_pulse = Pulse.LOW if high_inputs else Pulse.HIGH
                        case ModuleType.BROADCAST:
                            new_pulse = pulse

                    last_pulse[name] = new_pulse
                    for dst in mod.destinations:
                        queue.append((new_pulse, dst))
                        # We found the pulse we wanted, report the number of button presses
                        if (
                            new_pulse == pulse_wanted
                            and name == wanted_src
                            and dst == wanted_dst
                        ):
                            return i

            assert False  # Sanity check

        inputs = compute_inputs(modules)
        # The input has a single conjunction leading to "rx"
        # So we want to compute when all of *its* inputs are high at the same time
        assert len(inputs["rx"]) == 1  # Sanity check
        rx_input = inputs["rx"][0]
        assert modules[rx_input].module_type == ModuleType.CONJUNCTION  # Sanity check
        # Shortcut: assume that the high pulse output is cyclic
        return math.lcm(
            *(count_buttons_for(mod, rx_input, Pulse.HIGH) for mod in inputs[rx_input])
        )

    modules = parse(input)
    return count_buttons(modules)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
