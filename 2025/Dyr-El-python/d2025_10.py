from aoc_prepare import PrepareAoc
from utils.parse import parse_lines
from utils.grid import Grid2D
from utils.vec import Vec2D
from collections import deque
from functools import reduce
import z3

test_inp_1 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
test_inp_2 = test_inp_1


def parse_line(line):
    grid_part = line.split()[0][1:-1]
    rest = line.split()[1:]
    buttons = line.split()[1:-1]
    jolts = line.split()[-1]
    jolts = tuple(map(int, jolts[1:-1].split(",")))
    buttons = [tuple(map(int, b[1:-1].split(","))) for b in buttons]
    return (grid_part, buttons, jolts)

def parse_input(inp):
    data = parse_lines(inp, parse_line)
    return data


def part1(inp):
    data = parse_input(inp)
    total = 0
    for machine in data:
        best_presses = float("inf")
        grid_str, buttons, _ = machine
        width = len(grid_str)
        for i in range(2**len(buttons)):
            no_presses = 0
            grid = [False] * width
            for bi, b in enumerate(buttons):
                if (i >> bi) & 1:
                    no_presses += 1
                    for v in b:
                        grid[v] = not grid[v]
            grid_str2 = "".join("#" if cell else "." for cell in grid)
            if grid_str2 == grid_str:
                best_presses = min(best_presses, no_presses)
        total += best_presses
    return total


def part2(inp):
    data = parse_input(inp)
    total = 0
    for machine in data:
        _, buttons, jolts = machine
        vars = []
        s = z3.Optimize()
        for button_idx, button in enumerate(buttons):
            vars.append(z3.Int(f"b{button_idx}"))
            s.add(vars[-1] >= 0)
        for jolt_idx, jolt in enumerate(jolts):
            btns = [button_idx for button_idx, button in enumerate(buttons) if jolt_idx in button]
            s.add(z3.Sum([vars[btn] for btn in btns]) == jolt)
        s.minimize(z3.Sum(vars))
        s.check()
        s.model()
        total += sum(s.model()[var].as_long() for var in vars)
    return total


def test_1_1():
    assert part1(test_inp_1) == 7


def test_1_2():
    assert part2(test_inp_2) == 33


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2025, 10)
    main(prep.get_content())