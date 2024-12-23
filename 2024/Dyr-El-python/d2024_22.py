from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count, permutations
from peek import peek


def parse(inp: str):
    return [int(s) for s in inp.splitlines()]


def step1(n: int) -> int:
    return ((n * 64) ^ n) % 16777216

def step2(n: int) -> int:
    return ((n // 32) ^ n) % 16777216

def step3(n: int) -> int:
    return ((n * 2048) ^ n) % 16777216

def steps(n: int) -> int:
    n = step1(n)
    n = step2(n)
    n = step3(n)
    return n

def part1(inp):
    l = parse(inp)
    tot = 0
    for secret in l:
        for i in range(2000):
            secret = steps(secret)
        tot += secret
    return tot


def part2(inp):
    l = parse(inp)
    tot = 0
    d = {}
    for secret in l:
        seq = [secret % 10]
        for i in range(2000):
            secret = steps(secret)
            seq.append(secret % 10)
        dd = {}
        for i1, i2, i3, i4, i5 in zip(seq, seq[1:], seq[2:], seq[3:], seq[4:]):
            key = (i2-i1, i3-i2, i4-i3, i5-i4)
            if key not in dd:
                dd[key] = list()
            dd[key].append(i5)
        for k, v in dd.items():
            d[k] = d.get(k, 0) + v[0]
    return max(d.values())


ex_inp = """1
10
100
2024""".strip()

ex2_inp = """1
2
3
2024""".strip()


def test_1_1():
    expected = 37327623
    assert part1(ex_inp) == expected


def test_1_2():
    expected = 23
    assert part2(ex2_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 22)
    main(prep.get_content())
