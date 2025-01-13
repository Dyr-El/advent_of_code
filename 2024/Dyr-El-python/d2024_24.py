from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque, defaultdict
from functools import cache, reduce
from itertools import combinations, count, permutations
from peek import peek


def parse_first(line):
    gate, v = line.split(': ')
    return gate, int(v)

def parse_second(line):
    g1, op, g2, _, g3 = line.split()
    return g1, op, g2, g3

def parse(inp):
    return parse_lines(inp, [parse_first, parse_second], '\n\n')

def run(regs, ops):
    iter = 0
    changed = True
    while changed:
        changed = False
        iter = iter + 1
        for r1, op, r2, r3 in ops:
            if r1 not in regs:
                regs[r1] = 0
            if r2 not in regs:
                regs[r2] = 0
            r1, r2 = regs[r1], regs[r2]
            if op == "AND":
                val = r1 & r2
            elif op == "OR":
                val = r1 | r2
            elif op == "XOR":
                val = r1 ^ r2
            else:
                print("Error", op)
            if r3 not in regs:
                regs[r3] = 0
            if val != regs[r3]:
                regs[r3] = val
                changed = True
        if iter > 10000:
            return regs
    return regs

def read_reg_bits(regs, letter):
    result = 0
    for reg, val in regs.items():
        if reg[0] != letter:
            continue
        shift = int(reg[1:])
        result = result | (val << shift)
    return result

def part1(inp):
    regs, ops = parse(inp)
    regs = {name: value for name, value in regs}
    run(regs, ops)
    return read_reg_bits(regs, 'z')

def find_ops(reg, op_map):
    if reg in op_map:
        op = op_map[reg]
        s = {(op[0], op[1], op[2], reg)}
        s |= find_ops(op[0], op_map)
        s |= find_ops(op[2], op_map)
        return s
    return set()

def find_suspect(ops, regs):
    op_map = {res_reg: (arg1_reg, op, arg2_reg) for arg1_reg, op, arg2_reg, res_reg in ops}
    marked_correct = set()
    for bits in range(45):
        for x in range(2 << bits):
            for y in range( (2 << bits) - x):
                for i in range(45):
                    regs[f"x{i:02d}"] = (x & (1 << i)) >> i
                    regs[f"y{i:02d}"] = (y & (1 << i)) >> i
                z = x + y
                run(regs, ops)
                val = read_reg_bits(regs, "z")
                if z != val:
                    print(f"Found error {x} + {y} != {val}")
                    used_ops = find_ops(f"z{bits:02d}", op_map)
                    return (used_ops - marked_correct, x, y)
        used_ops = find_ops(f"z{bits:02d}", op_map)
        marked_correct |= used_ops
    return set()

def try_swap(regs, ops, op1, op2, limit):
    for opidx, op in enumerate(ops):
        if op1 == op:
            i1 = opidx
        if op2 == op:
            i2 = opidx
    ops[i1] = (op1[0], op1[1], op1[2], op2[3])
    ops[i2] = (op2[0], op2[1], op2[2], op1[3])
    all_correct = True
    for x in range(limit):
        for y in range(limit):
            for i in range(45):
                regs[f"x{i:02d}"] = (x & (1 << i)) >> i
                regs[f"y{i:02d}"] = (y & (1 << i)) >> i
            run(regs, ops)
            z = read_reg_bits(regs, 'z')
            if z != x + y:
                all_correct = False
    if all_correct:
        print(op1[3], op2[3])
        input(">>>")
        return (op1[3], op2[3])
    ops[i1] = op1
    ops[i2] = op2

def print_rec(d, op):
    if op in d:
        print_rec(d, d[op][0])
        print_rec(d, d[op][2])
    if op in d:
        print(f"{d[op][0]} {d[op][1]} {d[op][2]} -> {d[op][3]}")
        del d[op]

def print_dep(ops):
    d = {op[3]:op for op in ops}
    count = 0
    while True:
        current = f"z{count:02d}"
        if current not in d:
            break
        print_rec(d, current)
        count += 1

def part2(inp):
    regs, ops = parse(inp)
    regs = {name: value for name, value in regs}
    # print_dep(ops)
    # input()
    for ii in range(44):
        test_i = (1 << ii )- 1
        x = test_i
        y = test_i
        expected = x + y
        for i in range(45):
            regs[f"x{i:02d}"] = (x & (1 << i)) >> i
            regs[f"y{i:02d}"] = (y & (1 << i)) >> i
        run(regs, ops)
        z = read_reg_bits(regs, "z")
        if z != expected:
            print(bin(z))
            print(bin(expected))
            print(ii, x, y)
            break


ex_inp = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""".strip()

ex2_inp = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00""".strip()


def test_1_1():
    expected = 4
    assert part1(ex_inp) == expected


def test_1_2():
    expected = "z00,z01,z02,z05"
    assert part2(ex_inp) == expected

def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))

if __name__ == "__main__":
    prep = PrepareAoc(2024, 24)
    main(prep.get_content())
