from modules import DataManager

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


ranking = {
    "Five of a kind": 5,
    "Four of a kind": 4,
    "Full house": 3.5,
    "Three of a kind": 3,
    "Two pair": 2.5,
    "One pair": 2,
    "High card": 1,
}


values = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


def calculate_total_winnings(input, part2=False):
    hands = []

    # Parse input and classify each hand
    for line in input:
        hand, bid = line.split()
        bid = int(bid)
        if part2:
            hand_type = classify_hand_joker(hand)
        else:
            hand_type = classify_hand_jack(hand)

        hands.append((hand_type, hand, bid))

    # Sort hands by type and then by card values
    hands.sort(key=lambda x: (ranking.get(x[0]), [card_value(card) for card in x[1]]))
    winnings = [bid * (rank + 1) for rank, (_, _, bid) in enumerate(hands)]
    total_winnings = sum(winnings)

    return total_winnings


def card_value(card, part2=False):
    if card in values.keys():
        return 0 if card == "J" and part2 else values[card]
    return int(card)


def classify_hand(counts):
    max_count = max(counts.values())
    # Classify based on counts
    if max_count == 5:
        return "Five of a kind"
    elif max_count == 4:
        return "Four of a kind"
    # part2: "aabbJ" is a full house and counted as [3 (2a+J), 3 (2b+J), 1 (J)]
    elif sorted(counts.values()) in ([2, 3], [1, 3, 3]):
        return "Full house"
    elif max_count == 3:
        return "Three of a kind"
    elif sorted(counts.values()) == [1, 2, 2]:
        return "Two pair"
    elif max_count == 2:
        return "One pair"
    else:
        # Precaution, should not happen
        if max_count > 1:
            raise ValueError(f"Unexpected max count for high card: {max_count}")
        return "High card"


# Part 1 ---------------------------------------------------------------------------------------


def part1(input=data) -> int:
    return calculate_total_winnings(input)


def classify_hand_jack(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return classify_hand(counts)


# Part 2 ---------------------------------------------------------------------------------------


def part2(input=data) -> int:
    return calculate_total_winnings(input, True)


def classify_hand_joker(hand):
    counts = {
        card: hand.count(card) + (0 if card == "J" else hand.count("J"))
        for card in set(hand)
    }
    return classify_hand(counts)


# Output ---------------------------------------------------------------------------------------


print("Test Part 1:", part1(test_data))
print("Part 1:", part1())
print("Test Part 2:", part2(test_data))
print("Part 2:", part2())
