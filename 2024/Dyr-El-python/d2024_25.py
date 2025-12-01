from aoc_prepare import PrepareAoc
from utils import Grid2D


def parse(inp):
    schematics = [Grid2D(part) for part in inp.split("\n\n")]
    locks = [
        schematic
        for schematic in schematics
        if all(schematic[x, 0] == "#" for x in range(schematic.max_x + 1))
    ]
    keys = [
        schematic
        for schematic in schematics
        if all(schematic[x, schematic.max_y] == "#" for x in range(schematic.max_x + 1))
    ]
    return locks, keys


def part1(inp):
    locks, keys = parse(inp)
    return sum(
        all(key[pos] != "#" for pos in lock.find("#")) for lock in locks for key in keys
    )


def part2(inp):
    parse(inp)


ex_inp = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""".strip()

ex2_inp = """None""".strip()


def test_1_1():
    expected = 3
    assert part1(ex_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 25)
    main(prep.get_content())
