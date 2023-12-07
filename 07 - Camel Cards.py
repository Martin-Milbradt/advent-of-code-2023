from modules import DataManager
from enum import Enum

data = DataManager(__file__).get_data_string()


# Testdata -------------------------------------------------------------------------------------


test_data_string = """
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
"""

test_data = test_data_string.strip().split("\n")


# Shared ---------------------------------------------------------------------------------------


class Ranking(Enum):
    FIVE = 50
    FOUR = 40
    FULL = 32
    THREE = 30
    PAIRS = 22
    TWO = 20
    ONE = 10


def calculate_total_winnings(input, rank_hand, values):
    hands = []

    # Parse input and classify each hand
    for line in input:
        hand, bid = line.split()
        bid = int(bid)
        hand_type = rank_hand(hand)

        hands.append((hand_type, hand, bid))

    # Sort hands by type and then by card values
    hands.sort(key=lambda x: (x[0].value, [card_value(card, values) for card in x[1]]))
    winnings = [bid * (rank + 1) for rank, (_, _, bid) in enumerate(hands)]
    total_winnings = sum(winnings)

    return total_winnings


def rank_hand(counts) -> Ranking:
    if sum(counts.values()) != 5:
        raise ValueError(f"Not a legal hand: {counts}")
    max_count = max(counts.values())
    # Classify based on counts
    if max_count == 5:
        return Ranking.FIVE
    elif max_count == 4:
        return Ranking.FOUR
    elif sorted(counts.values()) == [2, 3]:
        return Ranking.FULL
    elif max_count == 3:
        return Ranking.THREE
    elif sorted(counts.values()) == [1, 2, 2]:
        return Ranking.PAIRS
    elif max_count == 2:
        return Ranking.TWO
    elif max_count == 1:
        return Ranking.ONE
    raise ValueError(f"No classification found: {counts}")


def card_value(card, values):
    if card in values.keys():
        return values[card]
    return int(card)


# Part 1 ---------------------------------------------------------------------------------------


values1 = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


def part1(input=data) -> int:
    return calculate_total_winnings(input, rank_hand_1, values1)


def rank_hand_1(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return rank_hand(counts)


# Part 2 ---------------------------------------------------------------------------------------


values2 = {"A": 14, "K": 13, "Q": 12, "T": 10, "J": 0}


def part2(input=data) -> int:
    return calculate_total_winnings(input, rank_hand_2, values2)


def rank_hand_2(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    jokers = counts.pop("J", 0)
    if jokers == 5:
        return Ranking.FIVE
    most_common_card = max(counts, key=counts.get)
    counts[most_common_card] += jokers
    return rank_hand(counts)


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
