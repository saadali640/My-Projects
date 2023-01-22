# TODO
from cs50 import get_string

grade = 0
countL = 0
countW = 1
countS = 0


# get string

text = get_string("Text: ")

# calculate number of letters

for char in text:

    if char.isalpha():
        countL += 1


# calculate number of words

for char in text:

    if char.isspace():
        countW += 1

# calculate number of sentences

for char in text:

    if char in ('!', '.', '?'):
        countS += 1

# get sum of letters

sumL = countL / countW * 100

# get sum of sentences


sumS = countS / countW * 100

# get index result

index = 0.0588 * sumL - 0.296 * sumS - 15.8
index = round(index)
grade = index

# print


if grade > 16:

    print("Grade 16+")

elif grade < 1:

    print("Before Grade 1")

else:

    print(f"Grade: {grade}")
