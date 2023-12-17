from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
...
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (None, None, None, None)

# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    def turn(direction, tile):
        """Determine new direction after encountering a mirror."""
        if tile == "/":
            return {"right": "up", "up": "right", "left": "down", "down": "left"}[
                direction
            ]
        elif tile == "\\":
            return {"right": "down", "down": "right", "left": "up", "up": "left"}[
                direction
            ]
        return direction

    def move(pos, direction):
        """Move to the next position based on the current direction."""
        x, y = pos
        if direction == "right":
            return (x, y + 1)
        elif direction == "left":
            return (x, y - 1)
        elif direction == "up":
            return (x - 1, y)
        elif direction == "down":
            return (x + 1, y)

    # Initialize variables
    energized_tiles = set()
    beams = [(0, 0, "right")]  # starting position and direction

    while beams:
        new_beams = []
        for x, y, direction in beams:
            # Check if beam is outside the grid
            if not (0 <= x < len(input) and 0 <= y < len(input[0])):
                continue

            tile = input[x][y]
            energized_tiles.add((x, y))

            if tile in "/\\":
                new_direction = turn(direction, tile)
                new_beams.append((x, y, new_direction))
            elif tile in "|-":
                # Split the beam if it hits the flat side of a splitter
                if (direction == "right" and tile == "|") or (
                    direction == "down" and tile == "-"
                ):
                    new_beams.append((x, y, "up"))
                    new_beams.append((x, y, "down"))
                elif (direction == "left" and tile == "|") or (
                    direction == "up" and tile == "-"
                ):
                    new_beams.append((x, y, "right"))
                    new_beams.append((x, y, "left"))
                else:
                    # Pass through the splitter
                    new_beams.append((x, y, direction))
            else:
                # Continue in the same direction for empty space
                new_pos = move((x, y), direction)
                new_beams.append((new_pos[0], new_pos[1], direction))

        # Update beams with their new positions
        beams = new_beams

    return len(energized_tiles)


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
