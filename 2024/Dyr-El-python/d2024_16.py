from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations
from icecream import ic
from peek import peek


def parse(inp:str):
    return Grid2D(inp)


def part1(inp):
    grid = parse(inp)
    start_pos = grid.find(lambda _, x: x=="S")[0]
    end_pos = grid.find(lambda _, x: x=="E")[0]
    direction = Vec2D(1, 0)
    rem = deque([(start_pos, direction)])
    cost = {((start_pos, direction)): 0}
    while rem:
        p, d = rem.popleft()
        np = p + d
        if grid.get(np, "#") != "#":
            if cost.get((np, d), 1000_000) > cost[(p, d)] + 1:
                rem.append((np, d))
                cost[(np, d)] = cost[(p, d)] + 1
        nd = d << 1
        if cost.get((p, nd), 1000_000) > cost[(p, d)] + 1000:
            rem.append((p, nd))
            cost[(p, nd)] = cost[(p, d)] + 1000
        nd = d >> 1
        if cost.get((p, nd), 1000_000) > cost[(p, d)] + 1000:
            rem.append((p, nd))
            cost[(p, nd)] = cost[(p, d)] + 1000
    return min((cost[end_pos, d] for d in Grid2D.four_directions()))


def track_back(p, d, wb, cost):
    s = set()
    for np, nd in wb.get((p, d), list()):
        s.add(np)
        s = s | track_back(np, nd, wb, cost)
    return s


def part2(inp):
    grid = parse(inp)
    start_pos = grid.find(lambda _, x: x=="S")[0]
    end_pos = grid.find(lambda _, x: x=="E")[0]
    direction = Vec2D(1, 0)
    rem = deque([(start_pos, direction)])
    cost = {((start_pos, direction)): 0}
    way_back = {(start_pos, direction): set()}
    visited = {start_pos, end_pos}
    while rem:
        p, d = rem.popleft()
        np = p + d
        if grid.get(np, "#") != "#":
            if cost.get((np, d), 1000_000) >= cost[(p, d)] + 1:
                if cost.get((np, d), 1000_000) > cost[(p, d)] + 1:
                    rem.append((np, d))
                    cost[(np, d)] = cost[(p, d)] + 1
                    way_back[np, d] = set()
                if (np, d) not in way_back:
                    way_back[np, d] = set()
                way_back[np, d].add((p, d))
        nd = d << 1
        if cost.get((p, nd), 1000_000) >= cost[(p, d)] + 1000:
            if cost.get((p, nd), 1000_000) > cost[(p, d)] + 1000:
                rem.append((p, nd))
                cost[(p, nd)] = cost[(p, d)] + 1000
                way_back[p, nd] = set()
            if (p, nd) not in way_back:
                way_back[p, nd] = set()
            way_back[p, nd].add((p, d))
        nd = d >> 1
        if cost.get((p, nd), 1000_000) >= cost[(p, d)] + 1000:
            if cost.get((p, nd), 1000_000) > cost[(p, d)] + 1000:
                rem.append((p, nd))
                cost[(p, nd)] = cost[(p, d)] + 1000
                way_back[p, nd] = set()
            if (p, nd) not in way_back:
                way_back[p, nd] = set()
            way_back[p, nd].add((p, d))
    for ep, ed in ((end_pos, d) for d in Grid2D.four_directions()):
        visited = visited | track_back(ep, ed, way_back, cost)
    return len(visited)


ex_inp = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".strip()

def test_1_1():
    expected = 7036
    assert part1(ex_inp) == expected


def test_1_2():
    expected = None
    assert part2(ex_inp) == expected


def main(inp):
    with peek():
        print("Part1:", part1(inp.strip()))
    with peek():
        print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 16)
    main(prep.get_content())
