from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
F-7-
|-S7
|F.|
L7FJ
FLJ.
"""

test_data = test_data_string.strip().split("\n")
expected = [7, 6725, 3, 383]

# Shared ---------------------------------------------------------------------------------------


directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
pipes = {
    "S": [[-1, 0], [0, 1]],  # North, East - just my test data
    "|": [[-1, 0], [1, 0]],  # North, South
    "-": [[0, 1], [0, -1]],  # East, West
    "L": [[-1, 0], [0, 1]],  # North, East
    "J": [[-1, 0], [0, -1]],  # North, West
    "7": [[1, 0], [0, -1]],  # South, West
    "F": [[0, 1], [1, 0]],  # East, South
}


def get_pos(pos, move):
    p1 = pos[0] + move[0]
    p2 = pos[1] + move[1]
    return [p1, p2]


def get_start(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                return [i, j]
    return None


# Part 1 ---------------------------------------------------------------------------------------


# Only handles my specific input (not even test data), since I didn't bother to figure out the start
def part1(input=data) -> int:
    grid = [list(line) for line in input]
    start = get_start(grid)

    pos1 = start.copy()
    pos2 = start.copy()
    move1 = [[-1, 0], [0, 1]]  # My "S" is going N-E
    move2 = [[-1, 0], [0, 1]]
    last_move1 = [1, 0]  # Inverse of move1
    last_move2 = [0, -1]  # Inverse of move2
    steps = 0
    while True:
        steps += 1
        i = 1 if get_pos(move1[0], last_move1) == [0, 0] else 0
        pos1 = get_pos(pos1, move1[i])
        if pos1 == pos2:
            return steps
        last_move1 = move1[i]
        i = 1 if get_pos(move2[0], last_move2) == [0, 0] else 0
        pos2 = get_pos(pos2, move2[i])
        if pos1 == pos2:
            return steps
        last_move2 = move2[i]
        move1 = pipes[grid[pos1[0]][pos1[1]]]
        move2 = pipes[grid[pos2[0]][pos2[1]]]


# Part 2 ---------------------------------------------------------------------------------------


# Only handles my specific input (not even test data), since I didn't bother to figure out the start
def part2(input=data) -> int:
    grid = [list(line) for line in input]
    start = get_start(grid)

    pos1 = start.copy()
    pos2 = start.copy()
    move1 = [[-1, 0], [0, 1]]  # My "S" is going N-E
    move2 = [[-1, 0], [0, 1]]
    last_move1 = [1, 0]  # Inverse of move1
    last_move2 = [0, -1]  # Inverse of move2
    visited = [start.copy()]
    while True:
        i = 1 if get_pos(move1[0], last_move1) == [0, 0] else 0
        pos1 = get_pos(pos1, move1[i])
        if pos1 == pos2:
            break
        visited += [pos1.copy()]
        last_move1 = move1[i]
        i = 1 if get_pos(move2[0], last_move2) == [0, 0] else 0
        pos2 = get_pos(pos2, move2[i])
        if pos1 == pos2:
            break
        visited += [pos2.copy()]
        last_move2 = move2[i]
        move1 = pipes[grid[pos1[0]][pos1[1]]]
        move2 = pipes[grid[pos2[0]][pos2[1]]]
    size = 0
    for cell in range(len(grid[0])):
        inside = False
        for row in range(len(grid)):
            if [row, cell] in visited:
                pos = grid[row][cell]
                match pos:
                    case "-":
                        inside = not inside
                    case "7":
                        l_switches = True
                    case "F":
                        l_switches = False
                    case "L" | "S":  # "S" == "L" just in my data
                        if l_switches:
                            inside = not inside
                    case "J":
                        if not l_switches:
                            inside = not inside
            elif inside:
                size += 1
    return size


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
