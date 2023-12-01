import modules

modules.init()
data = modules.get_data_string("1")
sum = 0
for val in data:
    first_number = next(char for char in val if char.isdigit())
    last_number = next(char for char in reversed(val) if char.isdigit())
    sum += int(first_number + last_number)

print(sum)
