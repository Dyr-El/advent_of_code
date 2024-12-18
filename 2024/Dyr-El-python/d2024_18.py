from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count
from peek import peek


def parse_line(line):
    return [int(s) for s in line.split(',')]


def parse(inp:str):
    return parse_lines(inp, parse_line)


def find_distances(start_position, grid):
    remaining = deque([start_position])
    distance = {start_position:0}
    
    while remaining:
        position = remaining.popleft()
        for delta in Grid2D.four_directions():
            next_position = position + delta
            if grid[next_position] == "#":
                continue
            if next_position in distance:
                continue
            distance[next_position] = distance[position] + 1
            remaining.append(next_position)
    return distance
    

def part1(inp, amount=1024, xmax=70, ymax=70):
    coords = parse(inp)

    grid = Grid2D("", xmax=xmax, ymax=ymax)
    for x, y in coords[:amount]:
        grid[x,y] = "#"
    return find_distances(Vec2D(0, 0), grid)[Vec2D(xmax, ymax)]


def part2(inp, xmax=70, ymax=70):
    coords = parse(inp)
    min_time, max_time = 0, len(coords)
    reachable = set()
    unreachable = set()
    end_position = Vec2D(xmax, ymax)
    while True:
        time = (max_time + min_time) // 2
        grid = Grid2D("", xmax=xmax, ymax=ymax)
        for x, y in coords[:time]:
            grid[x,y] = "#"
        distance = find_distances(Vec2D(0, 0), grid)
        
        if end_position not in distance:
            if (time - 1) in reachable:
                return ','.join(map(str, coords[time - 1]))
            unreachable.add(time)
            max_time = time
        else:
            if (time + 1) in unreachable:
                return ','.join(map(str, coords[time]))
            reachable.add(time)
            min_time = time


ex_inp = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".strip()

# ex2_inp = """Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,3,5,4,3,0"""

def test_1_1():
    expected = 22
    assert part1(ex_inp, amount=12, xmax=6, ymax=6) == expected


def test_1_2():
    expected = "6,1"
    assert part2(ex_inp, xmax=6, ymax=6) == expected



def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 18)
    main(prep.get_content())
