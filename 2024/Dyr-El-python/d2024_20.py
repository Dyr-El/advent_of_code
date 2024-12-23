from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count
from peek import peek


def parse(inp: str):
    return Grid2D(inp)


def distance_map(grid, start, end):
    remaining = deque([start])
    distance = {start:0}
    while remaining:
        pos = remaining.popleft()
        if pos == end:
            break
        for delta in Grid2D.four_directions():
            npos = pos + delta
            if grid[npos] == "#":
                continue
            if npos in distance:
                continue
            distance[npos] = distance[pos] + 1
            remaining.append(npos)
    return distance    


def find_cheats(grid, start, end, cheat_length, threshold):
    distance = distance_map(grid, start, end)
    return sum(distance[pos2] - dist1 - (pos1 - pos2).length() >= threshold
               for pos1, dist1 in distance.items()
               for pos2 in pos1.iter_distance(cheat_length)
               if pos2 in distance)


def part1(inp, threshold):
    grid = parse(inp)
    start = grid.find(lambda _, x:x=='S')[0]
    end = grid.find(lambda _, x:x=='E')[0]
    return find_cheats(grid, start, end, 2, threshold)


def part2(inp, threshold):
    grid = parse(inp)
    start = grid.find(lambda _, x:x=='S')[0]
    end = grid.find(lambda _, x:x=='E')[0]
    return find_cheats(grid, start, end, 20, threshold)


ex_inp = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""".strip()


def test_1_1():
    expected = 5
    assert part1(ex_inp, 20) == expected


def test_1_2():
    expected = 7
    assert part2(ex_inp, 74) == expected


def main(inp):
    print("Part1:", part1(inp.strip(), 100))
    print("Part2:", part2(inp.strip(), 100))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 20)
    main(prep.get_content())
