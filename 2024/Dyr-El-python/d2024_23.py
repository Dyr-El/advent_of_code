from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque, defaultdict
from functools import cache, reduce
from itertools import combinations, count, permutations
from peek import peek


def parse(inp):
    result = defaultdict(lambda:set())
    for line in inp.splitlines():
        a, _, b = line.partition("-")
        result[a].add(b)
        result[b].add(a)
    return result


def part1(inp):
    relations = parse(inp)
    groups_of_3 = set()
    for a_comp in relations:
        for b_comp in relations[a_comp]:
            for computer in relations[b_comp]:
                if a_comp in relations[computer]:
                    groups_of_3.add(frozenset([a_comp, b_comp, computer]))
    beginning_with_t = set()
    for computer in relations:
        if computer[0] == "t":
            beginning_with_t.add(computer)
    total = 0
    for group in groups_of_3:
        if len(beginning_with_t & group) > 0:
            total += 1
    return total


cache = {}
def build_lp(lan_party, remaining_comps, relations):
    cachekey = (frozenset(lan_party), frozenset(remaining_comps))
    if cachekey in cache:
        return cache[cachekey]
    if len(remaining_comps) == 0:
        return lan_party
    largest_size = len(lan_party)
    largest_lan_party = lan_party
    for computer in remaining_comps:
        if relations[computer] & lan_party == lan_party:
            nxt = build_lp(lan_party | {computer}, remaining_comps - {computer}, relations)
            if len(nxt) > largest_size:
                largest_lan_party = nxt
                largest_size = len(nxt)
    cache[cachekey] = largest_lan_party
    return largest_lan_party


def part2(inp):
    relations = parse(inp)
    largest_size = 0
    largest_lan_party = None
    for computer, neighbours in relations.items():
        result = build_lp({computer}, neighbours, relations)
        if len(result) > largest_size:
            largest_lan_party = result
            largest_size = len(result)
    return ",".join(sorted(largest_lan_party))


ex_inp = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""".strip()


def test_1_1():
    expected = 7
    assert part1(ex_inp) == expected


def test_1_2():
    expected = "co,de,ka,ta"
    assert part2(ex_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 23)
    main(prep.get_content())
