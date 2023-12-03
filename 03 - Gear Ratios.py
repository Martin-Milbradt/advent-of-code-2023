from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata (optional) ---------------------------------------------------------------------------

# data = [
#     "467..114..",
#     "...*......",
#     "..35..633.",
#     "......#...",
#     "617*......",
#     ".....+.58.",
#     "..592.....",
#     "......755.",
#     "...$.*....",
#     ".664.598..",
# ]

# Shared ---------------------------------------------------------------------------------------

directions = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


# Function to check if a position is within the bounds of the schematic
def in_bounds(x, y):
    return 0 <= x < len(data) and 0 <= y < len(data[0])


# Part 1 ---------------------------------------------------------------------------------------


def part1():
    return sum_part_numbers(data)


def sum_part_numbers(data):
    part_sum = 0
    visited = set()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j].isdigit() and (i, j) not in visited:
                # Find the full number starting at this digit
                full_number = data[i][j]
                k = j + 1
                while k < len(data[i]) and data[i][k].isdigit():
                    full_number += data[i][k]
                    visited.add((i, k))
                    k += 1

                # Check if any part of the number is adjacent to a symbol
                for x in range(j, k):
                    if adjacent_to_symbol(i, x):
                        part_sum += int(full_number)
                        break

    return part_sum


def is_symbol(char):
    return not char.isdigit() and char != "."


def adjacent_to_symbol(i, j):
    for di, dj in directions:
        if in_bounds(i + di, j + dj) and is_symbol(data[i + di][j + dj]):
            return True
    return False


# Part 2 ---------------------------------------------------------------------------------------


def part2():
    return sum_gear_ratios_corrected_v5(data)


def sum_gear_ratios_corrected_v5(data):
    total_gear_ratio = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "*":
                adjacent_numbers = adjacent_part_numbers(i, j)
                if len(adjacent_numbers) == 2:
                    total_gear_ratio += adjacent_numbers.pop() * adjacent_numbers.pop()

    return total_gear_ratio


def adjacent_part_numbers(i0, j0):
    part_numbers = []
    visited = set()
    for di, dj in directions:
        i, j = i0 + di, j0 + dj
        if in_bounds(i, j) and data[i][j].isdigit() and (i, j) not in visited:
            # Find the start of the number
            while in_bounds(i, j - 1) and data[i][j - 1].isdigit():
                j -= 1
            full_number = ""
            # Extend in the original direction to find the entire number
            while in_bounds(i, j) and data[i][j].isdigit():
                full_number += data[i][j]
                visited.add((i, j))
                j += 1
            part_numbers.append(int(full_number))
    return part_numbers


# Output ---------------------------------------------------------------------------------------


print("Part 1:", part1())
print("Part 2:", part2())
