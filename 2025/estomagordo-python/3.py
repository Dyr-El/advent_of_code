from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import DIRECTIONS, EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, find_in_grid, forward_rays_with_diagonals, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, solve_system, words


def parse(lines):
    return [ints(' '.join(list(line.rstrip()))) for line in lines]


def make_num(digits):
    return int(''.join(str(digit) for digit in digits))


def extract_max(bank, needed):
    n = len(bank)

    @cache
    def solve(digits, pos):
        if len(digits) == needed:
            return make_num(digits)
        
        if pos == n:
            return -1
        
        skip = solve(digits, pos+1)

        l = list(digits) + [bank[pos]]

        take = solve(tuple(l), pos+1)

        return max(skip, take)
    
    return solve(tuple(), 0)
    

def solve_a(lines):
    banks = parse(lines)

    return sum(extract_max(bank, 2) for bank in banks)


def solve_b(lines):
    banks = parse(lines)

    return sum(extract_max(bank, 12) for bank in banks)


def main():
    lines = []

    with open('3.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
