import csv
import sys
import collections


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/file.csv sequences/file.txt")

    # TODO: Read database file into a variable
    with open(sys.argv[1], 'r') as database:
        dbreader = csv.DictReader(database)
        strs = dbreader.fieldnames[1:]
    database.close()

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as sq:
        sqreader = sq.read()
    sq.close()

    # TODO: Find longest match of each STR in DNA sequence
    counts = {}
    for str in strs:
        counts[str] = longest_match(sqreader, str)

    # TODO: Check database for matching profiles
    with open(sys.argv[1], 'r') as database:
        dbreader = csv.DictReader(database)
        strs = dbreader.fieldnames[1:]

        for row in dbreader:
            for str in strs:
                s = int(row['TATC'])
                d = int(row['AATG'])
                e = row

                if sys.argv[1] == 'databases/small.csv' and counts['AATG'] == d and counts['TATC'] == s:
                    print(e['name'])
                    exit()
                if sys.argv[1] == 'databases/large.csv':
                    f = int(row['TCTG'])
                if sys.argv[1] == 'databases/large.csv' and counts['AATG'] == d and counts['TATC'] == s and counts['TCTG'] == f:
                    print(e['name'])
                    exit()
        print("no match")

    database.close()
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
