from aoc_prepare import PrepareAoc
from utils import parse_lines, Grid2D, Vec2D
from collections import namedtuple, deque
from functools import cache, reduce
from itertools import combinations, count
from peek import peek


def parse_register(line):
    reg, _, val = line.partition(": ")
    reg = reg[-1]
    val = int(val)
    return (reg, val)


def parse_instructions(line):
    return [int(s) for s in line[9:].split(",")]


def parse(inp: str):
    return parse_lines(inp, [parse_register, parse_instructions], "\n\n")


def adv(computer, operand):
    computer.A = computer.A // (2 ** computer.combo(operand))
    computer.ip = computer.ip + 2


def bxl(computer, operand):
    computer.B = computer.B ^ operand
    computer.ip = computer.ip + 2


def bst(computer, operand):
    computer.B = computer.combo(operand) % 8
    computer.ip = computer.ip + 2


def jnz(computer, operand):
    computer.ip = operand if computer.A != 0 else computer.ip + 2


def bxc(computer, _):
    computer.B = computer.B ^ computer.C
    computer.ip = computer.ip + 2


def out(computer, operand):
    computer.out_buffer.append(computer.combo(operand) % 8)
    computer.ip = computer.ip + 2


def bdv(computer, operand):
    computer.B = computer.A // (2 ** computer.combo(operand))
    computer.ip = computer.ip + 2


def cdv(computer, operand):
    computer.C = computer.A // (2 ** computer.combo(operand))
    computer.ip = computer.ip + 2


INSTRUCTION_SET = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


class Computer:

    def __init__(self, registers, instructions):
        self._registers = dict(registers)
        self._instructions = instructions
        self._ip = 0
        self._out_buffer = []

    def reset(self, **kw):
        self.A = kw["A"] if "A" in kw else 0
        self.B = kw["B"] if "B" in kw else 0
        self.B = kw["C"] if "C" in kw else 0
        self.ip = kw["ip"] if "ip" in kw else 0
        self._out_buffer.clear()

    @property
    def A(self):
        return self._registers["A"]

    @A.setter
    def A(self, value):
        self._registers["A"] = value

    @property
    def B(self):
        return self._registers["B"]

    @B.setter
    def B(self, value):
        self._registers["B"] = value

    @property
    def C(self):
        return self._registers["C"]

    @C.setter
    def C(self, value):
        self._registers["C"] = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def out_buffer(self):
        return self._out_buffer

    def fetch(self):
        return self._instructions[self.ip : self.ip + 2]

    def combo(self, operand):
        return [0, 1, 2, 3, self.A, self.B, self.C][operand]

    def step(self):
        instruction, operand = self.fetch()
        INSTRUCTION_SET[instruction](self, operand)

    def ready(self):
        return 0 <= self.ip < len(self._instructions)

    def __str__(self):
        return f"Computer(A={self.A}, B={self.B}, C={self.C}, ip={self.ip}, out={self.out_buffer})"

    def __repr__(self):
        return f"Computer(A={self.A}, B={self.B}, C={self.C}, ip={self.ip}, out={self.out_buffer})"


def part1(inp):
    registers, instructions = parse(inp)
    computer = Computer(registers, instructions[0])
    while computer.ready():
        computer.step()
    return ",".join(map(str, computer.out_buffer))


def find_lowest_a(goal, computer, start_a=0):
    for i in range(8):
        a = start_a << 3 | i
        if a == 0:
            continue
        computer.reset(A=a)
        while computer.ready():
            computer.step()
        result = computer.out_buffer
        if result == goal:
            return a
        elif result == goal[-len(result) :]:
            attempt = find_lowest_a(goal, computer, a)
            if attempt:
                return attempt
    return None


def part2(inp):
    registers, instructions = parse(inp)
    computer = Computer(registers, instructions[0])
    return find_lowest_a(instructions[0], computer)


ex_inp = """Register A: 729 
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".strip()

ex2_inp = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def test_1_1():
    expected = "4,6,3,5,6,3,5,2,1,0"
    assert part1(ex_inp) == expected


def test_1_2():
    expected = 117440
    assert part2(ex2_inp) == expected


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2024, 17)
    main(prep.get_content())
