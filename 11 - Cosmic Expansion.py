from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (374, 10276166, 1030, 598693078798)

# Shared ---------------------------------------------------------------------------------------


def sum_distances(input, factor) -> int:
    universe = get_universe(input)
    empty_rows = [all(cell == "." for cell in row) for row in universe]
    empty_cols = [
        all(input[row][col] == "." for row in range(len(input)))
        for col in range(len(input[0]))
    ]
    galaxy_positions = [
        (i, j)
        for i, row in enumerate(universe)
        for j, cell in enumerate(row)
        if cell == "#"
    ]
    if debug:
        print_universe(universe)
        print_galaxy_positions(galaxy_positions)

    return int(  # cast to int since we're dealing with large numbers
        sum(calculate_distances(galaxy_positions, empty_rows, empty_cols, factor)),
    )


def get_universe(input):
    return [list(row) for row in input]


def calculate_distances(galaxy_positions, empty_rows, empty_cols, factor):
    distances = []
    for idx, g1 in enumerate(galaxy_positions):
        for g2 in galaxy_positions[idx + 1 :]:
            dist = abs(g1[0] - g2[0])
            for i in bi_range(g1[0], g2[0]):
                if empty_rows[i]:
                    dist += factor - 1
            dist += abs(g1[1] - g2[1])
            for j in bi_range(g1[1], g2[1]):
                if empty_cols[j]:
                    dist += factor - 1
            distances.append(dist)
            if debug:
                print(f"Distance between {g1} and {g2} is {dist}")
    return distances


def bi_range(a, b):
    if a < b:
        return range(a, b)
    return range(b, a)


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return sum_distances(input, 2)


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return sum_distances(input, 1e6)


def part2_test(input=data) -> int:
    return sum_distances(input, 10)


# Debugging ------------------------------------------------------------------------------------


def print_universe(universe) -> None:
    print("Universe:")
    for row in universe:
        print("".join(row))


def print_galaxy_positions(galaxy_positions) -> None:
    print("Galaxy Positions:")
    for i, pos in enumerate(galaxy_positions):
        print(f"Galaxy {i+1}: Position {pos}")


# Output ---------------------------------------------------------------------------------------


results = [
    ("Test Part 1:", part1, test_data, expected[0], debug[0]),
    ("Part 1:", part1, data, expected[1], debug[1]),
    ("Test Part 2:", part2_test, test_data, expected[2], debug[2]),
    ("Part 2:", part2, data, expected[3], debug[3]),
]

for result in results:
    debug = result[4]
    value = result[1](result[2])
    print(result[0], value)
    if result[3] and value != result[3]:
        print("Expected:", result[3])
