from modules import DataManager

data = DataManager(__file__).get_data_string()


# Testdata (optional) ---------------------------------------------------------------------------


# data = [
#     "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
#     "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
#     "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
#     "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
#     "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
#     "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
# ]


# Shared ---------------------------------------------------------------------------------------


# Part 1 ---------------------------------------------------------------------------------------


def part1() -> int:
    return calculate_card_points(data)


def calculate_card_points(data):
    total_points = 0

    for line in data:
        line = line.split(": ")[1]
        winning_numbers, our_numbers = line.split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        our_numbers = set(map(int, our_numbers.split()))
        matches = winning_numbers.intersection(our_numbers)
        if matches:
            points = 2 ** (len(matches) - 1)
            total_points += points

    return total_points


# Part 2 ---------------------------------------------------------------------------------------


def part2() -> int:
    return count_scratchcards(data)


def count_scratchcards(data):
    cards = [1] * len(data)

    for i, line in enumerate(data):
        line = line.split(": ")[1]
        winning_numbers, our_numbers = line.split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        our_numbers = set(map(int, our_numbers.split()))
        matches = winning_numbers.intersection(our_numbers)
        for j in range(i + 1, min(i + 1 + len(matches), len(data))):
            cards[j] += cards[i]

    return sum(cards)


# Output ---------------------------------------------------------------------------------------


print("Part 1:", part1())
print("Part 2:", part2())
