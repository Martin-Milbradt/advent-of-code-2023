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


dirs = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
inverse = {"^": "v", ">": "<", "v": "^", "<": ">", "o": "o"}


def part1(input=data) -> int:
    grid = parse_input(input)
    return find_least_heat_loss(grid)


def parse_input(input):
    """Parse the input data into a grid."""
    return [[int(char) for char in line] for line in input]


def find_least_heat_loss(losses):
    """Find the path with the least heat loss."""
    rows, cols = len(losses), len(losses[0])
    traversal = get_diagonal_traversal(len(losses), len(losses[0]))
    losses = pad_with_inf(losses)
    old, new = False, True
    expected_total = [[float("inf")] * (cols + 2) for _ in range(rows + 2)]
    expected_total[rows][cols] = losses[rows][cols]
    while old != new:
        old = new
        expected_total, directions = update_expected_losses(
            expected_total, losses, traversal
        )
        new = "".join(str(c) for row in expected_total for c in row)
    steps, loss = calculate_loss(losses, directions)
    if debug:
        print("Simple solution (steps, loss)", steps, loss)
    steps, loss = calculate_route(losses, directions, [(1, 1)], [0], [(1, 1)])
    if debug:
        print("Complex solution (steps, loss)", steps, loss)
    return loss


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


def calculate_route(
    loss_matrix,
    directions,
    coords,
    losses,
    visited,
    lvl=0,
    steps="o",
    forbidden="",
):
    if forbidden == "o":  # Can't backtrack from the start
        return steps, float("inf")
    min_loss = float("inf")
    min_steps = "o"
    row, col = coords[-1]
    while row != len(loss_matrix) - 2 or col != len(loss_matrix[0]) - 2:
        opts = directions[row][col]
        if opts == 0:  # Return if we went out of bounds
            return steps, float("inf")
        if opts[0] * 3 == steps[-3:]:
            if lvl < 100:  # Fork and go back if we're at 3 in a row
                for b in range(1, min(max_backtrack, len(steps)) + 1):
                    if debug:
                        print(
                            "Level",
                            lvl,
                            "- Three in a row after",
                            len(steps),
                            "steps, backtracking",
                            b,
                        )
                        print(coords[:-b])
                    alt_steps, alt_loss = calculate_route(
                        loss_matrix,
                        directions,
                        coords[:-b],
                        losses[:-b],
                        visited[:-b],
                        lvl + 1,
                        steps[:-b],
                        steps[-b],
                    )
                    if alt_loss < min_loss:
                        min_steps, min_loss = alt_steps, alt_loss
            elif debug:
                print("Recursion level too high after", len(steps))
        found = False
        for o in opts:
            d = dirs[o]
            row += d[0]
            col += d[1]
            if (
                o != forbidden
                and o * 3 != steps[-3:]
                and o != inverse[steps[-1]]
                and (row, col) not in visited
            ):
                found = True
                break
        if not found:
            return steps, float("inf")
        steps += o
        losses.append(losses[-1] + loss_matrix[row][col])
        coords.append((row, col))
        visited.append((row, col))
    losses = losses[-1]
    if min_loss < losses:
        return min_steps, min_loss
    return steps, losses


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
