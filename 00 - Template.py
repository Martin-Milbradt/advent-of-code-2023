from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
    ...
"""

test_data = test_data_string.strip().split("\n")
expected = (None, None, None, None)

# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    pass


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    pass


# Output ---------------------------------------------------------------------------------------


results = [
    ("Test Part 1:", part1(test_data), expected[0]),
    ("Part 1:", part1(), expected[1]),
    ("Test Part 2:", part2(test_data), expected[2]),
    ("Part 2:", part2(), expected[3]),
]

for result in results:
    print(result[0], result[1])
    if result[2] and result[1] != result[2]:
        print("Expected:", result[2])
