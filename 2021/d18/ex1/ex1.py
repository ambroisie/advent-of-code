#!/usr/bin/env python

import functools
import itertools
import sys
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple


@dataclass
class Tree:
    parent: Optional["Pair"]


@dataclass
class Pair(Tree):
    left: Tree
    right: Tree


@dataclass
class Num(Tree):
    val: int


# True means left, False means right
Path = List[bool]


def solve(input: List[str]) -> int:
    def make_pair(left: Tree, right: Tree, parent: Optional[Pair] = None) -> Pair:
        pair = Pair(parent=parent, left=left, right=right)
        pair.left.parent = pair
        pair.right.parent = pair
        return pair

    def make_num(val: int, parent: Optional[Pair] = None) -> Num:
        return Num(parent=parent, val=val)

    # FIXME: remove this
    def debug(tree: Tree) -> str:
        if isinstance(tree, Pair):
            return f"[{debug(tree.left)},{debug(tree.right)}]"
        assert isinstance(tree, Num)
        return str(tree.val)

    def parse() -> List[Tree]:
        def parse_snailfish_number(line: str) -> Tree:
            def parse_index(input: str, index: int = 0) -> Tuple[int, Tree]:
                if input[index] == "[":
                    left_index, left = parse_index(input, index + 1)
                    assert input[left_index] == ","  # Sanity check
                    right_index, right = parse_index(input, left_index + 1)
                    assert input[right_index] == "]"  # Sanity check
                    return right_index + 1, make_pair(left, right)
                res = 0
                for i in itertools.count(index):
                    if i < len(input) and input[i] in set(str(i) for i in range(10)):
                        res = res * 10 + int(input[i])
                    else:
                        return i, make_num(res)
                assert False  # Sanity check

            __, res = parse_index(line)
            return res

        return [parse_snailfish_number(line) for line in input]

    def explosion_path(number: Tree) -> Optional[Path]:
        def dfs(number: Pair, path: Path = []) -> Optional[Path]:
            if (
                len(path) >= 4
                and isinstance(number.left, Num)
                and isinstance(number.right, Num)
            ):
                return path
            if isinstance(number.left, Pair):
                left_path = dfs(number.left, path + [True])
                if left_path is not None:
                    return left_path
            if isinstance(number.right, Pair):
                right_path = dfs(number.right, path + [False])
                if right_path is not None:
                    return right_path
            return None

        assert isinstance(number, Pair)  # Sanity check
        return dfs(number)

    def split_path(number: Tree) -> Optional[Path]:
        def dfs(number: Pair, path: Path = []) -> Optional[Path]:
            if isinstance(number.left, Num):
                if number.left.val >= 10:
                    return path + [True]
            else:
                assert isinstance(number.left, Pair)  # Sanity check
                if (left_path := dfs(number.left, path + [True])) is not None:
                    return left_path
            if isinstance(number.right, Num):
                if number.right.val >= 10:
                    return path + [False]
            else:
                assert isinstance(number.right, Pair)  # Sanity check
                if (right_path := dfs(number.right, path + [False])) is not None:
                    return right_path
            return None

        assert isinstance(number, Pair)  # Sanity check
        return dfs(number)

    def explode(number: Tree, path: Path) -> Tree:
        def walk(number: Tree, reverse: bool) -> Iterator[Tree]:
            if isinstance(number, Num):
                yield number
            else:
                assert isinstance(number, Pair)  # Sanity check
                first, second = (
                    (number.right, number.left)
                    if reverse
                    else (number.left, number.right)
                )
                yield from walk(first, reverse)
                yield number
                yield from walk(second, reverse)

        def next_num(number: Tree, reverse: bool) -> Optional[Num]:
            if number.parent is None:
                return None
            sibling = number.parent.left if reverse else number.parent.right
            if number is sibling:
                return next_num(number.parent, reverse)
            for node in walk(sibling, reverse=reverse):
                if isinstance(node, Num):
                    return node
            return None

        assert isinstance(number, Pair)  # Sanity check

        if len(path) == 0:
            p, n = next_num(number, reverse=True), next_num(number, reverse=False)
            if p is not None:
                assert isinstance(number.left, Num)  # Safety check
                p.val += number.left.val
            if n is not None:
                assert isinstance(number.right, Num)  # Safety check
                n.val += number.right.val
            return make_num(0)

        parent, left, right = number.parent, number.left, number.right
        if path[0]:
            left = explode(number.left, path[1:])
        else:
            right = explode(number.right, path[1:])

        return make_pair(parent=parent, left=left, right=right)

    def split(number: Tree, path: Path) -> Tree:
        def split_int(num: int, parent: Optional[Pair]) -> Tree:
            assert num >= 0  # Sanity check
            left = num // 2
            right = num - left
            res = make_pair(left=make_num(left), right=make_num(right), parent=parent)
            return res

        if len(path) == 0:
            assert isinstance(number, Num)  # Sanity check
            return split_int(number.val, number.parent)

        assert isinstance(number, Pair)  # Sanity check

        parent, left, right = number.parent, number.left, number.right
        if path[0]:
            left = split(number.left, path[1:])
        else:
            right = split(number.right, path[1:])

        return make_pair(parent=parent, left=left, right=right)

    def reduce(number: Tree) -> Tree:
        path = explosion_path(number)
        if path is not None:
            return reduce(explode(number, path))
        path = split_path(number)
        if path is not None:
            return reduce(split(number, path))
        return number

    def add(left: Tree, right: Tree) -> Tree:
        return reduce(make_pair(left=left, right=right))

    def magnitude(number: Tree) -> int:
        if isinstance(number, Num):
            return number.val
        assert isinstance(number, Pair)  # Safety check
        return 3 * magnitude(number.left) + 2 * magnitude(number.right)

    numbers = parse()
    result = functools.reduce(add, numbers)
    return magnitude(result)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
