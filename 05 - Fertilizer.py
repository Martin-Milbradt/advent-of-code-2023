from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

test_data = test_data_string.strip().split("\n")


# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return find_lowest_location(input)


def find_lowest_location(data):
    seeds, maps = parse_data(data)
    lowest_location = float("inf")

    for number in seeds:
        for map in maps:
            number = apply_mapping(map, number)
        lowest_location = min(lowest_location, number)

    return lowest_location


def parse_data(data):
    seeds = []
    maps = []

    for line in data:
        if line.startswith("seeds:"):
            seeds = [int(x) for x in line.split()[1:]]
        elif line.endswith("map:"):
            maps.append([])
        elif len(line or "") > 0:
            parts = [int(x) for x in line.split()]
            maps[-1].append(parts)

    return seeds, maps


def apply_mapping(mapping, number):
    for destination_start, source_start, length in mapping:
        if source_start <= number < source_start + length:
            return destination_start + (number - source_start)
    return number  # Return the same number if not found in the mapping


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return find_lowest_location_arrays(input)


def parse_data_range(data):
    seeds = []
    maps = []

    for line in data:
        if line.startswith("seeds:"):
            numbers = [int(x) for x in line.split()[1:]]
            seeds = [
                (numbers[i], numbers[i] + numbers[i + 1] - 1)
                for i in range(0, len(numbers), 2)
            ]
        elif line.endswith("map:"):
            maps.append([])
        elif len(line or "") > 0:
            new_start, start, length = [int(x) for x in line.split()]
            maps[-1].append(
                (start, start + length - 1, new_start - start)
            )  # refactoring so it feels natural to me: (start, end, offset)

    return seeds, maps


def find_lowest_location_arrays(data):
    ranges, maps = parse_data_range(data)

    for map in maps:
        ranges = apply_mapping_tuples(map, ranges)

    return min(ranges)[0]


def apply_mapping_tuples(
    mapping: list[tuple[int, int, int]], ranges: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    new_ranges = []
    for start, end in ranges:
        overlap = False
        for map_start, map_end, offset in mapping:
            if map_start <= end and map_end >= start:
                overlap = True
                intersection_begin = max(map_start, start)
                intersection_end = min(map_end, end)

                if map_start > start:
                    ranges.append((start, map_start - 1))

                new_ranges.append(
                    (intersection_begin + offset, intersection_end + offset)
                )

                if end > map_end:
                    ranges.append((map_end + 1, end))
        if not overlap:
            new_ranges.append((start, end))

    return new_ranges


# Output ---------------------------------------------------------------------------------------

print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
