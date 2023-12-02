from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata (optional) ---------------------------------------------------------------------------


# data = [
#     "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
#     "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
#     "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
#     "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
#     "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
# ]


# Shared ---------------------------------------------------------------------------------------


def parse_game_details(line):
    game_id, game_details = line.split(": ")
    game_id = int(game_id.split(" ")[1])
    subsets = []
    for detail in game_details.split("; "):
        cube_counts = {}
        for part in detail.split(", "):
            count, color = part.split(" ")
            cube_counts[color] = int(count)
        subsets.append(cube_counts)
    return game_id, subsets


# Part 1 ---------------------------------------------------------------------------------------


def part1():
    return sum_possible_game_ids(data)


def is_game_possible(subsets, constraints):
    for subset in subsets:
        for color in subset:
            if subset[color] > constraints[color]:
                return False
    return True


def sum_possible_game_ids(data):
    constraints = {"red": 12, "green": 13, "blue": 14}
    total_sum = 0
    for line in data:
        game_id, subsets = parse_game_details(line)
        if is_game_possible(subsets, constraints):
            total_sum += game_id
    return total_sum


# Part 2 ---------------------------------------------------------------------------------------


def part2():
    parsed_games = [parse_game_details(line) for line in data]
    min_cubes_list = min_cubes_per_color(parsed_games)
    return calculate_power_of_games(min_cubes_list)


def min_cubes_per_color(games):
    min_cubes_list = []
    for game in games:
        game = game[1]
        red, green, blue = 0, 0, 0
        for move in game:
            red = max(red, move.get("red", 0))
            green = max(green, move.get("green", 0))
            blue = max(blue, move.get("blue", 0))
        min_cubes_list.append((red, green, blue))
    return min_cubes_list


def calculate_power_of_games(min_cubes_list):
    total_power = 0
    for red, green, blue in min_cubes_list:
        total_power += red * green * blue
    return total_power


# Output ---------------------------------------------------------------------------------------


print("Part 1:", part1())
print("Part 2:", part2())
