from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (405, 37381, 400, 28210)


# Shared ---------------------------------------------------------------------------------------


def find_mirrors(data, errors=False):
    total = 0
    pattern = []

    for line in data:
        if line:
            pattern.append(line)
            continue

        vertical_reflection = find_vertical_reflection(pattern, errors)
        horizontal_reflection = find_horizontal_reflection(pattern, errors)

        if vertical_reflection:
            total += vertical_reflection
        elif horizontal_reflection:
            total += 100 * horizontal_reflection

        pattern = []

    # Parse last pattern (no newline at the end)
    vertical_reflection = find_vertical_reflection(pattern, errors)
    horizontal_reflection = find_horizontal_reflection(pattern, errors)

    if vertical_reflection:
        total += vertical_reflection
    elif horizontal_reflection:
        total += 100 * horizontal_reflection

    return total


def find_horizontal_reflection(pattern, errors=False):
    length = len(pattern)
    for i in range(1, length):
        error = errors
        j0 = i - 1
        j1 = i
        mirror = True
        while j0 > -1 and j1 < length:
            if debug:
                print("Comparing", j0, pattern[j0], "to", j1, pattern[j1])
            if pattern[j0] != pattern[j1]:
                if error and off_by_one(pattern[j0], pattern[j1]):
                    error = False
                    if debug:
                        print("Smudge found")
                else:
                    if debug:
                        print("No Match")
                    mirror = False
                    break
            if debug:
                print("Match")
            j0 -= 1
            j1 += 1
        if mirror and not error:
            if debug:
                print("Found Mirror at", i)
            return i
    return False


def find_vertical_reflection(pattern, errors=False):
    transposed = ["".join(t) for t in zip(*pattern)]
    return find_horizontal_reflection(transposed, errors)


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return find_mirrors(input)


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return find_mirrors(input, True)


def off_by_one(str1, str2):
    differences = sum(1 for a, b in zip(str1, str2) if a != b)
    return differences == 1


# Debugging ------------------------------------------------------------------------------------


# Output ---------------------------------------------------------------------------------------


results = [
    ("Test Part 1:", part1, test_data, expected[0], debug[0]),
    ("Part 1:", part1, data, expected[1], debug[1]),
    ("Test Part 2:", part2, test_data, expected[2], debug[2]),
    ("Part 2:", part2, data, expected[3], debug[3]),
]

for result in results:
    debug = result[4]  # this is a global variable
    value = result[1](result[2])
    print(result[0], value)
    if result[3] and value != result[3]:
        print("Expected:", result[3])
