#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])

{
    string plain;
    // check argument
    {

    if (argc != 2)

    {
    printf("Usage: ./substitution key\n");
    return 1;
    }

    }

    int argv1isnotalpha = 0;
    int argv1length = 0;
    int argv1norepeated = 0;
    { // key must only contain alphabetic characters

    for (int i = 0; i < strlen(argv[1]); i++)

    if (!isalpha(argv[1][i]))

    argv1isnotalpha = 1;


   if (argv1isnotalpha == 1)
    {
    printf("Key must only contain alphabetic characters.\n");
    return 1;
    }


    // Key must contain 26 characters
    if (strlen(argv[1]) != 26)

    argv1length = 1;

    if (argv1length == 1)
        {
    printf("Key must contain 26 characters.\n");
    return 1;
    }
  // key must not contain repeated letters
        for (int i = 0; i < strlen(argv[1]); i++)
   for (int r = i + 1; r < strlen(argv[1]); r++)

    if (tolower(argv[1][i]) == tolower(argv[1][r]))

    argv1norepeated = 1;


   if (argv1norepeated == 1)
    {
    printf("Key must not contain repeated characters.\n");
    return 1;
    }


    // get plain text
   else
   plain = get_string("plaintext:  ");
   printf("ciphertext: ");

    }


    // encrept plain text using the key in the argumen

    {

    for (int a = 0; a < strlen(argv[1]); a++)

    if (isupper(argv[1][a]))

    argv[1][a] += 32;


    for (int i = 0; i < strlen(plain); i++)


    if (!isalpha(plain[i]))

    printf("%c", plain[i]);


    else if (islower(plain[i]))

    printf("%c", argv[1][plain[i] - 'a']);

    else if (isupper(plain[i]))

    printf("%c", argv[1][plain[i] - 'A'] - 32);

    }


    {
    printf("\n");
    }
}

