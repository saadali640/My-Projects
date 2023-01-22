# TODO
from cs50 import get_float

get_dollars = 0

while True:
    get_dollars = get_float("Change owed: ")
    if get_dollars >= 0:
        break
get_dollars *= 100
calculate_quarters = get_dollars // 25

remainder = get_dollars - (25 * calculate_quarters)

calculate_dimes = remainder // 10

remainder2 = remainder - (10 * calculate_dimes)

calculate_nickels = remainder2 // 5

remainder3 = remainder2 - (5 * calculate_nickels)

calculate_pennies = remainder3 // 1

change = calculate_quarters + calculate_dimes + calculate_nickels + calculate_pennies

print(f"cents = {change}")
