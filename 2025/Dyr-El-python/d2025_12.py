from aoc_prepare import PrepareAoc
from utils.parse import parse_lines
from utils.grid import Grid2D
from utils.vec import Vec2D
from collections import deque
from functools import reduce

test_inp_1 = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
test_inp_2 = test_inp_1


def parse_sections(sections):
    pieces = []
    for sec in sections:
        pieces.append(Grid2D(sec[3:]))
    return pieces

def parse_regions(section):
    regions = []
    for line in section.splitlines():
        parts = line.split(": ")
        size_part = parts[0]
        regions_part = parts[1]
        width, height = map(int, size_part.split("x"))
        region_indices = list(map(int, regions_part.split()))
        regions.append((width, height, region_indices))
    return regions

def parse_input(inp):
    sections = inp.split("\n\n")
    pieces = parse_sections(sections[:-1])
    regions = parse_regions(sections[-1])
    return pieces, regions

def rotate_piece(piece: Grid2D) -> Grid2D:
    new_grid = Grid2D("", xmax=piece.max_y, ymax=piece.max_x)
    for y in range(piece.max_y + 1):
        for x in range(piece.max_x + 1):
            new_grid[y, piece.max_x - x] = piece.get((x, y))
    return new_grid

def fit_piece_into_region(piece, region):
    region_width, region_height = region.max_x + 1, region.max_y + 1
    piece_width, piece_height = piece.max_x + 1, piece.max_y + 1
    # print(f"Fitting piece {piece_width}x{piece_height} into region {region_width}x{region_height}")
    for y in range(region_height - piece_height + 1):
        for x in range(region_width - piece_width + 1):
            fits = True
            for py in range(piece_height):
                for px in range(piece_width):
                    if piece[px, py] == "#" and region[x + px, y + py] == "#":
                        fits = False
                        break
                if not fits:
                    break
            if fits:
                yield Vec2D(x, y)

def places_piece_in_region(piece, region, position):
    new_region = Grid2D(str(region), xmax=region.max_x, ymax=region.max_y)
    piece_width, piece_height = piece.max_x + 1, piece.max_y + 1
    for py in range(piece_height):
        for px in range(piece_width):
            if piece[px, py] == "#":
                new_region[position.x + px, position.y + py] = "#"
    return new_region

cache = {}
def place_pieces(rotations, region, no_pieces):
    if sum(no_pieces) == 0:
        return True
    if str((region, tuple(no_pieces))) in cache:
        return cache[str((region, tuple(no_pieces)))]
    for pidx, count in enumerate(no_pieces):
        if count == 0:
            continue
        for rotated_piece in rotations[pidx]:
            for position in fit_piece_into_region(rotated_piece, region):
                new_region = places_piece_in_region(rotated_piece, region, position)
                new_no_pieces = no_pieces[:]
                new_no_pieces[pidx] -= 1
                if place_pieces(rotations, new_region, new_no_pieces):
                    cache[str((region, tuple(no_pieces)))] = True
                    return True
    cache[str((region, tuple(no_pieces)))] = False
    return False

def part1(inp):
    pieces, regions = parse_input(inp)
    rotations = dict()
    for pidx, piece in enumerate(pieces):
        rotations[pidx] = [piece]
        rotated_piece = piece
        done = set([str(piece)])
        for _ in range(3):
            rotated_piece = rotate_piece(rotated_piece)
            rotate_str = str(rotated_piece)
            if rotate_str in done:
                continue
            done.add(rotate_str)
            rotations[pidx].append(rotated_piece)
    total = 0
    for ridx, region in enumerate(regions):
        cache.clear()
        width, height, region_indices = region
        s = 0
        for idx, count in enumerate(region_indices):
            no_pixels = sum(1 for pos, ch in pieces[idx].items() if ch == "#")
            s += no_pixels * count
        if s > width * height:
            continue
        region_grid = Grid2D("", xmax=width - 1, ymax=height - 1)
        if place_pieces(rotations, region_grid, region_indices):
            print(f"Region {ridx} {width}x{height} with pieces {region_indices} can be placed")
            total += 1
        else:
            print(f"Region {ridx} {width}x{height} with pieces {region_indices} cannot be placed")
    return total

def part2(inp):
    pieces, regions = parse_input(inp)
    # print(pieces, regions)
    pass


def test_1_1():
    assert part1(test_inp_1) == 2


def test_1_2():
    assert part2(test_inp_2) == None


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2025, 12)
    main(prep.get_content())