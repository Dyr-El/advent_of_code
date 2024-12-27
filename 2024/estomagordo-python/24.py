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
    a, b = grouped_lines(lines)
    starts = {}

    for line in a:
        wire, signal = line.rstrip().split(': ')
        starts[wire] = bool(int(signal))

    gates = {}

    for line in b:
        a, operation, b, _, output = line.split()
        gates[output] = (a, operation, b)

    return starts, gates


def solve_a(lines):
    starts, gates = parse(lines)
    outputs = set()
    signals = {}

    for wire, signal in starts.items():
        if wire[0] == 'z':
            outputs.add(wire)

        signals[wire] = signal

    for output, gate in gates.items():
        a, _, b = gate

        if output[0] == 'z':
            outputs.add(output)
        if a[0] == 'z':
            outputs.add(a)
        if b[0] == 'z':
            outputs.add(b)

    while any(output not in signals for output in outputs):
        for output, gate in gates.items():
            if output in signals:
                continue

            a, operation, b = gate

            if a not in signals or b not in signals:
                continue

            aval = signals[a]
            bval = signals[b]

            signals[output] = aval&bval if operation == 'AND' else aval|bval if operation == 'OR' else aval^bval

    binary = ''

    for output in sorted(outputs, reverse=True):
        binary += str(int(signals[output]))

    return int(binary, 2)


def solve_b(lines):
    data = parse(lines)

    return None


def main():
    lines = []

    with open('24.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
