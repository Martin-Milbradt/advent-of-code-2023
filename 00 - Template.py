from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
    ...
"""

test_data = test_data_string.strip().split("\n")


# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    pass


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    pass


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
