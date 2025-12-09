from aoc_prepare import PrepareAoc
from utils.parse import parse_lines
from utils.grid import Grid2D
from utils.vec import Vec2D
from collections import deque
from functools import reduce

test_inp_1 = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
test_inp_2 = test_inp_1


def parse_input(inp):
    data = [tuple(map(int, line.split(","))) for line in inp.splitlines()]
    return data



def part1(inp):
    rects = parse_input(inp)
    largest = 0
    for x1, y1 in rects:
        for x2, y2 in rects:
            area = abs(x2 - x1 + 1) * abs(y2 - y1 + 1)
            if area > largest:
                largest = area
    return largest


def part2(inp):
    rects = parse_input(inp)
    find_circuit = dict()
    while rects:
        x1, y1 = rects.pop(0)
        for x2, y2 in rects:
            if x1 == x2 or y1 == y2:
                find_circuit[x1, y1] = (x2, y2)
                break
    rects = parse_input(inp)
    largest = 0
    print("Find circuit lines:", find_circuit)
    print("Rects to check:", rects)
    for x1, y1 in rects:
        for x2, y2 in rects:
            rx1, rx2 = sorted((x1, x2))
            ry1, ry2 = sorted((y1, y2))
            broken = False
            for line_start, line_end in find_circuit.items():
                lx1, lx2 = sorted((line_start[0], line_end[0]))
                ly1, ly2 = sorted((line_start[1], line_end[1]))
                if lx1 == lx2: # vertical line
                    if rx1 < lx1 < rx2: # line is within x bounds
                        if ry1 < ly2 and ry2 > ly1: 
                            broken = True
                            break
                else: # horizontal line
                    if ry1 < ly1 < ry2: # line is within y bounds
                        if lx1 < rx2 and lx2 > rx1:
                            broken = True
                            break
            if broken:
                continue
            area = abs(x2 - x1 + 1) * abs(y2 - y1 + 1)
            if area > largest:
                largest = area
    return largest

def test_1_1():
    assert part1(test_inp_1) == 50


def test_1_2():
    assert part2(test_inp_2) == 24


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2025, 9)
    main(prep.get_content())