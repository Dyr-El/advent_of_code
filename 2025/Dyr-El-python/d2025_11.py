from aoc_prepare import PrepareAoc
from utils.parse import parse_lines
from utils.grid import Grid2D
from utils.vec import Vec2D
from collections import deque
from functools import reduce
import z3

test_inp_1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
test_inp_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse_line(line):
    return line.split(": ")[0], line.split(": ")[1].split()

def parse_input(inp):
    return {k: v for k, v in parse_lines(inp, parse_line)}

cache = {}
def find_paths(data, start, end, clear_cache=False):
    if clear_cache:
        cache.clear()
    if start == end:
        return 1
    if start not in data:
        return 0
    if (start, end) in cache:
        return cache[(start, end)]
    paths = 0
    for node in data[start]:
        rest_paths = find_paths(data, node, end)
        paths += rest_paths
    cache[(start, end)] = paths
    return paths

def part1(inp):
    data = parse_input(inp)
    paths = find_paths(data, "you", "out", clear_cache=True)
    return paths

def part2(inp):
    data = parse_input(inp)
    paths_from_svr_to_dac = find_paths(data, "svr", "dac", clear_cache=True)
    paths_from_dac_to_fft = find_paths(data, "dac", "fft")
    paths_from_fft_to_out = find_paths(data, "fft", "out")
    paths_from_svr_to_fft = find_paths(data, "svr", "fft")
    paths_from_fft_to_dac = find_paths(data, "fft", "dac")
    paths_from_dac_to_out = find_paths(data, "dac", "out")
    return (paths_from_svr_to_dac * paths_from_dac_to_fft * paths_from_fft_to_out +
            paths_from_svr_to_fft * paths_from_fft_to_dac * paths_from_dac_to_out)

def test_1_1():
    assert part1(test_inp_1) == 5


def test_1_2():
    assert part2(test_inp_2) == 2


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2025, 11)
    main(prep.get_content())