from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
    Time:      7  15   30
    Distance:  9  40  200
"""

test_data = test_data_string.strip().split("\n")


# Shared ---------------------------------------------------------------------------------------


def calculate_ways_to_win_race(total_time, record_distance):
    ways_to_win = 0
    won = False
    for hold_time in range(total_time):
        speed = hold_time
        travel_time = total_time - hold_time
        distance = speed * travel_time
        if distance > record_distance:
            ways_to_win += 1
            won = True
            continue
        # winning -> loosing means our total distance will never be enough anymore
        if won:
            break
    return ways_to_win


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return calculate_total_ways(input)


def parse_data(input):
    times = [int(time) for time in input[0].split()[1:]]
    distances = [int(distance) for distance in input[1].split()[1:]]
    return times, distances


def calculate_total_ways(input):
    total_ways = 1
    times, distances = parse_data(input)
    for time, distance in zip(times, distances):
        ways_to_win = calculate_ways_to_win_race(time, distance)
        total_ways *= ways_to_win
    return total_ways


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return calculate_total_ways_single_race(input)


def parse_data_single_race(input):
    time = int("".join(input[0].split()[1:]))
    distance = int("".join(input[1].split()[1:]))
    return time, distance


def calculate_total_ways_single_race(input):
    time, distance = parse_data_single_race(input)
    return calculate_ways_to_win_race(time, distance)


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
