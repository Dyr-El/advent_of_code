from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count
from peek import peek


def parse_towel_patterns(line):
    return [s for s in line.split(", ")]


def parse_designs(line):
    return line


def parse(inp: str):
    return parse_lines(inp, [parse_towel_patterns, parse_designs], "\n\n")


def is_possible(patterns, goal):
    if goal == "":
        return True
    for pattern in patterns:
        if goal.startswith(pattern):
            if is_possible(patterns, goal[len(pattern) :]):
                return True
    return False


def part1(inp):
    patterns, designs = parse(inp)
    patterns = patterns[0]
    return sum(is_possible(patterns, design) for design in designs)


@cache
def number_of_ways(patterns, design):
    return (
        1
        if design == ""
        else sum(
            number_of_ways(patterns, design[len(pattern) :])
            for pattern in patterns
            if design.startswith(pattern)
        )
    )


def part2(inp):
    patterns, designs = parse(inp)
    patterns = tuple(patterns[0])
    return sum(number_of_ways(patterns, design) for design in designs)


ex_inp = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".strip()


def test_1_1():
    expected = 6
    assert part1(ex_inp) == expected


def test_1_2():
    expected = 16
    assert part2(ex_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 19)
    main(prep.get_content())
