from aoc_prepare import PrepareAoc

test_inp_1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
test_inp_2 = test_inp_1


def parse_input(inp):
    for line in inp.splitlines():
        if line.strip()[0] == "L":
            yield -int(line.strip()[1:])
        else:
            yield int(line.strip()[1:])
    return inp

def part1(inp):
    pos = 50
    total = 0
    for move in parse_input(inp):
        pos = (move + pos) % 100
        if pos ==  0:
            total += 1
    return total


def part2(inp):
    pos = 50
    total = 0
    for move in parse_input(inp):
        if move < 0:
            for i in range(abs(move)):
                pos = (pos - 1) % 100
                if pos == 0:
                    total += 1
        elif move > 0:
            for i in range(move):
                pos = (pos + 1) % 100
                if pos == 0:
                    total += 1
    return total


def test_1_1():
    assert part1(test_inp_1) == 3


def test_1_2():
    assert part2(test_inp_2) == 6

def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2025, 1)
    main(prep.get_content())