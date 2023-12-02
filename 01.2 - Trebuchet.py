from modules import DataManager

data = DataManager(__file__).get_data_string()

num_dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

sum = 0
for val in data:
    for key, value in num_dict.items():
        val = val.replace(
            key, key + value + key
        )  # Required since the numbers can overlap: e.g. twone contains one and two
    first_number = next(char for char in val if char.isdigit())
    last_number = next(char for char in reversed(val) if char.isdigit())
    sum += int(first_number + last_number)

print(sum)
