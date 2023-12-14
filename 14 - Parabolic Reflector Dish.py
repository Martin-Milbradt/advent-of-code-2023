from modules import DataManager
import copy

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (136, 111979, 64, 102055)


# Shared ---------------------------------------------------------------------------------------


dirs = []
free_dirs = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
]  # Steps for the next free position depending tilt


def tilt(grid, dir=0):
    j_max = len(grid[0]) - 1
    i_max = len(grid) - 1
    free = dirs[dir][0]
    di = free_dirs[dir][0]
    dj = free_dirs[dir][1]
    # Doing everything in one loop is ugly, but reduces code duplication
    for i, j in dirs[dir]:
        match dir:
            case 0:
                if i == 0:
                    free = [0, j]
            case 1:
                if j == 0:
                    free = [i, 0]
            case 2:
                if i == i_max:
                    free = [i_max, j]
            case 3:
                if j == j_max:
                    free = [i, j_max]
            case _:
                raise ValueError("Invalid direction:", dir)
        if grid[i][j] == "O":
            # Place the rock at the next free position
            grid[i][j] = "."
            grid[free[0]][free[1]] = "O"
            free[0] += di
            free[1] += dj
        elif grid[i][j] == "#":
            if di != 0:
                free[0] = i + di
            else:
                free[1] = j + dj


def calculate_load(grid):
    height = len(grid)
    width = len(grid[0])

    # Calculate the load
    total_load = 0
    for x in range(width):
        for y in range(height):
            if grid[y][x] == "O":
                # Calculate the load for this rock
                total_load += height - y

    return total_load


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return part2(input, 0.25)


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data, cycles=1e9) -> int:
    global dirs
    steps = int(4 * cycles)
    height = len(input)
    width = len(input[0])
    grid = [list(s) for s in input]
    visited = ["".join(c for row in grid for c in row)]
    grids = [copy.deepcopy(grid)]
    dirs = [[], [], [], []]
    for j in range(width):
        for i in range(height):
            dirs[0].append([i, j])  # North
            dirs[2].append([width - i - 1, j])  # South
    for i in range(height):
        for j in range(width):
            dirs[1].append([i, j])  # East
            dirs[3].append([i, height - j - 1])  # West
    for i in range(steps):
        tilt(grid, i % 4)  # 0 = north, 1 = west, 2 = south, 3 = east
        if i % 4 == 3:
            identifier = "".join(c for row in grid for c in row)
            # Too much to brute force, so we look for periods
            if identifier in visited:
                idx = visited.index(identifier)
                period = (i + 1) / 4 - idx
                if debug:
                    print("Cycle found after", i + 1, "steps,", (i + 1) / 4, "cycles.")
                    print("Cylce length:", period)
                    print("Current Grid")
                    print_grid(grid)
                    print("Matching Grid", idx + 1)
                    print_grid(grids[idx])
                    print("Previous occurence after cycle:", idx + 1)
                    print(idx + 1)
                # If the period would start at the beginning this would be the first occurence
                offset = int((cycles - idx) % period)
                # Get the occurence of the final grid in the discovered period
                idx += offset
                final = grids[idx]
                return calculate_load(final)
            visited.append(identifier)
            # Saving all grids is a memory hungry approach, but it's fast
            grids.append(copy.deepcopy(grid))
    return calculate_load(grid)


# Debugging ------------------------------------------------------------------------------------


def print_grid(grid):
    for line in grid:
        print("".join(line))
    print()


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
