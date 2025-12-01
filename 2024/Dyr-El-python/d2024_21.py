from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count, permutations
from peek import peek


def parse(inp: str):
    l = list()
    for s in inp.splitlines():
        s2 = int(''.join(c for c in s if c in '0123456789'))
        l.append((s, s2))
    return l

keyboard_layout_1 = """
789
456
123
#0A
""".strip()
keyboard_layout_2 = """
#^A
<v>
""".strip()

cache1 = dict()

def clear_cache():
    cache1.clear()

class Robot:
    def __init__(self, keyboard_layout, next=None):
        self._grid = Grid2D(keyboard_layout)
        self._keyb_id = id(keyboard_layout)
        self._pos = self._grid.find(lambda pos, ch: ch=="A")[0]
        self._next = next
        self._cache = dict()
        
    @property
    def pos(self):
        return self._pos
    
    def how_to_type(self, key:str, key_start):
        cache_key = (key, key_start, self._keyb_id)
        start_pos = self._grid.find(lambda _, ch: ch == key_start)[0]
        end_pos = self._grid.find(lambda _, ch: ch == key)[0]
        
        if start_pos.x == end_pos.x:
            if start_pos.y > end_pos.y:
                result = ["^" * (start_pos.y - end_pos.y) + "A"]
                cache1[cache_key] = result
                return result
            else:
                result = ["v" * (end_pos.y - start_pos.y) + "A"]
                cache1[cache_key] = result
                return result
        if start_pos.y == end_pos.y:
            if start_pos.x > end_pos.x:
                result = ["<" * (start_pos.x - end_pos.x) + "A"]
                cache1[cache_key] = result
                return result
            else:
                result = [">" * (end_pos.x - start_pos.x) + "A"]
                cache1[cache_key] = result
                return result
            
        result = list()
        horiz = list()
        p = start_pos
        delta_y, key_y = (Vec2D(0, 1), "v") if start_pos.y < end_pos.y else (Vec2D(0, -1), "^")
        delta_x, key_x = (Vec2D(1, 0), ">") if start_pos.x < end_pos.x else (Vec2D(-1, 0), "<")
        while p.y != end_pos.y:
            p = p + delta_y
            if self._grid[p] == "#":
                p = p - delta_y
                while p.x != end_pos.x:
                    p = p + delta_x
                    horiz.append(key_x)
            else:
                horiz.append(key_y)
        while p != end_pos:
            p = p + delta_x
            horiz.append(key_x)
        result.append(''.join(horiz) + "A")
        vert = list()
        p = start_pos
        while p.x != end_pos.x:
            p = p + delta_x
            if self._grid[p] == "#":
                p = p - delta_x
                while p.y != end_pos.y:
                    p = p + delta_y
                    vert.append(key_y)
            else:
                vert.append(key_x)
        while p != end_pos:
            p = p + delta_y
            vert.append(key_y)
        result.append(''.join(vert) + "A")
        cache1[cache_key] = result
        return result
    
    
    @staticmethod
    def sentences(s):
        return [ss + 'A' for ss in s.split('A')[:-1]]
    
    
    def type_sentence(self, s):
        if s in self._cache:
            return self._cache[s]
        tot = 0
        for c1, c2 in zip('A' + s, s):
            variants = self.how_to_type(c2, c1)
            find_min = 2**63
            for variant in variants:
                if self._next:
                    tot2 = sum(self._next.type_sentence(sentence)
                               for sentence in self.sentences(variant))
                else:
                    tot2 = sum(len(sentence)
                               for sentence in self.sentences(variant))
                find_min = min(find_min, tot2)
            tot += find_min
        self._cache[s] = tot
        return tot
    
    def find_shortest(self, s):
        return self.type_sentence(s)
                        
                        
def part1(inp):
    clear_cache()
    r3 = Robot(keyboard_layout_2)
    r2 = Robot(keyboard_layout_2, r3)
    r1 = Robot(keyboard_layout_1, r2)
    tot = 0
    for keys, ii in parse(inp):
        tot += (ii * r1.find_shortest(keys))
    return tot

def part2(inp):
    clear_cache()
    robots = [Robot(keyboard_layout_2)]
    for _ in range(24):
        robots.append(Robot(keyboard_layout_2, robots[-1]))
    first_robot = Robot(keyboard_layout_1, robots[-1])
    tot = 0
    for keys, ii in parse(inp):
        tot += (ii * first_robot.find_shortest(keys))
    return tot


ex_inp = """029A
980A
179A
456A
379A""".strip()


def test_1_1():
    expected = 126384
    assert part1(ex_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 21)
    main(prep.get_content())
