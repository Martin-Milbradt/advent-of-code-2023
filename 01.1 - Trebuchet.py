from modules import DataManager

data = DataManager(__file__).get_data_string()
sum = 0
for val in data:
    first_number = next(char for char in val if char.isdigit())
    last_number = next(char for char in reversed(val) if char.isdigit())
    sum += int(first_number + last_number)

print(sum)
