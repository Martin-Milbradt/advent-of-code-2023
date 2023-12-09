from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

test_data = test_data_string.strip().split("\n")


# Shared ---------------------------------------------------------------------------------------


def create_sequences(history):
    values = list(map(int, history.split()))

    # Generate sequences of differences
    sequences = [values]
    while sequences[-1].count(sequences[-1][0]) != len(sequences[-1]):
        new_sequence = [
            sequences[-1][i + 1] - sequences[-1][i]
            for i in range(len(sequences[-1]) - 1)
        ]
        sequences.append(new_sequence)
    return sequences


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return sum(extrapolate_next_value(history) for history in input)


def extrapolate_next_value(history):
    sequences = create_sequences(history)

    # Extrapolate the next value
    for i in range(len(sequences) - 1, 0, -1):
        sequences[i - 1].append(sequences[i - 1][-1] + sequences[i][-1])

    # Return the last element of the first sequence
    return sequences[0][-1]


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return sum(extrapolate_previous_value(history) for history in input)


def extrapolate_previous_value(history):
    sequences = create_sequences(history)

    # Extrapolate the previous value
    for i in range(len(sequences) - 1, 0, -1):
        sequences[i - 1].insert(0, sequences[i - 1][0] - sequences[i][0])

    # Return the first element of the first sequence
    return sequences[0][0]


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
