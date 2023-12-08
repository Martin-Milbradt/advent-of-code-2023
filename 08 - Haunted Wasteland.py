from modules import DataManager
import sympy

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

test_data = test_data_string.strip().split("\n")


test_data_string_2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

test_data_2 = test_data_string_2.strip().split("\n")


test_data_string_3 = """
R

11A = (11B, 11Z)
11B = (11B, 11Z)
11Z = (11B, 11B)
22A = (22B, 22B)
22B = (22E, 22C)
22C = (22E, 22Z)
22Z = (22E, 22A)
"""

test_data_3 = test_data_string_3.strip().split("\n")

# Shared ---------------------------------------------------------------------------------------


def parse_network(input):
    network = {}
    for line in input:
        node, connections = line.split(" = ")
        left, right = connections.strip("()").split(", ")
        network[node] = (left, right)
    return network


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    network = parse_network(input[2:])
    instructions = input[0]
    return follow_instructions(instructions, network)


def follow_instructions(instructions, network):
    node = "AAA"
    steps = 0

    while node != "ZZZ":
        next_move = instructions[steps % len(instructions)]
        node = network[node][0 if next_move == "L" else 1]
        steps += 1

    return steps


# Part 2 ---------------------------------------------------------------------------------------


# This it not a general solution, it falls on its face for more general inputs.


def part2(input=data) -> int:
    network = parse_network(input[2:])
    instructions = input[0]
    return follow_instructions_multi_start(network, instructions)


def follow_instructions_multi_start(network, instructions):
    starts = [node for node in network if node.endswith("A")]
    count = len(starts)
    nodes = starts.copy()
    steps = 0
    loops = []
    journey = {node: [(node, 0)] for node in nodes}

    while len(loops) < count:
        idx = steps % len(instructions)
        steps += 1
        LR = 0 if instructions[idx] == "L" else 1
        nodes = [network[node][LR] for node in nodes]
        for start, current in zip(starts, nodes):
            if (current, idx) in journey[start]:
                loops.append(steps - journey[start].index((current, idx)))
                nodes.remove(current)
                starts.remove(start)
            journey[start].append((current, idx))

    return sympy.lcm(loops)


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data_2))
print("Part 2:", part2())
