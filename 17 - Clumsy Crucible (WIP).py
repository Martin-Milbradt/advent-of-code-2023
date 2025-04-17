import heapq

from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (102, None, None, None)
max_backtrack = 5

# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def parse_input(input):
    return [[int(char) for char in line] for line in input]


dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
expected_total = None
from_start = None
grid = None


def part1(input=data) -> int:
    global grid
    grid = parse_input(input)
    return find_least_heat_loss(grid)


def find_least_heat_loss(input):
    global expected_total, from_start
    rows, cols = len(input), len(input[0])
    traversal = get_diagonal_traversal(len(input), len(input[0]))
    loss_matrix = pad_with_inf(input)
    old, new = False, True
    expected_total = [[float("inf")] * (cols + 2) for _ in range(rows + 2)]
    expected_total[rows][cols] = loss_matrix[rows][cols]
    while old != new:
        old = new
        expected_total, _ = update_expected_losses(
            expected_total, loss_matrix, traversal,
        )
        new = "".join(str(c) for row in expected_total for c in row)
    from_start = [[float("inf")] * (cols + 2) for _ in range(rows + 2)]
    return a_star((1, 1), (rows, cols))


def pad_with_inf(matrix):
    cols = len(matrix[0])

    # Pad existing rows with float('inf') at start and end
    padded_matrix = [[float("inf")] + row + [float("inf")] for row in matrix]

    # Add a new row of float('inf') at the top and bottom
    inf_row = [float("inf")] * (cols + 2)
    padded_matrix.insert(0, inf_row)
    padded_matrix.append(inf_row)

    return padded_matrix


def get_diagonal_traversal(rows, cols):
    traversal = []

    # This already prepares for the padded matrix
    for start_row in range(rows - 1, 0, -1):  # Skips bottom right corner
        row, col = start_row, cols
        while row <= rows and col >= 1:
            traversal.append((row, col))
            row += 1
            col -= 1

    # Cover the upper half
    for start_col in range(cols - 1, 0, -1):
        row, col = 1, start_col
        while row <= rows and col >= 1:
            traversal.append((row, col))
            row += 1
            col -= 1

    return traversal


def update_expected_losses(expected_total, losses, traversal):
    directions = [[0] * len(expected_total[0]) for _ in range(len(expected_total))]
    for row, col in traversal:
        opts = {
            "^": expected_total[row - 1][col],
            ">": expected_total[row][col + 1],
            "v": expected_total[row + 1][col],
            "<": expected_total[row][col - 1],
        }
        sorted_keys = sorted(opts, key=lambda k, opts=opts: opts[k])
        expected_total[row][col] = losses[row][col] + opts[sorted_keys[0]]
        directions[row][col] = sorted_keys
    return expected_total, directions


def h(c):
    return expected_total[c[0]][c[1]]


def set_g(c, v) -> None:
    global from_start
    from_start[c[0]][c[1]] = v


def g(c):
    return from_start[c[0]][c[1]]


def f(c):
    return g(c) + h(c)


def loss(c):
    return grid[c[0] - 1][c[1] - 1]


def get_neighbors(c, d):
    neighbors = [(c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0] + 1, c[1]), (c[0], c[1] - 1)]
    return [
        n for n in neighbors if h(n) != float("inf") and n[0] + d[0] + n[1] + d[1] != 0
    ]


def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (h(start), start, [(0, 0)]))
    came_from = {}

    from_start[start[0]][start[1]] = 0

    while open_set:
        _, pos, d = heapq.heappop(open_set)
        if pos == goal:
            print("Found goal")
            return 4

        neighbors = get_neighbors(pos, d[-1])
        for i, neighbor in enumerate(neighbors):
            if all(e == dirs[i] for e in d[-3:]):
                continue
            tentative_g_score = g(pos) + loss(neighbor)
            if tentative_g_score < g(neighbor):
                # This is a better path, record it
                came_from[neighbor] = pos
                set_g(neighbor, tentative_g_score)
                if neighbor not in [item[1] for item in open_set]:
                    d_copy = d.copy()
                    d_copy.append(dirs[i])
                    heapq.heappush(open_set, (f(neighbor), neighbor, d_copy))

    return float("inf")


def calculate_loss(losses, directions):
    steps = ""
    row, col = 1, 1
    loss = 0
    while row != len(losses) - 2 or col != len(losses[0]) - 2:
        steps += directions[row][col][0]
        loss += losses[row][col]
        d = dirs[directions[row][col][0]]
        row += d[0]
        col += d[1]
    return steps, loss


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    pass


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
