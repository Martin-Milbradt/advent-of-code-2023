import time

from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (21, 6935, 525152, 3920437278260)


# Shared ---------------------------------------------------------------------------------------


def count_arrangements(springs, groups, lookup=None, streak=False) -> int:
    global looking_up, next_print
    if lookup is None:
        lookup = {}
    key = springs + ",".join(map(str, groups)) + str(streak)
    if time_tracking:
        before = time.time()
    val = lookup.get(key)
    if time_tracking:
        after = time.time()
        total = after - start
        looking_up += after - before
        if total > next_print:
            print(
                f"Time spent looking up: {looking_up:.2f}",
                f"s. Ratio: {looking_up / total:.1%}",
            )
            next_print += 1
    if val:
        return val
    if not springs:
        done = len(groups) == 0 or groups == [0]
        val = 1 if done else 0
    elif len(springs) < sum(groups) + len(groups) - 1:
        val = 0  # not enough space for the groups
    elif springs.count("#") + springs.count("?") < sum(groups):
        val = 0  # not enough broken springs
    else:
        match springs[0]:
            case ".":
                val = count_operational(springs[1:], groups, lookup, streak)
            case "#":
                val = count_broken(springs[1:], groups, lookup)
            case "?":
                val = count_operational(
                    springs[1:], groups.copy(), lookup, streak,
                ) + count_broken(springs[1:], groups.copy(), lookup)
            case _:
                raise ValueError("Unexpected character:" + springs[0])
    lookup[key] = val
    if isinstance(val, bool):
        print(f"{val} is bool")
    return val


def count_operational(springs, groups, lookup, streak) -> int:
    if streak:
        return 0
    if groups and groups[0] == 0:
        groups = groups[1:]
    return count_arrangements(springs, groups, lookup)


def count_broken(springs, groups, lookup) -> int:
    if not groups or groups[0] == 0:
        return 0
    groups[0] -= 1
    streak = groups[0] != 0
    return count_arrangements(springs, groups, lookup, streak)


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    total = 0
    for line in input:
        springs, groups = line.split()
        groups = list(map(int, groups.split(",")))
        arrangements = count_arrangements(springs, groups)
        if debug:
            print(line, "-", arrangements)
        total += arrangements
    return total


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    total = 0
    for line in input:
        springs, groups = line.split()
        springs = "?".join([springs] * 5)
        groups = list(map(int, groups.split(","))) * 5
        arrangements = count_arrangements(springs, groups)
        if debug:
            print(line, "-", arrangements)
        total += arrangements
    return total


# Debugging ------------------------------------------------------------------------------------


time_tracking = True
start = time.time()
looking_up = 0
next_print = 1


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
