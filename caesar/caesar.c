#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])

{
    //all
    string plain;
    // check argument
    {
        //1

        if (argc != 2)

        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }//1

    int argv1isnotnum = 0;
    {
        //2

        for (int i = 0; i < strlen(argv[1]); i++)

            if (!isdigit(argv[1][i]))

                    argv1isnotnum = 1;


   if (argv1isnotnum == 1)
    {
            printf("Usage: ./caesar key\n");
            return 1;
    }
        // get plain text
        else
            plain = get_string("plaintext:  ");
   printf("ciphertext: ");

    }//2


    int key = atoi(argv[1]);
    // change argv to int & encrept plain text using the key in the argumen

    {
        //3

        for (int i = 0; i < strlen(plain); i++)



            if (!isalpha(plain[i]))

                    printf("%c", plain[i]);


            else if (islower(plain[i]))

                    printf("%c", ((plain[i] - 'a') + key) % 26 + 'a');

            else if (isupper(plain[i]))

                printf("%c", ((plain[i] - 'A') + key) % 26 + 'A');

    }//3


    {
        //4
        printf("\n");
    }//4
}//all

