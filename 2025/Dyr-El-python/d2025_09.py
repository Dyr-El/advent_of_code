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
    red_tiles = parse_input(inp)
    
    edges = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        edges.append(((x1, y1), (x2, y2)))
    
    vertical_edges = []
    horizontal_edges = []
    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:
            vertical_edges.append((x1, min(y1, y2), max(y1, y2)))
        else:
            horizontal_edges.append((min(x1, x2), max(x1, x2), y1))
    
    def is_inside(x, y):
        """Check if point (x, y) is inside the polygon using ray casting."""
        crossings = 0
        for edge_x, edge_y_min, edge_y_max in vertical_edges:
            if edge_x > x and edge_y_min <= y < edge_y_max:
                crossings += 1
        return crossings % 2 == 1
    
    def rect_fully_inside(rx1, ry1, rx2, ry2):
        # All corners inside or on boundary?
        for x, y in [(rx1, ry1), (rx1, ry2), (rx2, ry1), (rx2, ry2)]:
            if not is_inside(x, y):
                on_boundary = False
                for edge_x, edge_y_min, edge_y_max in vertical_edges:
                    if edge_x == x and edge_y_min <= y <= edge_y_max:
                        on_boundary = True
                        break
                if not on_boundary:
                    for edge_x_min, edge_x_max, edge_y in horizontal_edges:
                        if edge_y == y and edge_x_min <= x <= edge_x_max:
                            on_boundary = True
                            break
                if not on_boundary:
                    return False
        
        # No vertical edges cross interior?
        for edge_x, edge_y_min, edge_y_max in vertical_edges:
            if rx1 < edge_x < rx2:
                if edge_y_min < ry2 and edge_y_max > ry1:
                    return False
        
        # No horizonal edges cross interior?
        for edge_x_min, edge_x_max, edge_y in horizontal_edges:
            if ry1 < edge_y < ry2:
                if edge_x_min < rx2 and edge_x_max > rx1:
                    return False
        
        return True
    largest = 0
    
    for i, (x1, y1) in enumerate(red_tiles):
        for j, (x2, y2) in enumerate(red_tiles):
            if i >= j:
                continue
            rx1, rx2 = sorted((x1, x2))
            ry1, ry2 = sorted((y1, y2))
            area = (rx2 - rx1 + 1) * (ry2 - ry1 + 1)
            if area <= largest:
                continue
            if rect_fully_inside(rx1, ry1, rx2, ry2):
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