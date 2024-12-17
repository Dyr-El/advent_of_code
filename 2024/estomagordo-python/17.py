from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm, log

from algo import a_star, custsort, merge_ranges, sssp
from constants import DIRECTIONS, EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, find_in_grid, forward_rays_with_diagonals, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, solve_system, words


def parse(lines):
    registers, program = grouped_lines(lines)
    a = ints(registers[0])[0]
    b = ints(registers[1])[0]
    c = ints(registers[2])[0]
    code = ints(program[0])

    return a, b, c, code
    

def solve_a(lines):
    a, b, c, code = parse(lines)
    n = len(code)
    out = []
    pointer = 0

    def combo(val):
        match val:
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                return val
        
    while 0 <= pointer < n:
        opcode = code[pointer]
        operand = code[pointer+1]
        move_pointer = True

        match opcode:
            case 0:
                a //= 2**combo(operand)
            case 1:
                b ^= operand
            case 2:
                b = combo(operand)%8
            case 3:
                if a != 0:
                    pointer = operand
                    move_pointer = False
            case 4:
                b ^= c
            case 5:
                out.append(combo(operand)%8)
            case 6:
                b = a // 2**combo(operand)
            case 7:
                c = a // 2**combo(operand)

        if move_pointer:
            pointer += 2
            
    return ','.join(str(val) for val in out)


def solve_b(lines):
    _, bb, cc, code = parse(lines)
    n = len(code)
            
    def run(a, b, c):
        out = []
        pointer = 0

        def combo(val):
            match val:
                case 4:
                    return a
                case 5:
                    return b
                case 6:
                    return c
                case _:
                    return val

        while 0 <= pointer < n:
            opcode = code[pointer]
            operand = code[pointer+1]
            move_pointer = True

            match opcode:
                case 0:
                    a //= 2**combo(operand)
                case 1:
                    b ^= operand
                case 2:
                    b = combo(operand)%8
                case 3:
                    if a != 0:
                        pointer = operand
                        move_pointer = False
                case 4:
                    b ^= c
                case 5:
                    out.append(combo(operand)%8)
                    if out != code[:len(out)]:
                        return out
                case 6:
                    b = a // 2**combo(operand)
                case 7:
                    c = a // 2**combo(operand)

            if move_pointer:
                pointer += 2

        return out
    
    a = 8**(len(code)-1)

    while True:
        output = run(a, bb, cc)

        if output == code:
            return a
        
        a += 1

        if a % 10000000 == 0:
            print(a, log(a, 8), len(output), len(code))


def main():
    lines = []

    with open('17.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# 4,4,2,6,5,4,3,1,7 awrong