import contextlib
import re

from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

test_data = test_data_string.strip().split("\n")
debug = [False, False, False, False]
expected = (1320, 513158, 145, 200277)


# Shared ---------------------------------------------------------------------------------------


def custom_hash(s):
    current_value = 0
    for char in s:
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= 17
        current_value %= 256
    return current_value


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    steps = input[0].split(",")
    values = [custom_hash(step) for step in steps]
    return sum(values)


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    steps = input[0].split(",")
    boxes = [{} for _ in range(256)]
    for step in steps:
        parts = re.split("[-=]", step)
        label = parts[0]
        focal_length = int(parts[1]) if parts[1] else None
        update_boxes(boxes, label, step[len(label)], focal_length)
    return calculate_focusing_power(boxes)


def update_boxes(boxes, label, action, focal_length) -> None:
    box_number = custom_hash(label)
    if action == "-":
        with contextlib.suppress(KeyError):
            del boxes[box_number][label]
    else:
        boxes[box_number][label] = focal_length


def calculate_focusing_power(boxes):
    total_power = 0
    for box, lenses in enumerate(boxes, start=1):
        for slot, focal_length in enumerate(lenses.values(), start=1):
            total_power += box * slot * focal_length
    return total_power


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
