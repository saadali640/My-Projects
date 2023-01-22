# TODO
from cs50 import get_int

height = 0
# prompting user for height if input is not an int between 1 and 8
while height < 1 or height > 8:
    height = get_int("Height:")

for i in range(height):
    for j in range(height-i-1):
        print(" ", end="")
    for j in range(i+1):
        print("#", end="")
    for s in range(2):
        print(" ", end="")
    for j in range(i+1):
        print("#", end="")
    print()